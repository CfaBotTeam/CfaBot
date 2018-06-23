import spacy
from spacy.tokenizer import Tokenizer


class SpacyLoader:
    # def create_custom_tokenizer(self, nlp):
    #     all_prefixes_re = spacy.util.compile_prefix_regex(nlp.Defaults.prefixes)
    #     infixes = ['\\.\\.+',
    #                '…',
    #                '[\\p{So}]',
    #                '(?<=[0-9])[+\\-\\*^](?=[0-9-])',
    #                '(?<=[[[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]])\\.(?=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]])',
    #                '(?<=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]]),(?=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]])',
    #                '(?<=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]])[?";:=,.]*(?:--|---|——|~)(?=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]])',
    #                '(?<=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]"])[:<>=/](?=[[[\\p{Lu}&&\\p{Latin}]||[ЁА-Я]||[\\p{Ll}&&\\p{Latin}]||[ёа-я]||[\\p{L}&&\\p{Bengali}]||[\\p{L}&&\\p{Hebrew}]||[\\p{L}&&\\p{Arabic}]]])']
    #     infix_re = spacy.util.compile_infix_regex(tuple(infixes))
    #     suffix_re = spacy.util.compile_suffix_regex(nlp.Defaults.suffixes)
    #
    #     return Tokenizer(nlp.vocab, nlp.Defaults.tokenizer_exceptions,
    #                      prefix_search=all_prefixes_re.search,
    #                      infix_finditer=infix_re.finditer, suffix_search=suffix_re.search,
    #                      token_match=None)

    def load_nlp(self, model_path, disable=None):
        dis = ['tagger', 'textcat'] if disable is None else disable
        nlp = spacy.load(model_path, disable=dis)
        # nlp.tokenizer = self.create_custom_tokenizer(nlp)
        return nlp
