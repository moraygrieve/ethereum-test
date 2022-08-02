from web3 import Web3, IPCProvider
from web3.middleware import geth_poa_middleware
from ethsys.networks.default import DefaultNetwork


class GethNetwork(DefaultNetwork):
    HOST = '127.0.0.1'
    PORT = 8545

    @classmethod
    def chain_id(cls): return 1337

    @classmethod
    def connect(cls, private_key, host, port):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account
