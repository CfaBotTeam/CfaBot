import xml.etree.ElementTree as ET
import json
import pandas as pd


class ProblemsReader:
    def __init__(self, dataset_path):
        self.dataset_path_ = dataset_path

    def read_xml(self, path):
        xml_data = open(path, encoding="utf8").read()
        problems = ET.XML(xml_data)
        records = []
        for problem in problems:
            record = {}
            record['filename'] = problem.attrib['filename']
            record['topic'] = problem.attrib['topic']
            record['year'] = problem.attrib['year']
            record['category'] = int(problem.attrib['category'])
            for child in problem:
                if child.tag == "choices":
                    for choice in child:
                        id = choice.attrib['id']
                        record[choice.tag + '_' + id] = choice.text
                else:
                    record[child.tag] = child.text
                    if child.tag == 'question':
                        record['question_nb'] = child.attrib['id']
            records.append(record)
        res = pd.DataFrame(records)
        res['question'] = res['question'].str.strip()
        return res

    def read_questions_json(self, path):
        data = json.load(open(path))
        for query in data:
            choices = query.pop('choices')
            for i_choice, choice in enumerate(choices):
                choice_key = 'choice_' + chr(65 + i_choice)
                query[choice_key] = choice
        res = pd.DataFrame(data)
        res['question'] = res['question'].str.strip()
        return res

    def read_all_problems(self):
        # read all problems XML file and return a dataframe
        return self.read_xml(self.dataset_path_)
