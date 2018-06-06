class ComparedToken:
    def __init__(self, token, scores):
        self.token_ = token
        self.scores_ = scores


class Comparison:
    def __init__(self, sentence1_compared_tokens, sentence2_compared_tokens):
        self.sentence1_tokens_ = sentence1_compared_tokens
        self.sentence2_tokens_ = sentence2_compared_tokens


class ModelResult:
    def __init__(self, problem):
        self.choices_comparisons_ = list(map(lambda x: x['comparisons'], problem['choices_results']))
        self.choices_scores_ = list(map(lambda x: x['scores'], problem['choices_results']))
        self.choices_ = list(map(lambda x: x['choice'], problem['choices_results']))
        self.predicted_answer_ = problem['predicted_answer']
        self.randomly_answered_ = problem['random_answer']
        self.random_label_ = "randomly" if self.randomly_answered_ else ''


class Problem:
    def __init__(self, id, model, category, problem):
        self.id_ = id
        self.category_ = category
        self.question_ = problem['question']
        self.correct_answer_ = problem['real_answer']
        self.model_results_ = {}
        self.add_model_result(model, problem)

    def add_model_result(self, model, problem):
        self.model_results_[model] = ModelResult(problem)

    def get_comparisons(self, model):
        return self.model_results_[model].choices_comparisons_

    def get_comparison_options(self, choice_index):
        # return list(range(len(self.choices_comparisons_[choice_index])))
        return [0]

    def get_choices_ordinals(self):
        first_model = list(self.model_results_.keys())[0]
        choices = self.model_results_[first_model].choices_
        return [(i, chr(i + ord('A'))) for i in range(len(choices))]

    def get_choices(self):
        first_model = list(self.model_results_.keys())[0]
        return self.model_results_[first_model].choices_

    def has_model(self, model):
        return model in self.model_results_

    def add_model(self, model, problem):
        if self.has_model(model):
            print("Warning when loading data => Found the question '%s' twice for the same model" % self.id_)
            return
        self.add_model_result(model, problem)

    def get_choice_score(self, model, choice_index, option_index):
        choice_comparisons = self.model_results_[model].choices_comparisons_[choice_index]
        if len(choice_comparisons) == 0:
            return "0.0"
        choice = choice_comparisons[option_index][0]
        score = self.model_results_[model].choices_scores_[choice_index][choice]
        return "%0.5f" % score

    def get_model_result(self, model):
        return self.model_results_[model]
