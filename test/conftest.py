import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def tmp_dir() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as dir_:
        yield str(Path(dir_).absolute())


@pytest.fixture
def tmp_dir_chdir(tmp_dir) -> Generator[str, None, None]:
    curr_cwd = os.getcwd()
    os.chdir(tmp_dir)
    try:
        yield tmp_dir
    finally:
        os.chdir(curr_cwd)
