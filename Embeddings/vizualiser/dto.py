class ComparedToken:
    def __init__(self, token, scores):
        self.token_ = token
        self.scores_ = scores


class NlpComparison:
    def __init__(self, sentence1_compared_tokens, sentence2_compared_tokens):
        self.sentence1_tokens_ = sentence1_compared_tokens
        self.sentence2_tokens_ = sentence2_compared_tokens


class Comparison:
    def __init__(self, q_definition, q_source, q_keyword, q_gloss_keyword,
                 c_definition, c_source, c_keyword, c_gloss_keyword, score):
        self.q_definition_ = q_definition
        self.q_source_ = q_source
        self.q_keyword_ = q_keyword
        self.q_gloss_keyword_ = q_gloss_keyword
        self.c_definition_ = c_definition
        self.c_source_ = c_source
        self.c_keyword_ = c_keyword
        self.c_gloss_keyword_ = c_gloss_keyword
        self.score_ = score


class ComparisonResult:
    def __init__(self, comp, c_options, c_ordinal, f_index, c_index, q_options, file, max_score_q_index, max_score_c_index):
        self.q_keyword_ = comp.q_keyword_
        self.q_gloss_keyword_ = comp.q_gloss_keyword_
        self.q_def_ = comp.q_definition_
        self.q_source_ = comp.q_source_
        self.score_ = comp.score_
        self.c_keyword_ = comp.c_keyword_
        self.c_gloss_keyword_ = comp.c_gloss_keyword_
        self.c_source_ = comp.c_source_
        self.c_def_ = comp.c_definition_
        self.c_options_ = c_options
        self.c_ordinal_ = c_ordinal
        self.q_options_ = q_options
        self.f_index_ = f_index
        self.c_index_ = c_index
        self.file_ = file
        self.max_score_q_index_ = max_score_q_index
        self.max_score_c_index_ = max_score_c_index


class FileResult:
    def __init__(self, problem, model, dataset, provider, similarity_mode, glossary):
        self.model_ = model
        self.dataset_ = dataset
        self.provider_ = provider
        self.similarity_mode_ = similarity_mode
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
            q_keyword = comparison['q_keyword']
            q_gloss_keyword = comparison['q_gloss_keyword']
            q_source = comparison['source']
            choice_comparisons = []
            for c_comp in comparison['c_comparisons']:
                c_comp_options = []
                for c_comp_option in c_comp:
                    c_def = c_comp_option['c_def']
                    c_keyword = c_comp_option['c_keyword']
                    c_gloss_keyword = c_comp_option['c_gloss_keyword']
                    c_source = c_comp_option['source']
                    score = self.format_score(c_comp_option['score'])
                    c_comp_options.append(Comparison(q_def, q_source, q_keyword, q_gloss_keyword, c_def,
                                                     c_source, c_keyword, c_gloss_keyword, score))
                choice_comparisons.append(c_comp_options)
            result.append(choice_comparisons)
        return result

    def format_score(self, score):
        return "%0.5f" % score


class Problem:
    def __init__(self, id, fullname, model, category, problem, dataset, provider, similarity_mode, glossary):
        self.id_ = id
        self.category_ = category
        self.question_ = problem['question']
        self.correct_answer_ = problem['real_answer']
        self.file_results_ = {}
        self.add_file_result(fullname, model, problem, dataset, provider, similarity_mode, glossary)

    def add_file_result(self, fullname, model, problem, dataset, provider, similarity_mode, glossary):
        self.file_results_[fullname] = FileResult(problem, model, dataset, provider, similarity_mode, glossary)

    def get_file_result(self, filename):
        if filename not in self.file_results_:
            return None
        return self.file_results_[filename]

    def get_comparisons(self, filename):
        return self.file_results_[filename].comparisons_

    def get_choice_max_score_indexes(self, comparisons, i_choice):
        max_score = 0
        max_q_index = 0
        max_c_index = 0
        for i_q_comp, q_comparison in enumerate(comparisons):
            c_comparisons = q_comparison[i_choice]
            for i_c_comp, c_comparison in enumerate(c_comparisons):
                cur_score = float(c_comparison.score_)
                if cur_score > max_score:
                    max_score = cur_score
                    max_q_index = i_q_comp
                    max_c_index = i_c_comp
        return max_q_index, max_c_index

    def get_comparison_results(self, files):
        first_file = list(self.file_results_.keys())[0]
        choices = self.file_results_[first_file].choices_
        comp_results = []
        for i_choice, choice in enumerate(choices):
            c_ordinal = chr(i_choice + ord('A'))
            for i_file, file in enumerate(files):
                file_result = self.get_file_result(file)
                q_options = list(range(len(file_result.comparisons_)))
                max_score_q_index, max_score_c_index = self.get_choice_max_score_indexes(file_result.comparisons_, i_choice)
                q_comparisons = file_result.comparisons_[max_score_q_index]
                c_comparisons = q_comparisons[i_choice]
                c_options = list(range(len(c_comparisons)))
                o_comp = c_comparisons[max_score_c_index]
                res = ComparisonResult(o_comp, c_options, c_ordinal, i_file, i_choice, q_options, file, max_score_q_index, max_score_c_index)
                comp_results.append(res)
        return comp_results

    def get_choices(self):
        first_file = list(self.file_results_.keys())[0]
        return self.file_results_[first_file].choices_

    def has_file(self, filename):
        return filename in self.file_results_

    def add_file(self, filename, model, problem, dataset, provider, similarity_mode, glossary):
        if self.has_file(filename):
            print("Warning when loading data => Found the question '%s' twice for the same filename %s" % (self.id_, filename))
            return
        self.add_file_result(filename, model, problem, dataset, provider, similarity_mode, glossary)

    def get_file_result_success(self, file_result):
        if file_result.success_:
            return 'static/img/success.png'
        return 'static/img/failure.png'

    def get_success_indicator(self, files):
        file1_result = self.get_file_result(files[0])
        if len(files) > 1:
            file2_result = self.get_file_result(files[1])
            if file2_result is None:
                return self.get_file_result_success(file1_result)
            if file1_result.success_ != file2_result.success_:
                if file1_result.success_:
                    return 'static/img/left_ok_right_ko.png'
                return 'static/img/left_ko_right_ok.png'
        return self.get_file_result_success(file1_result)
