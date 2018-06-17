import xml.etree.ElementTree as ET
from glob import glob
import os
import os.path
import re


def extract_year(file_path):
    match = re.match("^(\d{4})-.*\.xml", file_path)
    return match.group(1)


def extract_id_and_text(question_text):
    match = re.match("^(\d+)\.(.*)", question_text)
    id = match.group(1)
    text = match.group(2)
    return id, text.strip()


def add_problems(file_path, problems):
    filename = os.path.basename(file_path)
    xml_data = open(file_path, encoding="utf8").read()
    xml_data = xml_data.replace("&", "&amp; ") \
                       .replace("< ", "&lt; ")
    problems_xml = ET.XML("<problems>%s</problems>" % xml_data)
    for problem in problems_xml:
        problem.attrib['filename'] = filename
        problem.attrib['topic'] = ''
        problem.attrib['year'] = extract_year(filename)
        problem.attrib['category'] = '666'
        for child in problem:
            if child.tag == 'question':
                id, text = extract_id_and_text(child.text)
                child.attrib['id'] = id
                child.text = text
        problems.append(problem)


def write_problems(file_path, problems):
    root = ET.Element("problems")
    for prob in problems:
        root.append(prob)
    ET.ElementTree(root).write(file_path)


if __name__ == "__main__":
    problems = []
    output_filepath = "Data/qa_practice_exams_new/all_new_problems.xml"
    if os.path.exists(output_filepath):
        os.remove(output_filepath)
    xml_files = glob('Data/qa_practice_exams_new/*.xml')
    for xml_file in sorted(xml_files):
        print("Reading xml file %s" % xml_file)
        add_problems(xml_file, problems)
    write_problems(output_filepath, problems)
