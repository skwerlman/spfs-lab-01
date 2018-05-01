from spfs.objects import Object


class Feed:
    def __init__(self, manager, base_object, leaf):
        self.manager = manager
        self.base_object = base_object
        self.leaf = leaf or base_object

    def create_entry(self, data, links):
        links['_previous'] = self.leaf.multihash
        entry = Object(data, links)

        self.leaf = entry

        return entry.multihash

    def verify_integrity(self):
        previous = self.leaf.multihash

        counter = 0
        while True:
            counter += 1
            obj = Object.retrieve(previous)
            previous = obj.links['_previous']

        assert obj.previous == self.base_object.multihash
