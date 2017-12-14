import io
import os.path
import re
from google.cloud import vision


class Problem:
    def __init__(self):
        self.question_ = ""
        self.choices_ = []
        self.answer_ = ""
        self.comments_ = ""

    def set_question(self, question):
        self.question_ = question

    def add_choice(self, choice):
        self.choices_.append(choice)

    def set_answer(self, answer):
        self.answer_ = answer

    def set_comments(self, comments):
        self.comments_ = comments


class ParsingMode(object):
    NONE = 0
    QUESTION = 1
    CHOICES = 2
    ANSWER = 3
    COMMENTS = 4


class LastWordsXPositions:
    def __init__(self, capacity):
        self.capacity_ = capacity
        self.last_x_positions_ = []

    def add_x_position(self, x_new_pos):
        current_len = len(self.last_x_positions_)
        if current_len == self.capacity_:
            self.last_x_positions_.pop(0)
        self.last_x_positions_.append(x_new_pos)

    def get_positions(self):
        return self.last_x_positions_


class ParsingContext:
    SENTENCE_ENDINGS = ['?', ',', '.', ';', ':', '!']
    CHOICES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    def __init__(self):
        self.problems_ = []
        self.current_problem_ = None
        self.current_full_text_array_ = []
        self.current_word_array_ = []
        self.mode_ = ParsingMode.NONE
        self.last_character_ = ''
        self.current_full_word_ = ''
        self.last_full_word_ = ''
        self.previous_indicator_ = ''
        self.last_3_words_x_start_pos_ = LastWordsXPositions(3)

    def start_new_problem(self):
        if self.current_problem_ is not None:
            self.end_comments()
            self.problems_.append(self.current_problem_)
        self.current_problem_ = Problem()
        self.mode_ = ParsingMode.QUESTION

    def start_new_choice(self):
        # We don't take the last 2 words because they have already been parsed but represent the words '[A-D]' and '.'
        # used to detect the beginning of the choices section
        current_indicator = self.get_current_text(minus_at_the_end=3, use_minus_for_start=True).replace(' ', '')
        current_text = self.pop_current_text(minus_at_the_end=3).strip()
        if self.mode_ == ParsingMode.QUESTION:
            self.current_problem_.set_question(current_text)
            self.mode_ = ParsingMode.CHOICES
        else:
            self.current_problem_.add_choice(self.previous_indicator_ + ' ' + current_text)
        self.previous_indicator_ = current_indicator

    def end_choices(self):
        choice_text = self.pop_current_text()
        self.current_problem_.add_choice(self.previous_indicator_ + ' ' + choice_text)
        self.mode_ = ParsingMode.ANSWER

    def end_answer(self):
        answer = self.pop_current_text()
        self.current_problem_.set_answer(answer.strip())
        self.mode_ = ParsingMode.COMMENTS

    def end_comments(self):
        comments = self.pop_current_text(minus_at_the_end=3)
        self.current_problem_.set_comments(comments.strip())
        self.mode_ = ParsingMode.NONE

    def end_word(self, word):
        self.last_full_word_ = self.current_full_word_
        self.current_full_word_ = ''.join(self.current_word_array_)
        self.current_word_array_ = []
        self.current_full_text_array_.append(self.current_full_word_)
        self.last_3_words_x_start_pos_.add_x_position(word.bounding_box.vertices[0].x)

    def get_current_text(self, minus_at_the_end=0, use_minus_for_start=False):
        length = len(self.current_full_text_array_)
        start_index = 0
        end_index = length
        if use_minus_for_start:
            start_index = length - minus_at_the_end
        else:
            end_index = length - minus_at_the_end
        return ''.join(self.current_full_text_array_[start_index:end_index])

    def pop_current_text(self, minus_at_the_end=0):
        text = self.get_current_text(minus_at_the_end)
        self.current_full_text_array_ = []
        return text

    def add_word_separator(self):
        self.current_full_text_array_.append(' ')

    def add_line_separator(self):
        self.current_full_text_array_.append('\n')

    def add_symbol(self, symbol):
        self.last_character_ = symbol.text
        self.current_word_array_.append(symbol.text)

    def is_in_mode(self, mode):
        return self.mode_ == mode

    def current_word_is_dot(self):
        return self.current_full_word_ == '.'

    def currently_ending_a_sentence(self):
        return self.last_character_ in self.SENTENCE_ENDINGS

    def last_word_is_a_number(self):
        return re.match("^\d+$", self.last_full_word_) is not None

    def last_word_is_a_choice(self):
        return self.last_full_word_ in self.CHOICES

    def last_word_was_on_a_new_line(self):
        # Last word was written on a new line if the x position of the word
        # before the last one was superior to the x position of the last word
        last3_x_pos = self.last_3_words_x_start_pos_.get_positions()
        if len(last3_x_pos) < 2:
            return False
        previous_last_x_pos = last3_x_pos[0]
        last_x_pos = last3_x_pos[1]
        return previous_last_x_pos > last_x_pos

    def get_problems(self):
        return self.problems_


class CfaProblemsBuilder:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/abiarnes/Documents/Lessons/Fil_Rouge/CfaBot/Keys/CfaBot-ServiceKey-Adrien.json"
        self.client_ = vision.ImageAnnotatorClient()
        self.context_ = ParsingContext()

    def build_problems(self, image_path):
        request = {
            'image': {'content': self.load_image(image_path)},
            'features': [{'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
        }
        response = self.client_.annotate_image(request)
        self.parse_annotations(response.full_text_annotation)
        return self.context_.get_problems()

    @staticmethod
    def load_image(path):
        with io.open(path, 'rb') as image_file:
            return image_file.read()

    def parse_annotations(self, annotations):
        blocks = annotations.pages[0].blocks
        for block in blocks:
            self.parse_paragraph(block.paragraphs)

    def parse_paragraph(self, paragraphs):
        for paragraph in paragraphs:
            self.parse_words(paragraph.words)
        if self.context_.is_in_mode(ParsingMode.ANSWER):
            self.context_.end_answer()
        if self.context_.is_in_mode(ParsingMode.CHOICES):
            self.context_.end_choices()

    def parse_words(self, words):
        for word in words:
            self.parse_word(word)
            if self.context_.current_word_is_dot() and \
               self.context_.last_word_was_on_a_new_line():
                if self.context_.last_word_is_a_number():
                    self.context_.start_new_problem()
                elif self.context_.last_word_is_a_choice():
                    self.context_.start_new_choice()
            elif not self.context_.currently_ending_a_sentence():
                self.context_.add_word_separator()
        self.context_.add_line_separator()

    def parse_word(self, word):
        for symbol in word.symbols:
            self.context_.add_symbol(symbol)
        self.context_.end_word(word)


builder = CfaProblemsBuilder()
image_path = os.path.join('Data', 'qa_mock_exams', '2014', '2014_afternoon', '2014_afternoon_answer 3.jpeg')
problems = builder.build_problems(image_path)
pass
