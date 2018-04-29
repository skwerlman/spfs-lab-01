import zlib

from spfs import utils, constants
from . import settings
from .exceptions import BlockNotFoundError


class Block:
    def __init__(self, data, type_=b'D'):
        self.type = type_
        self.data = data

    @property
    def multihash(self):
        return utils.get_multihash(self.type + self.data)

    def __str__(self):
        size = len(self.data) + 1
        return f'{self.multihash}/{size}: {self.type}'

    def __repr__(self):
        return f'<Block {self}>'

    def generate_payload(self):
        if not isinstance(self.data, bytes):
            the_type = type(self.data)
            raise TypeError(f'`data` should be bytes, not {the_type}')

        if not isinstance(self.type, bytes):
            the_type = type(self.type)
            raise TypeError(f'`type` should be bytes, not {the_type}')

        payload = self.type + self.data

        if len(payload) > constants.BLOCK_MAX_SIZE:
            raise ValueError(f'`data` must be smaller than {constants.BLOCK_MAX_SIZE}')

        return payload

    @property
    def path(self):  # pragma: no cover
        return settings.blocks_path / self.multihash

    def persist(self):
        payload = self.generate_payload()
        self.persist_to_disk(payload, self.path)

    def persist_to_disk(self, data, path):  # pragma: no cover
        if path.is_file():
            return
        return self.do_persist_to_disk(data, path)

    def do_persist_to_disk(self, data, path):  # pragma: no cover
        compressed_data = zlib.compress(data)
        with path.open('wb') as file_object:
            file_object.write(compressed_data)

    @classmethod
    def retrieve(cls, multihash):
        path = settings.blocks_path / multihash
        payload = cls.retrieve_from_disk(path)
        return cls.parse_payload(payload)

    @staticmethod
    def retrieve_from_disk(path):
        if not path.is_file():
            raise BlockNotFoundError()

        with path.open('rb') as file_object:  # pragma: no cover
            payload = zlib.decompress(file_object.read())
        return payload  # pragma: no cover

    @classmethod
    def parse_payload(cls, payload):
        type_, data = payload[0:1], payload[1:]
        return cls(data, type_=type_)
