import xml.etree.ElementTree as ET
import pandas as pd
from glob import glob
import os.path as op
import re


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
