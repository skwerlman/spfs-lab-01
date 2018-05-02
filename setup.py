from distutils.core import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spfs-lab',
    version='0.0.1a1',
    packages=['spfs', 'spfs.identities', 'spfs.blocks', 'spfs.feeds', 'spfs.objects', 'spfs.wallets'],
    license='LICENSE',
    description='Simple Personal Feed System',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet'
    ]
)
