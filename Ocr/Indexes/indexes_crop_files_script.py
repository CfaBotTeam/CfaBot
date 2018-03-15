import os
from Ocr.files_resolver import FilePathResolver
from Ocr.image_cropper import ImageCropper


if __name__ == '__main__':
    resolver = FilePathResolver(os.path.join('Indexes', 'Corporate_Finance_And_Portfolio_Management'))
    cropper = ImageCropper(resolver, test_mode=False)
    cropper.crop_images()