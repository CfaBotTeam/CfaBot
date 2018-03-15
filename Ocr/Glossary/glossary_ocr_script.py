from Ocr.Glossary.glossary_builder import GlossaryBuilder
from Ocr.Glossary.glossary_files_resolver import FilePathResolver
from Ocr.Glossary.glossary_writer import GlossaryWriter


if __file__ == '__main__':
    resolver = FilePathResolver()
    paths = resolver.resolve_sorted_paths()
    builder = GlossaryBuilder()
    glossary = builder.build_glossary(paths)
    writer = GlossaryWriter()
    writer.write_glossary(glossary)
