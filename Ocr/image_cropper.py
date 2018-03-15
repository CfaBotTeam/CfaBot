import os
from PIL import Image


class ImageCropper:
    def __init__(self, resolver, test_mode=True):
        self.resolver_ = resolver
        self.test_mode_ = test_mode

    def get_cropped_path(self, path):
        base = os.path.basename(path)
        dir = os.path.dirname(path)
        filename = 'cropped_{}.jpg'.format(base)
        return os.path.join(dir, filename)

    def crop_images(self):
        paths = self.resolver_.resolve_sorted_paths()

        for i, path in enumerate(paths):
            crop_height = 260 if i == 0 else 120
            img = Image.open(path)
            img = img.crop((0, crop_height, img.width, img.height))
            img.save(path)
