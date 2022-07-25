from web3 import Web3
from ethsys.utils.properties import Properties

class RopstenNetwork:

    @classmethod
    def chainID(cls):
        return 3

    @classmethod
    def run(cls):
        raise NotImplementedError

    @classmethod
    def connect(cls, test, host=None, port=None):
        w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/%s' % Properties().infuraProjectID()))
        private_key = Properties().privateKey()
        account = w3.eth.account.privateKeyToAccount(private_key)
        return (private_key, account)

    @classmethod
    def waitForTransaction(cls):
        raise NotImplementedError