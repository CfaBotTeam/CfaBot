import xml.etree.ElementTree as ET
import pandas as pd
from glob import glob
import os.path as op
import re
import xml.dom.minidom
from problems_enriching import ProblemsEnricher


class ProblemsReader:
    def read_file(self, path):
        return self.read_files([path])[0]

    def get_filepaths_from_years(self, years):
        paths = []
        for year in years:
            year_paths = sorted(glob(op.join('..', 'Data', 'qa_mock_exams', str(year), '*.xml')))
            for path in year_paths:
                paths.append(path)
        return paths

    def read_files(self, paths):
        dfs = []
        for path in paths:
            try:
                records = self.get_records(path)
                dfs.append(pd.DataFrame(records))
            except Exception as e:
                print("Exception in file '{}': {}".format(path, e))
        return dfs

    def add_choice(self, choice, record):
        id = choice.attrib['id']
        record[choice.tag + '_' + id] = choice.text

    def get_records(self, path):
        records = []
        xml_data = open(path, encoding="utf8").read()
        nodes = ET.XML(xml_data)
        for node in nodes:
            if node.tag != 'problem':
                continue
            record = {}
            for child in node:
                if child.tag == "choices":
                    for choice in child:
                        self.add_choice(choice, record)
                else:
                    record[child.tag] = child.text
            records.append(record)
        return records

    def extract_question_number(self, question):
        match = re.match('^(\d+)\. (.*)$', question)
        return match.group(1)

    def extract_question(self, question):
        match = re.match('^(\d+)\. (.*)$', question)
        return match.group(2)

    def extract_choice(self, choice):
        match = re.match('^([ABC]). (.*)$', choice)
        return match.group(1), match.group(2)


class OldProblemsReader(ProblemsReader):
    def get_problems(self):
        years = list(range(2008, 2014))
        paths = self.get_filepaths_from_years(years)
        return paths, self.read_files(paths)


class NewProblemsReader(ProblemsReader):
    def add_choice(self, choice, record):
        # We override add choice to handle special file format
        id, text = self.extract_choice(choice.text)
        record[choice.tag + '_' + id] = text

    def get_problems(self):
        years = list(range(2014, 2016))
        years.append(2017)
        paths = self.get_filepaths_from_years(years)
        return paths, self.read_files(paths)


class Problems2016Reader(NewProblemsReader):
    def extract_2016_answer(self, answer):
        match = re.match('^\d+. .*([ABC]).?$', answer)
        return match.group(1)

    def merge_2016_df(self, questions_df, answers_df):
        merged_2016 = questions_df.copy()
        merged_2016['answer'] = answers_df['answer'].apply(self.extract_2016_answer)
        merged_2016['comments'] = answers_df['comments']
        return merged_2016

    def get_path(self, day_part, type):
        return op.join('..', 'Data', 'qa_mock_exams', '2016', '2016_' + day_part + '_' + type + '.xml')

    def get_problems(self, day_part):
        questions_path = self.get_path(day_part, 'question')
        answers_path = self.get_path(day_part, 'answer')
        questions_df = self.read_file(questions_path)
        answer_df = self.read_file(answers_path)
        return questions_path, self.merge_2016_df(questions_df, answer_df)


class ProblemsWriter:
    def pretty_write(self, filepath):
        xml_string = open(filepath, encoding="utf8").read()
        xml_dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = xml_dom.toprettyxml()
        open(filepath, encoding="utf8", mode='w').write(pretty_xml)

    def write_problems(self, dataframes):
        final_path = op.join('..', 'Data', 'qa_mock_exams', 'all_problems.xml')
        root = ET.Element("problems")
        for df in dataframes:
            self.add_problems(df, root)
        tree = ET.ElementTree(root)
        tree.write(final_path)
        self.pretty_write(final_path)

    def initialize_problem(self, root):
        problem = ET.SubElement(root, 'problem')
        ET.SubElement(root, 'choices')
        return problem

    def add_problems(self, df, root):
        for i_row in range(df.shape[0]):
            problem = self.new_problem(df, i_row, root)
            self.add_question(df, i_row, problem)
            choices = ET.SubElement(problem, 'choices')
            self.add_choice(df, i_row, choices, 'A')
            self.add_choice(df, i_row, choices, 'A')
            self.add_choice(df, i_row, choices, 'A')
            if 'choice_D' in df:
                self.add_choice(df, i_row, choices, 'D')
            self.add_answers(df, i_row, problem)
            self.add_comments(df, i_row, problem)

    def new_problem(self, df, i_row, root):
        problem = ET.SubElement(root, 'problem')
        topic = df.loc[i_row, 'topic']
        if topic != '':
            problem.attrib['topic'] = topic
        problem.attrib['year'] = str(df.loc[i_row, 'year'])
        problem.attrib['filename'] = df.loc[i_row, 'filename']
        return problem

    def add_question(self, df, i_row, problem):
        question_node = ET.SubElement(problem, 'question')
        question_node.text = df.loc[i_row, 'question']

    def add_choice(self, df, i_row, choices_node, id):
        choice_text = df.loc[i_row, 'choice_' + id]
        if pd.isnull(choice_text):
            return
        choice_node = ET.SubElement(choices_node, 'choice')
        choice_node.text = choice_text
        choice_node.attrib['id'] = id

    def add_answers(self, df, i_row, problem):
        answer_node = ET.SubElement(problem, 'answer')
        answer_node.text = df.loc[i_row, 'answer']

    def add_comments(self, df, i_row, problem):
        comments_node = ET.SubElement(problem, 'comments')
        comments_node.text = df.loc[i_row, 'comments']


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
