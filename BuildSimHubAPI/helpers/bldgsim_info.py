
import os.path
from pathlib import Path


class MetaInfo:

    """docstring for MetalInfo"""
    def __init__(self):
        dirpath = Path(os.path.dirname(os.path.realpath(__file__))).parent
        assert(dirpath.is_dir())
        q = dirpath / 'info.config'
        assert(q.exists())
        with q.open() as f:
            key, value = f.readline().split(":")
            if key == 'user_api_key':
                self._userKey = value
            elif key == 'base_url':
                self._base_url = value

    @property
    def userKey(self):
        return self._userKey

    @property
    def base_url(self):
        return self._base_url