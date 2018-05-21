
class ProblemCategory(object):
    # The subject of the question is the definition and
    # the choices contain the potential technical term associated to it
    DEF_KEYWORD = 0
    # The subject of the question is the definition and
    # the rest of the question contains the beginning of the technical term
    # and the choices contain the potential end of the technical term
    DEF_KEYWORD_START_END = 1

    # The subject of the question is a technical term or very close to it and
    # the proposed choices are the potential definitions of the technical term
    KEYWORD_DEF = 2
    # The subject of the question is a technical term or very close to it and
    # the rest of the question contains the beginning or a good part of the definition and
    # the choices contain the end of the definition
    KEYWORD_DEF_START_END = 3

    # The subject of the question is a characteristic and
    # the proposed choices are the potential technical terms exposing this characteristic
    CHAR_KEYWORD = 4
    # The subject of the question is a technical term and
    # the proposed choices are the potential characteristics associated with this characteristic
    KEYWORD_CHAR = 5

    CONTEXT_KEYWORD_CHAR = 6

    # The question is quite complex. The subject of the description refers to a previous sentence in the question
    SITUATION_KEYWORD = 7

    # Very hard
    KEYWORD_COMPARISON = 8
    CALCULUS = 9
    REASONING = 10
    BEST_ASSOCIATION = 11

    # Will probably never care
    OCR_PROBLEM = 20

    # For the situational questions regarding the standards topic
    SCENARIO = 30

    UNLABELED = 666