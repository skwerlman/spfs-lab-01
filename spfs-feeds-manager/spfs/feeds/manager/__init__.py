import dataset


class FeedManager:
    def __init__(self):
        pass

    def db_connect(self):
        self.db = dataset.connect()
