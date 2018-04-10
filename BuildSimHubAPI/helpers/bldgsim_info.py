
import os.path
from pathlib import Path


class MetaInfo:

    """docstring for MetalInfo

    read the info configuration
    api and base_url (for testing)

    """
    def __init__(self):
        dirpath = Path(os.path.dirname(os.path.realpath(__file__))).parent
        assert(dirpath.is_dir())
        q = dirpath / 'info.config'
        assert(q.exists())
        with q.open() as f:
            key, value = f.readline().split("=")
            if key == 'user_api_key':
                self._user_key = value.strip()
            elif key == 'base_url':
                self._base_url = value.strip()

            key, value = f.readline().split("=")
            if key == 'user_api_key':
                self._user_key = value.strip()
            elif key == 'base_url':
                self._base_url = value.strip()

    @property
    def user_key(self):
        return self._user_key

    @property
    def base_url(self):
        return self._base_url
