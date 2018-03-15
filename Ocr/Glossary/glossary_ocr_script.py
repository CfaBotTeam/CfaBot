from Ocr.Glossary.glossary_builder import GlossaryBuilder
from Ocr.Glossary.glossary_writer import GlossaryWriter
from Ocr.files_resolver import FilePathResolver


if __name__ == '__main__':
    resolver = FilePathResolver('Glossary')
    paths = resolver.resolve_sorted_paths()
    builder = GlossaryBuilder()
    glossary = builder.build_glossary(paths)
    writer = GlossaryWriter()
    writer.write_glossary(glossary)
