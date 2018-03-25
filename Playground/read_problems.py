import xml.etree.ElementTree as ET
import vkbeautify as vkb
import json
import pandas as pd
import numpy as np

def read_xml(path):
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
    return res

def read_questions_json(path):
    data = json.load(open(path))
    for query in data:
        choices = query.pop('choices')
        for i_choice, choice in enumerate(choices):
            choice_key = 'choice_' + chr(65 + i_choice)
            query[choice_key] = choice
    res = pd.DataFrame(queries)
    return res

def read_all_problems():
    # read all problems XML file and return a dataframe 
    file_path = '../Data/qa_mock_exams/all_problems.xml'
    return read_xml(file_path)

def add_to_xml(problems_xml, record):
    problem_xml = ET.SubElement(problems_xml, 'problem')
    problem_xml.attrib['filename'] = record['filename']
    problem_xml.attrib['topic'] = record['topic']
    problem_xml.attrib['category'] = str(record['category'])
    problem_xml.attrib['year'] = record['year']
    question_xml = ET.SubElement(problem_xml, 'question')
    question_xml.attrib['id'] = record['question_nb']
    question_xml.text = record['question']
    choices_xml = ET.SubElement(problem_xml, 'choices')
    choice_A_xml = ET.SubElement(choices_xml, 'choice')
    choice_A_xml.attrib['id'] = 'A'
    choice_A_xml.text = record['choice_A']
    choice_B_xml = ET.SubElement(choices_xml, 'choice')
    choice_B_xml.attrib['id'] = 'B'
    choice_B_xml.text = record['choice_B']
    choice_C_xml = ET.SubElement(choices_xml, 'choice')
    choice_C_xml.attrib['id'] = 'C'
    choice_C_xml.text = record['choice_C']
    if 'choice_D' in record and not record['choice_D'] is np.NaN:
        choice_D_xml = ET.SubElement(choices_xml, 'choice')
        choice_D_xml.attrib['id'] = 'D'
        choice_D_xml.text = record['choice_D']
    answer_xml = ET.SubElement(problem_xml, 'answer')
    answer_xml.text = record['answer']
    comments_xml = ET.SubElement(problem_xml, 'comments')
    comments_xml.text = record['comments']
    
def write_problems(df):
    file_path = '../Data/qa_mock_exams/all_problems.xml'
    document = ET.Element('problems')
    df.apply(lambda r: add_to_xml(document, r), axis=1)
    xml_text = ET.tostring(document, encoding='unicode', method="xml")
    pretty_xml_text = vkb.xml(xml_text)
    vkb.xml(pretty_xml_text, file_path)
