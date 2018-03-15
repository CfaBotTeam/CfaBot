import os.path
import re
from glob import glob
import pandas as pd


class FilePathResolver:
    def __init__(self, folder):
        self.folder_ = folder

    def extract_page_number(self, path):
        filename = os.path.basename(path)
        pattern = ".*-(\d+).jpg"
        match = re.match(pattern, filename)
        return int(match.groups()[0])

    def resolve_sorted_paths(self):
        paths = glob(os.path.join('Data', 'material_handbook', self.folder_, 'CFA-*.jpg'))
        df = pd.DataFrame(paths, columns=['filepath'])
        df['page_number'] = df['filepath'].map(self.extract_page_number)
        df.sort_values(["page_number"], inplace=True)
        return df['filepath'].values
