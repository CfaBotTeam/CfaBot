import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import pandas as pd
from glob import glob
import os.path as op


def add_records(path, all_records):
    xml_data = open(path).read()
    xml_data = "<problems>" + xml_data + "</problems>"
    problems = ET.XML(xml_data)
    for problem in problems:
        record = {}
        for child in problem:
            if child.tag == "choices":
                for choice in child:
                    id = choice.attrib['id']
                    record[choice.tag + '_' + id] = choice.text
            else:
                record[child.tag] = child.text
        all_records.append(record)


all_records = []
file_paths = sorted(glob(op.join('Data', 'qa_mock_exams', '*', '*.xml')))
for path in file_paths:
    try:
        add_records(path, all_records)
    except ParseError as e:
        print("Exception in file '{}': {}".format(path, e))

problems_df = pd.DataFrame(all_records)

print(problems_df.columns)
