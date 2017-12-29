from problems_reader import OldProblemsReader, Problems2016Reader, NewProblemsReader
from problems_enriching import ProblemsEnricher
from problems_writer import ProblemsWriter


old_questions_reader = OldProblemsReader()
old_paths, old_problems_df = old_questions_reader.get_problems()

reader_2016 = Problems2016Reader()
morning_2016_path, problems_2016_morning_df = reader_2016.get_problems('morning')
afternoon_2016_path, problems_2016_afternoon_df = reader_2016.get_problems('afternoon')

new_questions_reader = NewProblemsReader()
new_paths, new_problems_df = new_questions_reader.get_problems()

all_paths = old_paths + [morning_2016_path, afternoon_2016_path] + new_paths
all_dfs = old_problems_df + [problems_2016_morning_df, problems_2016_afternoon_df] + new_problems_df

transformer = ProblemsEnricher()
transformer.enrich(all_paths, all_dfs)

writer = ProblemsWriter()
writer.write_problems(all_dfs)
