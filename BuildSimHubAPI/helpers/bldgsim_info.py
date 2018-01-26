
import os.path
from pathlib import Path

class MetaInfo():

    """docstring for MetalInfo"""
    def __init__(self):
        dirpath = Path(os.path.dirname(os.path.realpath(__file__))).parent
        assert(dirpath.is_dir())
        q = dirpath / 'info.config'
        assert(q.exists())
        with q.open() as f:
            key, value = f.readline().split(":")
            self._userKey = value

    @property
    def userKey(self):
        return self._userKey
        
