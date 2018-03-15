from Ocr.files_resolver import FilePathResolver
from Ocr.image_cropper import ImageCropper


if __name__ == '__main__':
    resolver = FilePathResolver('Glossary')
    cropper = ImageCropper(resolver, test=True)
    cropper.crop_images()
