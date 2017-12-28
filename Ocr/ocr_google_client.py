import io
import os.path
import re
from google.cloud import vision
from google.cloud.vision import enums
import math
import more_itertools as mit


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

    def is_empty(self):
        return self.question_ == '' and self.answer_ == ''


class ParsingMode(object):
    NONE = 0
    HEADER = 1
    QUESTION = 2
    CHOICES = 3
    ANSWER = 4
    COMMENTS = 5


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

    def __init__(self, indentation_threshold):
        self.problems_ = []
        self.current_problem_ = None
        self.current_full_text_array_ = []
        self.current_word_array_ = []
        self.previous_mode_ = ParsingMode.NONE
        self.mode_ = ParsingMode.NONE
        self.last_character_ = ''
        self.current_full_word_ = ''
        self.last_full_word_ = ''
        self.previous_indicator_ = ''
        self.headers_ = None
        self.previous_page_text_array_ = []
        self.header_set_ = False
        self.last_new_line_x = 0
        self.current_new_line_x = 0
        self.last_3_words_x_start_pos_ = LastWordsXPositions(3)
        self.indentation_threshold_ = indentation_threshold
        self.previous_word_image_index_ = -1
        self.current_word_image_index_ = -1
        self.current_image_index_ = -1

    def end_problem(self, nb_lookup=0, with_comments=True):
        if self.current_problem_ is None or \
           self.current_problem_.is_empty():
            return
        if with_comments:
            self.end_comments(nb_lookup)
        else:
            self.current_problem_.set_comments("")
        self.problems_.append(self.current_problem_)

    def start_new_problem(self, nb_lookup, end_previous_comments=True):
        self.end_problem(nb_lookup, with_comments=end_previous_comments)
        self.current_problem_ = Problem()
        self.mode_ = ParsingMode.QUESTION

    def join_sentences(self, sentence1, sentence2):
        sentence1 = sentence1.strip()
        sentence2 = sentence2.strip()
        if len(sentence2) == 0:
            return sentence1
        first_character = sentence2[0]
        if first_character in self.SENTENCE_ENDINGS:
            return sentence1 + sentence2
        return sentence1 + " " + sentence2

    def start_new_choice(self):
        # We don't take the last 2 words because they have already been parsed but represent the words '[A-D]' and '.'
        # used to detect the beginning of the choices section
        current_indicator = self.get_current_text(minus_at_the_end=2, use_minus_for_start=True)
        current_text = self.pop_current_text(minus_at_the_end=2).strip()
        if self.mode_ < ParsingMode.QUESTION:
            # Should not happen but sometimes the stupid OCR does not recognises question start
            self.start_new_problem(nb_lookup=0, end_previous_comments=False)
        if self.mode_ == ParsingMode.QUESTION:
            question = current_text
            if len(self.previous_indicator_) > 0:
                question = self.join_sentences(self.previous_indicator_, question)
            self.current_problem_.set_question(question)
            self.mode_ = ParsingMode.CHOICES
        else:
            self.current_problem_.add_choice(self.join_sentences(self.previous_indicator_, current_text))
        self.previous_indicator_ = current_indicator

    def end_choices(self):
        # We don't take the Answer keyword
        choice_text = self.pop_current_text(minus_at_the_end=1)
        self.current_problem_.add_choice(self.join_sentences(self.previous_indicator_, choice_text))
        self.mode_ = ParsingMode.ANSWER

    def end_answer(self):
        self.previous_indicator_ = self.get_current_text(minus_at_the_end=1, use_minus_for_start=True)
        answer = self.pop_current_text(minus_at_the_end=1).lstrip('= ')
        self.current_problem_.set_answer(answer.strip())
        self.mode_ = ParsingMode.COMMENTS

    def end_comments(self, nb_lookup):
        current_indicator = self.get_current_text(minus_at_the_end=nb_lookup, use_minus_for_start=True)
        comments = self.pop_current_text(minus_at_the_end=nb_lookup)
        self.current_problem_.set_comments(self.join_sentences(self.previous_indicator_, comments.strip()))
        self.mode_ = ParsingMode.NONE
        self.previous_indicator_ = current_indicator

    def end_word(self, word):
        self.last_full_word_ = self.current_full_word_
        self.current_full_word_ = ''.join(self.current_word_array_)
        self.current_word_array_ = []
        self.current_full_text_array_.append(self.current_full_word_)
        start_x = word.bounding_box.vertices[0].x
        self.last_3_words_x_start_pos_.add_x_position(start_x)
        if self.current_word_was_on_a_new_line():
            self.last_new_line_x = self.current_new_line_x
            self.current_new_line_x = start_x
        if self.mode_ != ParsingMode.HEADER:
            # when in header mode we don't want to save the word image index
            self.previous_word_image_index_ = self.current_word_image_index_
            self.current_word_image_index_ = self.current_image_index_

    def start_new_image(self):
        self.current_image_index_ += 1
        if self.headers_ is None:
            return
        # When in header mode we need to:
        # 1) save the current text
        # 2) Remove the header
        # 3) Restore the text
        # Here we proceed step 1
        self.save_current_text()
        self.pop_current_text()
        self.mode_ = ParsingMode.HEADER

    def new_line_indentation_has_changed(self):
        if not self.current_word_was_on_a_new_line():
            return False
        if self.current_word_image_index_ != self.previous_word_image_index_:
            return False
        return math.fabs(self.last_new_line_x - self.current_new_line_x) > self.indentation_threshold_

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

    def save_current_text(self):
        self.previous_mode_ = self.mode_
        self.previous_page_text_array_ = list(self.current_full_text_array_)

    def restore_previous_text(self):
        self.mode_ = self.previous_mode_
        self.current_full_text_array_ = list(self.previous_page_text_array_)

    def add_word_separator(self):
        self.current_full_text_array_.append(' ')

    def add_line_separator(self):
        self.current_full_text_array_.append('\n')

    def add_symbol(self, symbol):
        self.last_character_ = symbol.text
        self.current_word_array_.append(symbol.text)

    def is_in_mode(self, mode):
        return self.mode_ == mode

    def set_mode(self, mode):
        self.mode_ = mode

    def current_word_is_dot(self):
        return self.current_full_word_ == '.'

    def currently_ending_a_sentence(self):
        return self.last_character_ in self.SENTENCE_ENDINGS

    def remove_previous_word_separator(self):
        length = len(self.current_full_text_array_)
        if length >= 2 and self.current_full_text_array_[length - 2] == ' ':
            self.current_full_text_array_.pop(length - 2)

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

    def current_word_was_on_a_new_line(self):
        # Current word was written on a new line if it's x position
        # is inferior to previous word's x position
        last3_x_pos = self.last_3_words_x_start_pos_.get_positions()
        if len(last3_x_pos) < 2:
            return False
        current_x_pos = last3_x_pos[len(last3_x_pos) - 1]
        last_x_pos = last3_x_pos[len(last3_x_pos) - 2]
        return current_x_pos < last_x_pos

    def current_word_equals(self, word):
        return self.current_full_word_ == word

    def set_headers(self, headers):
        self.headers_ = [h.replace(' ', '') for h in headers]

    def header_set(self):
        current_text = self.get_current_text().replace(' ', '')
        return current_text in self.headers_

    def get_problems(self):
        return self.problems_


