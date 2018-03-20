import os
from Ocr.files_resolver import FilePathResolver
from Ocr.image_cropper import ImageCropper


if __name__ == '__main__':
    folders = ['Corporate_Finance_And_Portfolio_Management',
               'Derivative_and_Alternative_Investments',
               'Economics',
               'Equity_and_Fixed_Income',
               'Ethics_and_Quantitative_Methods',
               'Financial_Reporting_And_Analysis']
    for folder in folders:
        resolver = FilePathResolver(os.path.join('Indexes', folder))
        cropper = ImageCropper(resolver, test_mode=False)
        cropper.crop_images()