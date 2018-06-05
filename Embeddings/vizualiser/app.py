#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
from flask import Flask, render_template, request
import uuid
from Embeddings.vizualiser import SimiliarityVizualiser


app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route('/', methods=['GET'])
def render_index():
    models, categories = vizualiser.load()
    selected_problems = vizualiser.select_problems(models[0], categories[0])
    return render_template('index.html', models=models, categories=categories, problems=selected_problems)


@app.route('/refresh-questions', methods=['POST'])
def refresh_questions():
    model1 = request.form['model1']
    category = request.form['category']
    selected_problems = vizualiser.select_problems(model1, category)
    return render_template('questions.html', problems=selected_problems)


@app.route('/refresh-problem', methods=['POST'])
def refresh_problem():
    problem = vizualiser.get_problem_by_id(request.form['problem_id'])
    model1 = request.form['model1']
    model2 = request.form['model2']
    models = list(enumerate([model1, model2]))
    return render_template('problem.html', problem=problem, models=models)


@app.route('/refresh-comparison', methods=['POST'])
def refresh_comparison():
    problem_id = request.form['problem_id']
    model = request.form['model']
    choice_index = int(request.form['choice_index'])
    comparison_index = int(request.form['comparison_index'])
    comparison = vizualiser.get_comparison(problem_id, choice_index, comparison_index, model)
    return render_template('comparison.html', comparison=comparison)


if __name__ == '__main__':
    vizualiser = SimiliarityVizualiser('data')
    app.run(debug=True)
