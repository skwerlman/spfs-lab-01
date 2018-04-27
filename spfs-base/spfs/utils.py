import datetime

import multihash

def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_multihash(data):
    return multihash.digest(data, 'sha2_256').digest.hex()