class CfaProblemsBuilder:
    def __init__(self, parser=None, headers=None, nb_blocks_footer=0, nb_words_footer=0, indentation_threshold=15):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/abiarnes/Documents/Lessons/Fil_Rouge/CfaBot/Keys/CfaBot-ServiceKey-Adrien.json"
        self.parser_ = parser if parser is not None else CommonParser(indentation_threshold)
        self.client_ = vision.ImageAnnotatorClient()
        self.context_ = self.parser_.get_context()
        if headers is not None:
            self.context_.set_headers(headers)
        self.nb_blocks_footer_ = nb_blocks_footer
        self.nb_words_footer_ = nb_words_footer
        self.current_image_path_ = ''

    @staticmethod
    def load_image(path):
        with io.open(path, 'rb') as image_file:
            return image_file.read()

    def build_problems(self, filepaths):
        start = 0
        end = len(filepaths)
        while start < end:
            temp_end = start + 5
            if temp_end > end:
                temp_end = end
            problems = self.build_problems_internal_(filepaths[start:temp_end], temp_end == end)
            start = temp_end
        return problems

    def build_problems_internal_(self, image_paths, last_call):
        requests = []
        for image_path in image_paths:
            requests.append({
                'image': {'content': self.load_image(image_path)},
                'features': [{'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
            })
        response = self.client_.batch_annotate_images(requests)
        self.parse_responses(zip(response.responses, image_paths))
        if last_call:
            self.context_.end_problem()
        return self.context_.get_problems()

    def parse_responses(self, responses):
        for response, image_path in responses:
            self.current_image_path_ = image_path
            self.context_.start_new_image()
            self.parse_annotations(response.full_text_annotation)

    def is_weird_case_of_question_number_not_ordered(self, page):
        # Sometimes, the question number is returned by the OCR as the first block
        # where the first block should always be the header
        # In such a case we ignore the first block
        first_block_y = page.blocks[0].paragraphs[0].words[0].symbols[0].bounding_box.vertices[0].y
        next_block_y = page.blocks[1].paragraphs[0].words[0].symbols[0].bounding_box.vertices[0].y
        if first_block_y <= next_block_y:
            return False
        text = ''
        first_word = page.blocks[0].paragraphs[0].words[0]
        for symbol in first_word.symbols:
            text += symbol.text
        if re.match("^\d+$", text) is None:
            raise Exception('Case not handled yet in ' + self.current_image_path_ + ", text = " + text)
        return True

    def handle_special_question_case(self, page):
        #if not self.is_weird_case_of_question_number_not_ordered(page):
        return 0, False
        #return 1, True

    def parse_annotations(self, annotations):
        for page in annotations.pages:
            block_start, should_start_problem = self.handle_special_question_case(page)
            blocks_iter = self.get_page_iterator(block_start, page)
            if self.context_.is_in_mode(ParsingMode.HEADER):
                self.parser_.parse_header(blocks_iter)
            if should_start_problem:
                self.context_.start_new_problem(0)
            self.parser_.parse_words(blocks_iter)

    def get_page_iterator(self, block_start, page):
        # we always skip the last blocks of the page which corresponds to the footer
        blocks = page.blocks[block_start:len(page.blocks) - self.nb_blocks_footer_]
        iterator = iter(self.get_next_word_from_blocks(blocks))
        if self.nb_words_footer_ != 0:
            return mit.islice_extended(iterator, None, -self.nb_words_footer_)
        return iterator

    def get_next_word_from_blocks(self, blocks):
        for block in blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    yield word


class BaseParser:
    def __init__(self, context):
        self.context_ = context

    def get_context(self):
        return self.context_

    def parse_header(self, blocks_iter):
        for word in blocks_iter:
            self.parse_word(word)
            if self.context_.header_set():
                self.context_.pop_current_text()
                self.context_.restore_previous_text()
                break
            self.try_add_word_separator(word)

    def try_add_word_separator(self, word):
        break_type = word.symbols[-1].property.detected_break.type
        if break_type != enums.TextAnnotation.DetectedBreak.BreakType.UNKNOWN:
            self.context_.add_word_separator()

    def parse_word(self, word):
        for symbol in word.symbols:
            self.context_.add_symbol(symbol)
        self.context_.end_word(word)


class CommonParser(BaseParser):
    def __init__(self, indentation_threshold):
        super().__init__(ParsingContext(indentation_threshold))

    def check_answer_end(self):
        if self.context_.is_in_mode(ParsingMode.ANSWER) and \
           self.context_.current_word_was_on_a_new_line():
            self.context_.end_answer()

    def check_choices_end(self):
        if self.context_.is_in_mode(ParsingMode.CHOICES) and \
           self.context_.current_word_was_on_a_new_line() and \
           self.context_.current_word_equals("Answer"):
            self.context_.end_choices()

    def check_comment_end(self):
        if self.context_.is_in_mode(ParsingMode.COMMENTS) and \
           self.context_.new_line_indentation_has_changed():
            self.context_.start_new_problem(1)

    def parse_words(self, blocks_iter):
        for word in blocks_iter:
            self.parse_word(word)
            self.check_answer_end()
            self.check_choices_end()
            self.check_comment_end()
            if self.context_.current_word_is_dot() and \
               self.context_.last_word_was_on_a_new_line():
                if not self.context_.is_in_mode(ParsingMode.QUESTION) and \
                   self.context_.last_word_is_a_number():
                    self.context_.start_new_problem(2)
                elif self.context_.last_word_is_a_choice():
                    self.context_.start_new_choice()
            self.try_add_word_separator(word)

