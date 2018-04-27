from .utils import timestamp


class Feed:
    def __init__(self, name):
        self.name = name
        self.created_at = timestamp()
        self.persisted_at = None

    def save(self, database, identity):
        table = database['feeds']
        self.persisted_at = timestamp()
        table.insert({
            'name': self.name.encode('utf-8'),
            'created_at': self.created_at,
            'persisted_at': self.persisted_at,
        })
