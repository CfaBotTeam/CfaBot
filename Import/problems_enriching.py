import xml.etree.ElementTree as ET
import re
import os


class TopicIndex:
    def __init__(self, xml_path):
        self.question_topics_ = {}
        self.initialized_ = False
        xml_data = open(xml_path, encoding="utf8").read()
        nodes = ET.XML(xml_data)
        for node in nodes:
            if node.tag != 'dispatch':
                continue
            self.initialized_ = True
            self.read_index(node)

    def read_index(self, index):
        for topic_node in index:
            name = topic_node.attrib['id']
            start = -1
            end = -1
            for sub_node in topic_node:
                if sub_node.tag == 'start':
                    start = int(sub_node.text)
                if sub_node.tag == 'end':
                    end = int(sub_node.text)
            if start == -1 or end == -1:
                continue
            for i in range(start, end + 1):
                self.question_topics_[i] = name

    def get_topic(self, question_number):
        if not self.initialized_:
            return ''
        if question_number not in self.question_topics_:
            print('Error in topic index:' + str(question_number))
            return ''
        return self.question_topics_[question_number]


class ProblemsEnricher:
    def extract_question_number(self, question, path):
        match = re.match('^(\d+)\. (.*)$', question, re.DOTALL)
        if match is None:
            print('error with question number:')
            print(path)
            print(question)
            print()
            return -1
        return int(match.group(1))

    def extract_question(self, question, path):
        match = re.match('^(\d+)\. (.*)$', question, re.DOTALL)
        if match is None:
            print('error with question:')
            print(path)
            print(question)
            print()
            return question
        return match.group(2)

    def assign_topic(self, topic_index, question_nb):
        return topic_index.get_topic(question_nb)

    def extract_filename(self, filepath):
        return os.path.basename(filepath)

    def extract_year(self, filename):
        match = re.match('^(\d+)_.*.xml$', filename)
        return int(match.group(1))

    def enrich(self, filepaths, dfs):
        for df, path in zip(dfs, filepaths):
            topic_index = TopicIndex(path)
            df['question_nb'] = df['question'].apply(lambda q: self.extract_question_number(q, path))
            df['question'] = df['question'].apply(lambda q: self.extract_question(q, path))
            filename = self.extract_filename(path)
            df['year'] = self.extract_year(filename)
            df['filename'] = filename
            df['topic'] = df['question_nb'].apply(lambda nb: topic_index.get_topic(nb))
