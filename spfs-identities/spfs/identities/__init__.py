from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, PublicKey, Box
from nacl.secret import SecretBox

from spfs.mixins import DictLikeMixin


class Identity(DictLikeMixin):
    def __init__(self, name, private_key, data=None):
        self.name = name
        self.data = data or {}

        if isinstance(private_key, PrivateKey):
            self.private_key_obj = private_key
            self.private_key = private_key.encode().hex()
        else:
            self.private_key = private_key
            self.private_key_obj = PrivateKey(self.private_key, HexEncoder())

        self.secret_box = SecretBox(bytes.fromhex(self.private_key))
        self.boxes = {}

    def get_box(self, other_public_key):
        if other_public_key not in self.boxes:
            opk = PublicKey(other_public_key, HexEncoder())
            self.boxes[other_public_key] = Box(self.private_key_obj, opk)
        return self.boxes[other_public_key]

    def as_dict(self):
        return {
            'name': self.name,
            'private_key': self.private_key,
            'data': self.data
        }


class IdentityManager:
    def __init__(self, wallet):
        self.wallet = wallet
        self.identities = {}

        self.retrieve()

    def retrieve(self):
        for name, identity_data in self.wallet['identities'].items():
            private_key = identity_data['private_key']
            data = identity_data['data']
            self.identities[name] = Identity(name, private_key, data)

    def create(self, name):
        private_key = PrivateKey.generate()
        identity = Identity(name, private_key)
        self.identities[name] = identity
        return identity

    def persist(self):
        for name, identity in self.identities.items():
            self.wallet['identities'][name] = identity.as_dict()
        return self.wallet.persist()
