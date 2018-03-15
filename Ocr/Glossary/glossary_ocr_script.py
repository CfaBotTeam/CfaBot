from glossary_builder import GlossaryBuilder
from glossary_files_resolver import FilePathResolver
from glossary_writer import GlossaryWriter


resolver = FilePathResolver()
paths = resolver.resolve_sorted_paths()
builder = GlossaryBuilder()
glossary = builder.build_glossary(paths)
writer = GlossaryWriter()
writer.write_glossary(glossary)
