import xml.dom.minidom
import xml.etree.ElementTree as ET
import os.path as op
import pandas as pd

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
            self.add_choice(df, i_row, choices, 'B')
            self.add_choice(df, i_row, choices, 'C')
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
        question_node.attrib['id'] = str(df.loc[i_row, 'question_nb'])

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
