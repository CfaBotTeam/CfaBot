class ComparedToken:
    def __init__(self, token, scores):
        self.token_ = token
        self.scores_ = scores


class NlpComparison:
    def __init__(self, sentence1_compared_tokens, sentence2_compared_tokens):
        self.sentence1_tokens_ = sentence1_compared_tokens
        self.sentence2_tokens_ = sentence2_compared_tokens


class Comparison:
    def __init__(self, q_definition, q_source, q_keyword, c_definition, c_source, c_keyword, score):
        self.q_definition_ = q_definition
        self.q_source_ = q_source
        self.q_keyword_ = q_keyword
        self.c_definition_ = c_definition
        self.c_source_ = c_source
        self.c_keyword_ = c_keyword
        self.score_ = score


class ComparisonResult:
    def __init__(self, comp, options, c_ordinal, f_index, o_index, c_index, file):
        self.q_keyword_ = comp.q_keyword_
        self.q_def_ = comp.q_definition_
        self.q_source_ = comp.q_source_
        self.score_ = comp.score_
        self.c_keyword_ = comp.c_keyword_
        self.c_source_ = comp.c_source_
        self.c_def_ = comp.c_definition_
        self.options_ = options
        self.c_ordinal_ = c_ordinal
        self.f_index_ = f_index
        self.o_index_ = o_index
        self.c_index_ = c_index
        self.file_ = file


class FileResult:
    def __init__(self, problem, model, dataset, provider, glossary):
        self.model_ = model
        self.dataset_ = dataset
        self.provider_ = provider
        self.glossary_ = glossary
        self.choices_ = problem['choices']
        self.predicted_answer_ = problem['predicted_answer']
        self.success_ = problem['real_answer'] == problem['predicted_answer']
        self.randomly_answered_ = problem['random_answer']
        self.random_label_ = "randomly" if self.randomly_answered_ else ''
        self.comparisons_ = self.parse_comparisons(problem)

    def parse_comparisons(self, problem):
        result = []
        for comparison in problem['comparisons']:
            q_def = comparison['q_def']
            q_keyword = comparison['q_keyword'] if 'q_keyword' in comparison else ''
            q_source = comparison['source']
            choice_comparisons = []
            for c_comp in comparison['c_comparisons']:
                c_comp_options = []
                for c_comp_option in c_comp:
                    c_def = c_comp_option['c_def']
                    c_keyword = c_comp_option['c_keyword'] if 'c_keyword' in c_comp_option else ''
                    c_source = c_comp_option['source']
                    score = self.format_score(c_comp_option['score'])
                    c_comp_options.append(Comparison(q_def, q_source, q_keyword, c_def, c_source, c_keyword, score))
                choice_comparisons.append(c_comp_options)
            result.append(choice_comparisons)
        return result

    def format_score(self, score):
        return "%0.5f" % score


class Problem:
    def __init__(self, id, fullname, model, category, problem, dataset, provider, glossary):
        self.id_ = id
        self.category_ = category
        self.question_ = problem['question']
        self.correct_answer_ = problem['real_answer']
        self.file_results_ = {}
        self.add_file_result(fullname, model, problem, dataset, provider, glossary)

    def add_file_result(self, fullname, model, problem, dataset, provider, glossary):
        self.file_results_[fullname] = FileResult(problem, model, dataset, provider, glossary)

    def get_file_result(self, filename):
        if filename not in self.file_results_:
            return None
        return self.file_results_[filename]

    def get_comparisons(self, filename):
        return self.file_results_[filename].comparisons_

    def get_comparison_results(self, files):
        first_file = list(self.file_results_.keys())[0]
        choices = self.file_results_[first_file].choices_
        comp_results = []
        for i_choice, choice in enumerate(choices):
            c_ordinal = chr(i_choice + ord('A'))
            for i_file, file in enumerate(files):
                file_result = self.get_file_result(file)
                comparisons_options = file_result.comparisons_[0][i_choice]
                options = list(range(len(comparisons_options)))
                o_index = 0
                o_comp = comparisons_options[o_index]
                res = ComparisonResult(o_comp, options, c_ordinal, i_file, o_index, i_choice, file)
                comp_results.append(res)
        return comp_results

    def get_choices(self):
        first_file = list(self.file_results_.keys())[0]
        return self.file_results_[first_file].choices_

    def has_file(self, filename):
        return filename in self.file_results_

    def add_file(self, filename, model, problem, dataset, provider, glossary):
        if self.has_file(filename):
            print("Warning when loading data => Found the question '%s' twice for the same filename %s" % (self.id_, filename))
            return
        self.add_file_result(filename, model, problem, dataset, provider, glossary)

    def get_success_indicator(self, files):
        file1_result = self.get_file_result(files[0])
        if len(files) > 1:
            file2_result = self.get_file_result(files[1])
            if file2_result is None:
                return 'static/img/left_ok_right_ko.png'
            if file1_result.success_ != file2_result.success_:
                if file1_result.success_:
                    return 'static/img/left_ok_right_ko.png'
                return 'static/img/left_ko_right_ok.png'
        if file1_result.success_:
            return 'static/img/success.png'
        return 'static/img/failure.png'
