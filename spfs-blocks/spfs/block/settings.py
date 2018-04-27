from os import environ
from pathlib import PosixPath

home = PosixPath(environ['HOME'])
default_spfs_home = home / '.data/spfs'
spfs_home = PosixPath(environ.get('SPFS_HOME', default_spfs_home))

blocks_path = spfs_home / 'blocks'
