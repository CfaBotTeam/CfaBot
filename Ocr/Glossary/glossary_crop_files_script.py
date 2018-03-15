import os
from PIL import Image
from glossary_helpers import FilePathResolver


def get_cropped_path(path):
    base = os.path.basename(path)
    dir = os.path.dirname(path)
    filename = 'cropped_{}.jpg'.format(base)
    return os.path.join(dir, filename)


resolver = FilePathResolver()
paths = resolver.resolve_sorted_paths()

for i, path in enumerate(paths):
    crop_height = 260 if i == 0 else 120
    img = Image.open(path)
    img = img.crop((0, crop_height, img.width, img.height))
    img.save(path)
