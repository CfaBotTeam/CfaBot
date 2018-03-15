import os.path
import re
from xml.etree import ElementTree as ET
import vkbeautify as vkb
from glob import glob
import pandas as pd


class FilePathResolver:
    def __init__(self, year, day_part, file_part):
        self.year_ = year
        self.day_part_ = day_part
        self.file_part_ = file_part

    def extract_page_number(self, path):
        filename = os.path.basename(path)
        pattern = self.year_ + "_" + self.day_part_
        if self.file_part_ != '':
            pattern = pattern + "_" + self.file_part_
        pattern = pattern + " (\d+).jpeg"
        match = re.match(pattern, filename)
        return int(match.groups()[0])

    def resolve_sorted_paths(self):
        paths = glob(os.path.join('Data', 'qa_mock_exams', self.year_, self.year_ + '_' + self.day_part_, '*.jpeg'))
        df = pd.DataFrame(paths, columns=['filepath'])
        df['page_number'] = df['filepath'].map(self.extract_page_number)
        df.sort_values(["page_number"], inplace=True)
        return df['filepath'].values

    def get_xml_result_file(self):
        return os.path.join('Data', 'qa_mock_exams', self.year_, self.year_ + '_' + self.day_part_ + '.xml')


class ProblemsWriter:
    def __init__(self):
        pass

    def get_xml_document(self, problems):
        document = ET.Element('problems')
        for problem in problems:
            problem_xml = ET.SubElement(document, 'problem')
            question_xml = ET.SubElement(problem_xml, 'question')
            question_xml.text = problem.question_
            choices_xml = ET.SubElement(problem_xml, 'choices')
            for choice in problem.choices_:
                choice_xml = ET.SubElement(choices_xml, 'choice')
                choice_xml.text = choice
            answer_xml = ET.SubElement(problem_xml, 'answer')
            answer_xml.text = problem.answer_
            comments_xml = ET.SubElement(problem_xml, 'comments')
            comments_xml.text = problem.comments_
        return document

    def write_problems(self, to_path, problems):
        document = self.get_xml_document(problems)
        xml_text = ET.tostring(document, encoding='unicode', method="xml")
        pretty_xml_text = vkb.xml(xml_text)
        vkb.xml(pretty_xml_text, to_path)