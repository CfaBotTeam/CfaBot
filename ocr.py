import requests
import base64
import os.path as op
import sys


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read())


my_key = "AIzaSyAgHEqLAy5AbspQ4KqG_OjHV-JSKlVzLho"

data = dict()
reqs = []
request = dict()
image_path = op.join('Data', 'qa_mock_exams', '2014', '2014_afternoon', '2014_afternoon_answer 1.jpeg')
img = dict()
img['content'] = get_base64_encoded_image(image_path)
request['image'] = img
features = []
feature = dict()
feature['type'] = 'DOCUMENT_TEXT_DETECTION'
features.append(feature)
request['features'] = features
reqs.append(request)
data['requests'] = reqs
size = sys.getsizeof(data)
headers = {'Content-Length': 2064820, 'Content-Type': 'application/json'}
request_result = requests.post("https://vision.googleapis.com/v1/images:annotate?fields=responses&key=" + my_key + "&alt=json", data=data, headers=headers).json()

pass