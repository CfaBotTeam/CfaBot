from Ocr.Glossary.glossary_writer import GlossaryWriter
from Ocr.Glossary.glossary_parser import GlossaryParser
from Ocr.files_resolver import FilePathResolver
from Ocr.image_extractor import ImageExtractor


if __name__ == '__main__':
    resolver = FilePathResolver('Glossary')
    paths = resolver.resolve_sorted_paths()
    extractor = ImageExtractor(GlossaryParser())
    glossary = extractor.extract_data(paths)
    writer = GlossaryWriter()
    writer.write_glossary(glossary)
