
import os.path


class MetaInfo(object):

    """docstring for MetalInfo

    read the info configuration
    api and base_url (for testing)

    """

    def __init__(self):
        dirpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        assert(os.path.isdir(dirpath))

        q = os.path.join(dirpath, 'info.config')
        assert(os.path.exists(q))

        with open(q, 'r') as f:
            for line in f:
                key, value = line.strip().split("=")
                if key == 'user_api_key':
                    self._user_key = value.strip()
                elif key == 'base_url':
                    self._base_url = value.strip()
                elif key == 'vendor_id':
                    self._vendor_id = value.strip()

    @property
    def user_key(self):
        return self._user_key

    @property
    def base_url(self):
        return self._base_url

    @property
    def vendor_id(self):
        return self._vendor_id
