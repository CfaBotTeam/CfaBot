from Ocr.Glossary.glossary_parsing_context import ParsingMode
from Ocr.Glossary.glossary_parsing_context import GlossaryParsingContext
from google.cloud.vision import enums


class GlossaryParser:
    def __init__(self):
        self.context_ = GlossaryParsingContext()

    def get_glossary(self):
        return self.context_.glossary_

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

    def check_keyword_end(self, new_word):
        if self.context_.is_in_mode(ParsingMode.KEYWORD) and \
            self.context_.new_word_indented(new_word):
            self.context_.end_keyword()

    def check_definition_end(self, word):
        break_type = word.symbols[-1].property.detected_break.type
        if break_type > enums.TextAnnotation.DetectedBreak.BreakType.SURE_SPACE and \
            self.context_.word_is_dot():
            self.context_.end_definition()

    def parse_words(self, blocks_iter):
        for word in blocks_iter:
            self.check_keyword_end(word)
            self.parse_word(word)
            self.check_definition_end(word)
            self.try_add_word_separator(word)
