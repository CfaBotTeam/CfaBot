#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import sys
from pathlib import WindowsPath, PosixPath

if sys.version_info < (3, 5):
    raise RuntimeError('DrQA supports Python 3.5 or higher.')


def get_data_dir():
    res = os.getenv('DRQA_DATA')
    if res:
        return res
    if os.name == 'nt':
        path = WindowsPath(__file__)
    else:
        path = PosixPath(__file__)
    return os.path.join(path.absolute().parents[1].as_posix(), 'data')


DATA_DIR = get_data_dir()

from . import tokenizers
from . import reader
from . import retriever
from . import pipeline
from . import selector
from . import utils
