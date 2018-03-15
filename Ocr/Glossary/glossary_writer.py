import os
import json


class GlossaryWriter:
    def write_glossary(self, glossary):
        text = json.dumps(glossary, indent=4)
        path = os.path.join('Data', 'material_handbook', 'glossary.json')
        with open(path, 'w') as f:
            f.write(text)
