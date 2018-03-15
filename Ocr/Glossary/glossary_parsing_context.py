import math


class ParsingMode(object):
    KEYWORD = 1
    DEFINITION = 2


class GlossaryParsingContext:
    INDENTATION_THRESHOLD = 18

    def __init__(self):
        self.glossary_ = {}
        self.words_array_ = []
        self.characters_array_ = []
        self.current_keyword_ = ''
        self.current_mode_ = ParsingMode.KEYWORD
        self.last_word_end_x_ = 99999999
        self.last_word_end_y_ = 0

    def clear_words_array(self):
        pending = ''.join(self.words_array_)
        self.words_array_ = []
        return pending

    def end_word(self, word):
        full_word = ''.join(self.characters_array_)
        self.words_array_.append(full_word)
        self.characters_array_ = []
        end_x = word.bounding_box.vertices[1].x
        end_y = word.bounding_box.vertices[1].y
        self.last_word_end_x_ = end_x
        self.last_word_end_y_ = end_y

    def end_keyword(self):
        self.current_keyword_ = self.clear_words_array()
        self.current_mode_ = ParsingMode.DEFINITION

    def end_definition(self):
        definition = self.clear_words_array()
        self.glossary_[self.current_keyword_] = definition
        self.current_keyword_ = ''
        self.current_mode_ = ParsingMode.KEYWORD

    def add_word_separator(self):
        self.words_array_.append(' ')

    def add_line_separator(self):
        self.words_array_.append('\n')

    def add_symbol(self, symbol):
        self.characters_array_.append(symbol.text)

    def word_is_dot(self):
        return self.words_array_[-1] == '.'

    def is_in_mode(self, mode):
        return self.current_mode_ == mode

    def new_word_indented(self, new_word):
        start_x = new_word.bounding_box.vertices[0].x
        start_y = new_word.bounding_box.vertices[0].y
        return start_x - self.last_word_end_x_ > self.INDENTATION_THRESHOLD and \
                abs(start_y - self.last_word_end_y_) <= 10
