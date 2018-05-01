from spfs.wallets import cli as wallets_cli
from spfs.identities import IdentityManager

_wallet = None


def open_wallet(name):
    wallet_key = wallets_cli.get_wallet_key(name)
    return wallets_cli.open_wallet(wallet_key, name)


def open_manager():
    global _wallet

    if _wallet is None:
        wallets = wallets_cli.list_wallets()
        keys = tuple(wallets.keys())
        if len(keys) == 0:
            raise Exception('You must create a wallet, first.')
        wallet_name = keys[0]
        _wallet = open_wallet(wallet_name)
        _wallet.name = wallet_name
        print(f'Using Wallet "{wallet_name}"')
    return IdentityManager(_wallet)


def persist_manager(manager):
    wallet_multihash = manager.persist()
    wallets_cli.add_to_wallets_list(manager.wallet.name, wallet_multihash)
