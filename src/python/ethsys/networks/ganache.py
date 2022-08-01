from web3 import Web3
from ethsys.utils.properties import Properties
from ethsys.networks.default import DefaultNetwork


class GanacheNetwork(DefaultNetwork):
    HOST = '127.0.0.1'
    PORT = 8545

    @classmethod
    def connect_account1(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.PORT)))
        account = web3.eth.account.privateKeyToAccount(Properties().account1PK())
        web3.eth.default_account = account.address
        return web3, account

    @classmethod
    def connect_account2(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.PORT)))
        account = web3.eth.account.privateKeyToAccount(Properties().account2PK())
        web3.eth.default_account = account.address
        return web3, account

    @classmethod
    def connect_account3(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.PORT)))
        account = web3.eth.account.privateKeyToAccount(Properties().account3PK())
        web3.eth.default_account = account.address
        return web3, account

    @classmethod
    def chain_id(cls):
        return 1337

    @classmethod
    def transact(cls, test, web3, target, account, gas):
        return target.transact()

    @classmethod
    def build_transaction(cls, test, web3, target, account, gas):
        pass

    @classmethod
    def send_transaction(cls, test, web3, target, build_tx):
        pass

    @classmethod
    def wait_for_transaction(cls, test, web3, tx_hash):
        return web3.eth.wait_for_transaction_receipt(tx_hash)