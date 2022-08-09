from web3 import Web3
from ethsys.utils.properties import Properties
from ethsys.networks.default import Default


class Ropsten(Default):
    """A Ropsten node giving access to the underlying network."""
    HOST = 'ropsten.infura.io/v3'
    PORT = None

    @classmethod
    def chain_id(cls): return 3

    @classmethod
    def connect(cls, private_key, host, port):
        web3 = Web3(Web3.HTTPProvider('https://%s/%s' % (host, Properties().infuraProjectID())))
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account

    @classmethod
    def connect_account1(cls):
        return cls.connect(Properties().account1pk(), cls.HOST, None)

    @classmethod
    def connect_account2(cls):
        return cls.connect(Properties().account2pk(), cls.HOST, None)

    @classmethod
    def connect_account3(cls):
        return cls.connect(Properties().account3pk(), cls.HOST, None)




