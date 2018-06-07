import os.path


class ComparedToken:
    def __init__(self, token, scores):
        self.token_ = token
        self.scores_ = scores


class NlpComparison:
    def __init__(self, sentence1_compared_tokens, sentence2_compared_tokens):
        self.sentence1_tokens_ = sentence1_compared_tokens
        self.sentence2_tokens_ = sentence2_compared_tokens


class Comparison:
    def __init__(self, q_definition, q_source, c_definition, c_source, score):
        self.q_definition_ = q_definition
        self.q_source_ = q_source
        self.c_definition_ = c_definition
        self.c_source_ = c_source
        self.score_ = score


class FileResult:
    def __init__(self, problem, model):
        self.model_ = model
        self.choices_ = problem['choices']
        self.predicted_answer_ = problem['predicted_answer']
        self.randomly_answered_ = problem['random_answer']
        self.random_label_ = "randomly" if self.randomly_answered_ else ''
        self.comparisons_ = self.parse_comparisons(problem)

    def parse_comparisons(self, problem):
        result = []
        for comparison in problem['comparisons']:
            q_def = comparison['q_def']
            q_source = comparison['source']
            choice_comparisons = []
            for c_comp in comparison['c_comparisons']:
                c_comp_options = []
                for c_comp_option in c_comp:
                    c_def = c_comp_option['c_def']
                    c_source = c_comp_option['source']
                    score = c_comp_option['score']
                    c_comp_options.append(Comparison(q_def, q_source, c_def, c_source, score))
                choice_comparisons.append(c_comp_options)
            result.append(choice_comparisons)
        return result


class Problem:
    def __init__(self, id, fullname, model, category, problem):
        self.id_ = id
        self.category_ = category
        self.question_ = problem['question']
        self.correct_answer_ = problem['real_answer']
        self.file_results_ = {}
        self.add_file_result(fullname, model, problem)

    def add_file_result(self, fullname, model, problem):
        self.file_results_[fullname] = FileResult(problem, model)

    def get_file_result(self, filename):
        return self.file_results_[filename]

    def get_comparisons(self, filename):
        return self.file_results_[filename].comparisons_

    def get_comparison_options(self, filename, question_index, choice_index):
        question_comparisons = self.file_results_[filename].comparisons_[question_index]
        if len(question_comparisons) == 0:
            return []
        return list(range(len(question_comparisons[choice_index])))

    def get_choices_ordinals(self):
        first_file = list(self.file_results_.keys())[0]
        choices = self.file_results_[first_file].choices_
        return [(i, chr(i + ord('A'))) for i in range(len(choices))]

    def get_choices(self):
        first_file = list(self.file_results_.keys())[0]
        return self.file_results_[first_file].choices_

    def has_file(self, filename):
        return filename in self.file_results_

    def add_file(self, filename, model, problem):
        if self.has_file(filename):
            print("Warning when loading data => Found the question '%s' twice for the same filename %s" % (self.id_, filename))
            return
        self.add_file_result(filename, model, problem)

    def get_choice_score(self, filename, question_index, choice_index, option_index):
        question_comparisons = self.file_results_[filename].comparisons_[question_index]
        if len(question_comparisons) == 0:
            return "0.0"
        choice_comparisons = question_comparisons[choice_index]
        if len(choice_comparisons) == 0:
            return "0.0"
        return "%0.5f" % choice_comparisons[option_index].score_
