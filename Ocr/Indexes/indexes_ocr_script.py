import os
from Ocr.Glossary.glossary_writer import GlossaryWriter
from Ocr.Glossary.glossary_parser import GlossaryParser
from Ocr.files_resolver import FilePathResolver
from Ocr.image_extractor import ImageExtractor


if __name__ == '__main__':
    folders = ['Corporate_Finance_And_Portfolio_Management',
               'Derivative_and_Alternative_Investments',
               'Economics',
               'Equity_and_Fixed_Income',
               'Ethics_and_Quantitative_Methods',
               'Financial_Reporting_And_Analysis']
    for folder in folders[:1]:
        resolver = FilePathResolver(os.path.join('Indexes', folder))
        paths = resolver.resolve_sorted_paths()
        extractor = ImageExtractor(GlossaryParser())
        glossary = extractor.extract_data(paths)
        writer = GlossaryWriter()
        writer.write_glossary(glossary)
