import string
import tempfile

import numpy as np
import pytest

from jsim.Util.Map import Map


def test_map_invalid():
    with pytest.raises(FileNotFoundError):
        Map("".join(np.random.choice(list(string.ascii_letters), size=(10,))) + ".tif")


def test_map_valid():
    fd, path = tempfile.mkstemp(suffix=".txt")
    Map(path)
