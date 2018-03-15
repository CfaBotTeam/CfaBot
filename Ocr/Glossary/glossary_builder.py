import io
import os.path
from google.cloud import vision
from Ocr.Glossary.glossary_parser import GlossaryParser


class GlossaryBuilder:
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/abiarnes/Documents/Lessons/Fil_Rouge/CfaBot/Keys/CfaBot-ServiceKey-Adrien.json"
        self.parser_ = GlossaryParser()
        self.client_ = vision.ImageAnnotatorClient()

    @staticmethod
    def load_image(path):
        with io.open(path, 'rb') as image_file:
            return image_file.read()

    def build_glossary(self, filepaths):
        start = 0
        end = len(filepaths)
        while start < end:
            temp_end = start + 5
            if temp_end > end:
                temp_end = end
            self.build_problems_internal_(filepaths[start:temp_end])
            start = temp_end
        return self.parser_.get_glossary()

    def build_problems_internal_(self, image_paths):
        requests = []
        for image_path in image_paths:
            requests.append({
                'image': {'content': self.load_image(image_path)},
                'features': [{'type': vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
            })
        response = self.client_.batch_annotate_images(requests)
        self.parse_responses(zip(response.responses, image_paths))


    def parse_responses(self, responses):
        for response, image_path in responses:
            self.parse_annotations(response.full_text_annotation)

    def parse_annotations(self, annotations):
        for page in annotations.pages:
            blocks_iter = iter(self.get_next_word_from_blocks(page.blocks))
            self.parser_.parse_words(blocks_iter)

    def get_next_word_from_blocks(self, blocks):
        for block in blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    yield word
