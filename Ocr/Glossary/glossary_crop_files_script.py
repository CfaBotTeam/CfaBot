from Ocr.Glossary.glossary_files_resolver import FilePathResolver
from Ocr.image_cropper import ImageCropper


if __file__ == '__main__':
    resolver = FilePathResolver()
    cropper = ImageCropper(resolver, test=True)
    cropper.crop_images()
