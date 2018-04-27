from nacl.secret import SecretBox

from spfs.utils import get_multihash
from spfs.json import json
from spfs.objects import Object, serialize


class Wallet:
    def __init__(self, data=None, key=None):
        self.data = data or {}
        self.key = key

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        if key not in self.data:
            if key.endswith('_list'):
                self.data[key] = []
            else:
                self.data[key] = {}
        self.data[key] = value

    @classmethod
    def open(cls, name, password, multihash):
        key = get_multihash(f'{name}:{password}')
        box = SecretBox(key)

        encrypted_data = Object.get_data(multihash)
        serialized_data = box.decrypt(encrypted_data)

        return cls(json.loads(serialized_data), key)

    def persist(self):
        serialized_data = serialize(self.data)
        box = SecretBox(self.key)
        encrypted_data = box.encrypt(serialized_data)

        multihash = Object.break_into_blocks(encrypted_data)
        return multihash
