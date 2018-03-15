from ocr_google_client import Problem, ParsingMode, BaseParser, ParsingContext


class ParsingContextTwoThousandSixteenAnswers(ParsingContext):
    def start_answer(self):
        self.end_problem(2)
        self.current_problem_ = Problem()
        self.mode_ = ParsingMode.ANSWER

    def end_answer(self):
        self.previous_indicator_ = self.get_current_text(minus_at_the_end=1, use_minus_for_start=True)
        answer = self.pop_current_text(minus_at_the_end=1)
        self.current_problem_.set_answer(answer.strip())
        self.mode_ = ParsingMode.COMMENTS


class ParserTwoThousandSixteenAnswers(BaseParser):
    def __init__(self, indentation_threshold):
        super().__init__(ParsingContextTwoThousandSixteenAnswers(indentation_threshold))

    def check_answer_end(self):
        if self.context_.is_in_mode(ParsingMode.ANSWER) and \
           self.context_.current_word_was_on_a_new_line():
            self.context_.end_answer()

    def parse_words(self, blocks_iter):
        for word in blocks_iter:
            self.parse_word(word)
            self.check_answer_end()
            if self.context_.current_word_is_dot() and \
               self.context_.last_word_was_on_a_new_line() and \
               self.context_.last_word_is_a_number():
                self.context_.start_answer()
            self.try_add_word_separator(word)


class ParsingContextTwoThousandSixteenQuestions(ParsingContext):
    def end_problem(self):
        if self.current_problem_ is None or \
           self.current_problem_.is_empty():
            return
        self.end_choices()
        self.problems_.append(self.current_problem_)

    def end_choices(self):
        current_indicator = self.get_current_text(minus_at_the_end=2, use_minus_for_start=True)
        choice_text = self.pop_current_text(minus_at_the_end=2)
        self.current_problem_.add_choice(self.join_sentences(self.previous_indicator_, choice_text))
        self.previous_indicator_ = current_indicator

    def start_new_choice(self):
        # We don't take the last 2 words because they have already been parsed but represent the words '[A-D]' and '.'
        # used to detect the beginning of the choices section
        current_indicator = self.get_current_text(minus_at_the_end=2, use_minus_for_start=True)
        current_text = self.pop_current_text(minus_at_the_end=2).strip()
        if self.mode_ == ParsingMode.QUESTION:
            question = current_text
            if len(self.previous_indicator_) > 0:
                question = self.join_sentences(self.previous_indicator_, question)
            self.current_problem_.set_question(question)
            self.mode_ = ParsingMode.CHOICES
        else:
            self.current_problem_.add_choice(self.join_sentences(self.previous_indicator_, current_text))
        self.previous_indicator_ = current_indicator

    def start_question(self):
        self.end_problem()
        self.current_problem_ = Problem()
        self.mode_ = ParsingMode.QUESTION


class ParserTwoThousandSixteenQuestions(BaseParser):
    def __init__(self, indentation_threshold):
        super().__init__(ParsingContextTwoThousandSixteenQuestions(indentation_threshold))

    def parse_words(self, blocks_iter):
        for word in blocks_iter:
            self.parse_word(word)
            # if self.context_.currently_ending_a_sentence():
            #     self.context_.remove_previous_word_separator()
            if self.context_.current_word_is_dot() and \
               self.context_.last_word_was_on_a_new_line():
                if self.context_.last_word_is_a_number():
                    self.context_.start_question()
                elif self.context_.last_word_is_a_choice():
                    self.context_.start_new_choice()
            self.try_add_word_separator(word)