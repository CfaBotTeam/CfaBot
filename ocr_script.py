from ocr_helpers import FilePathResolver, ProblemsWriter
from ocr_google_client import CfaProblemsBuilder
from ocr_google_client_2016 import ParserTwoThousandSixteenAnswers, ParserTwoThousandSixteenQuestions


def resolve_build_and_write(year, day_part, file_part, nb_blocks_footer=0, nb_words_footer=0, headers=None, skip_nb_page=0, parser=None, indentation_threshold=15):
    resolver = FilePathResolver(year, day_part, file_part)
    jpeg_filepaths = resolver.resolve_sorted_paths()
    jpeg_filepaths = jpeg_filepaths[skip_nb_page:]

    builder = CfaProblemsBuilder(parser=parser, headers=headers, nb_blocks_footer=nb_blocks_footer, nb_words_footer=nb_words_footer, indentation_threshold=indentation_threshold)
    problems = builder.build_problems(jpeg_filepaths)

    writer = ProblemsWriter()
    writer.write_problems(resolver.get_xml_result_file(), problems)


# 2014 afternoon
headers = ["7476229133318632 March Mock Exam - PM March Mock Exam - PM 399388"]
resolve_build_and_write('2014', 'afternoon', 'answer', nb_blocks_footer=1, headers=headers, indentation_threshold=25)

# 2014 morning
# base_header = '3172168919041893 March Mock Exam - AM 399388'
# headers = ["|" + base_header, base_header]
# resolve_build_and_write('2014', 'morning', 'answer', nb_blocks_footer=1, headers=headers)

# 2015 afternoon
# headers = ['2015 Level I Mock Exam PM Questions and Answers']
# resolve_build_and_write('2015', 'afternoon', 'answer', nb_blocks_footer=1, headers=headers)

# 2015 morning
# headers = ['2015 Level I Mock Exam AM Questions and Answers']
# resolve_build_and_write('2015', 'morning', 'answer', nb_blocks_footer=1, headers=headers)

# 2017 afternoon
# resolve_build_and_write('2017', 'morning', 'answer', skip_nb_page=1, nb_blocks_footer=2)

# 2017 afternoon
# resolve_build_and_write('2017', 'afternoon', 'answer', skip_nb_page=1, nb_blocks_footer=2)

# 2016 afternoon answer
# headers = ['CFA level1-Mock-114']
# parser = ParserTwoThousandSixteenAnswers()
# resolve_build_and_write('2016', 'afternoon_answer', '', skip_nb_page=1, headers=headers, nb_words_footer=3, parser=parser)

# 2016 afternoon questions
# headers = ['CFA level1-Mock-114', 'CFA levell-Mock-114']
# parser = ParserTwoThousandSixteenQuestions()
# resolve_build_and_write('2016', 'afternoon_question', '', skip_nb_page=1, headers=headers, nb_words_footer=3, parser=parser)
#
# 2016 morning answer
# headers = ['CFA level1-Mock-113']
# parser = ParserTwoThousandSixteenAnswers()
# resolve_build_and_write('2016', 'morning_answer', '', skip_nb_page=1, headers=headers, nb_words_footer=3, parser=parser)

# 2016 afternoon questions
# headers = ['CFA level1-Mock-113', 'CFA levell-Mock-113']
# parser = ParserTwoThousandSixteenQuestions()
# resolve_build_and_write('2016', 'morning_question', '', skip_nb_page=1, headers=headers, nb_words_footer=3, parser=parser)
