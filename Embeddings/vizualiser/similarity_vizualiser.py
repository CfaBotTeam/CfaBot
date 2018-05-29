#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
from flask import Flask, render_template, request
import uuid
import json
import spacy
from os import listdir
from os.path import isfile, join, dirname, basename
import numpy as np
import Embeddings.models


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


class ComparedToken:
    def __init__(self, token, scores):
        self.token_ = token
        self.scores_ = scores


class Comparison:
    def __init__(self, sentence1_compared_tokens, sentence2_compared_tokens):
        self.sentence1_ = sentence1_compared_tokens
        self.sentence2_ = sentence2_compared_tokens

    def get_sentence1_tokens(self):
        return list(map(lambda x: x.token_, self.sentence1_))

    def get_sentence2_tokens(self):
        return list(map(lambda x: x.token_, self.sentence2_))


class Problem:
    def __init__(self, model, category, problem):
        self.id_ = str(uuid.uuid4())
        self.model_ = model
        self.category_ = category
        self.question_ = problem['question']
        self.choices_comparisons_ = list(map(lambda x: x['comparisons'], problem['choices_results']))

    def get_comparison_options(self, choice_index):
        return list(range(len(self.choices_comparisons_[choice_index])))

    def has_choice_D(self):
        return len(self.choices_comparisons_) > 3


class SimiliarityVizualiser:
    def __init__(self, results_directory):
        self.nlp_models_ = {}
        self.results_directory_ = results_directory

    def load_category(self, model, category, result):
        for key, problem in result[category].items():
            self.all_problems_.append(Problem(model, category, problem))

    def load_all_problems(self):
        categories = set()
        for f in listdir(self.results_directory_):
            full_path = join(self.results_directory_, f)
            if not isfile(full_path):
                continue
            result = json.load(open(full_path, 'r'))
            model = result['model']
            self.all_models_.append(model)
            for key in result:
                if key == 'overall' or key == 'model':
                    continue
                if not key in categories:
                    categories.add(key)
                self.load_category(model, key, result)
        return categories

    def load(self):
        self.all_problems_ = []
        self.all_models_ = []
        self.all_categories_ = []
        categories = self.load_all_problems()
        for category in categories:
            self.all_categories_.append(category)
        self.all_categories_ = np.sort(self.all_categories_)
        return self.all_models_, self.all_categories_

    def select_problems(self, model, category):
        selected_problems = []
        for problem in self.all_problems_:
            if problem.model_ == model and problem.category_ == category:
                selected_problems.append(problem)
        return selected_problems

    def get_problem_by_id(self, id):
        for problem in self.all_problems_:
            if problem.id_ == id:
                return problem
        return None

    def get_nlp(self, model_name):
        if model_name != 'en':
            model_name = join(dirname(Embeddings.models.__file__), basename(model_name))
        if model_name not in self.nlp_models_:
            self.nlp_models_[model_name] = spacy.load(model_name, disable=['tagger', 'parser', 'ner', 'textcat'])
        return self.nlp_models_[model_name]

    def get_similarity(self, token1, token2):
        try:
            return token1.similarity(token2)
        except:
            return 0.0

    def get_sentence_compared_tokens(self, sentence1_nlp, sentence2_nlp):
        sentence_compared_tokens = []
        for token1 in sentence1_nlp:
            token1_scores = []
            for token2 in sentence2_nlp:
                token1_scores.append(self.get_similarity(token1, token2))
            sentence_compared_tokens.append(ComparedToken(token1, token1_scores))
        return sentence_compared_tokens

    def get_comparison(self, problem_id, choice_index, comparison_index):
        problem = self.get_problem_by_id(problem_id)
        nlp = self.get_nlp(problem.model_)
        sentences = problem.choices_comparisons_[choice_index][comparison_index]
        sentence1_nlp = nlp(sentences[0])
        sentence2_nlp = nlp(sentences[1])
        sentence1_compared_tokens = self.get_sentence_compared_tokens(sentence1_nlp, sentence2_nlp)
        sentence2_compared_tokens = self.get_sentence_compared_tokens(sentence2_nlp, sentence1_nlp)
        return Comparison(sentence1_compared_tokens, sentence2_compared_tokens)


@app.route('/', methods=['GET'])
def render_index():
    models, categories = vizualiser.load()
    selected_problems = vizualiser.select_problems(models[0], categories[0])
    return render_template('index.html', models=models, categories=categories, problems=selected_problems)


@app.route('/refresh-questions', methods=['POST'])
def refresh_questions():
    model = request.form['model']
    category = request.form['category']
    selected_problems = vizualiser.select_problems(model, category)
    return render_template('questions.html', problems=selected_problems)


@app.route('/refresh-problem', methods=['POST'])
def refresh_problem():
    problem = vizualiser.get_problem_by_id(request.form['problem_id'])
    return render_template('problem.html', problem=problem)


@app.route('/refresh-comparison', methods=['POST'])
def refresh_comparison():
    problem_id = request.form['problem_id']
    choice_index = int(request.form['choice_index'])
    comparison_index = int(request.form['comparison_index'])
    comparison = vizualiser.get_comparison(problem_id, choice_index, comparison_index)
    return render_template('comparison.html', comparison=comparison)


if __name__ == '__main__':
    vizualiser = SimiliarityVizualiser('data')
    app.run(debug=True)
