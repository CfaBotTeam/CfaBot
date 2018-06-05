class ComparedToken:
    def __init__(self, token, scores):
        self.token_ = token
        self.scores_ = scores


class Comparison:
    def __init__(self, sentence1_compared_tokens, sentence2_compared_tokens):
        self.sentence1_tokens_ = sentence1_compared_tokens
        self.sentence2_tokens_ = sentence2_compared_tokens


class Problem:
    def __init__(self, id, model, category, problem):
        self.id_ = id
        self.models_ = {model}
        self.category_ = category
        self.question_ = problem['question']
        self.choices_comparisons_ = {}
        self.choices_scores_ = {}
        self.add_comparison(model, problem)

    def add_comparison(self, model, problem):
        self.choices_comparisons_[model] = list(map(lambda x: x['comparisons'], problem['choices_results']))
        self.choices_scores_[model] = list(map(lambda x: x['scores'], problem['choices_results']))

    def get_comparisons(self, model):
        return self.choices_comparisons_[model]

    def get_comparison_options(self, choice_index):
        # return list(range(len(self.choices_comparisons_[choice_index])))
        return [0]

    def get_choices(self):
        first_model = list(self.models_)[0]
        return [(i, chr(i + ord('A'))) for i in range(len(self.choices_comparisons_[first_model]))]

    def has_model(self, model):
        return model in self.models_

    def add_model(self, model, problem):
        if model in self.models_:
            print("Warning when loading data => Found the question '%s' twice for the same model" % self.id_)
            return
        self.models_.add(model)
        self.add_comparison(model, problem)

    def get_choice_score(self, model, choice_index, option_index):
        choice_comparisons = self.choices_comparisons_[model][choice_index]
        if len(choice_comparisons) == 0:
            return "0.0"
        choice = choice_comparisons[option_index][0]
        score = self.choices_scores_[model][choice_index][choice]
        return "%0.5f" % score
