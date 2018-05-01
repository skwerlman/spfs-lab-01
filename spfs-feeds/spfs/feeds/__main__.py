import click

from spfs.wallets import cli as wallets_cli
from .manager import FeedManager
from spfs.identities import cli as identities_cli


@click.group()
def cmds():
    pass


@cmds.command()
@click.argument('identity_name')
@click.argument('name')
def create(identity_name, name):
    identities_manager = identities_cli.open_manager()
    identity = identities_manager.identities[identity_name]
    manager = FeedManager(identity)
    feed = manager.create(name)
    block = feed.persist()
    print(block.multihash)

    wallet_multihash = manager.persist()
    print('wallet_multihash:', wallet_multihash)
    wallets_cli.add_to_wallets_list(identities_manager.wallet.name, wallet_multihash)


cmds()
