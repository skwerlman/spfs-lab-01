from spfs import constants
from spfs.blocks import Block
from spfs.json import json


def serialize(data):
    return json.dumps(data).encode('utf-8')


def serialize_multihashes(blocks):
    return b'\n'.join([block.multihash for block in blocks])


class Object:
    def __init__(self, data, links=[]):
        self.data = data
        self.links = links

    @property
    def data_blocks(self):
        return self.break_into_blocks(self.data)

    @property
    def links_blocks(self):
        serialized_links = serialize(self.links)
        return self.break_into_blocks(serialized_links)

    @property
    def blocks(self):
        data_blocks_list_block = self.get_blocks_list_block(self.data_blocks)
        links_blocks_list_block = self.get_blocks_list_block(self.links_blocks)

        return [data_blocks_list_block, links_blocks_list_block]

    def get_blocks_list_block(self, blocks):
        blocks = list(blocks)
        serialized_blocks_list = serialize_multihashes(blocks)
        if len(serialized_blocks_list) <= constants.BLOCK_DATA_MAX_SIZE:
            list_block = Block(data=serialized_blocks_list, type_=b'L')

        else:
            list_block_blocks = self.break_into_blocks(serialized_blocks_list)
            list_block = self.get_blocks_list_block(list_block_blocks)

        blocks.append(list_block)
        return blocks

    def persist_related(self):
        data_blocks, links_blocks = self.blocks
        data_master_block = data_blocks[-1]
        links_master_block = links_blocks[-1]

        master_block = Block(serialize_multihashes([data_master_block, links_master_block]))
        for blocks_group in (data_blocks, links_blocks):
            for block in blocks_group:
                block.persist()
        return master_block

    def persist(self):
        master_block = self.persist_related()
        master_block.persist()
        return master_block

    @staticmethod
    def break_into_blocks(data, type_=b'D'):
        blocks = []

        counter = 0
        while True:
            start = counter * constants.BLOCK_DATA_MAX_SIZE
            end = start + constants.BLOCK_DATA_MAX_SIZE
            piece = data[start:end]

            if not piece:
                break

            block = Block(piece, type_=type_)
            blocks.append(block)

            counter += 1

        return blocks

    @classmethod
    def get_data(cls, multihash):
        block = Block.retrieve(multihash)

        if block.type == b'D':
            return block.data

        if block.type == b'L':
            data = b''
            children = block.data.split(b'\n')
            for child_multihash in children:
                data += cls.get_data(child_multihash)
            return data

    @classmethod
    def retrieve(cls, multihash):
        master_block = Block.retrieve(multihash)
        master_block_blocks_list = master_block.data.split(b'\n')
        data_block = Block.retrieve(master_block_blocks_list[0])
        links_block = Block.retrieve(master_block_blocks_list[1])

        data = cls.get_data(data_block.multihash)
        links = json.loads(cls.get_data(links_block.multihash))

        return cls(data, links)
