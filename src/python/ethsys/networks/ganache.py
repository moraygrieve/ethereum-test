from web3 import Web3
from ethsys.utils.properties import Properties
from pysys.constants import *


class GanacheNetwork:

    @classmethod
    def run(cls, test):
        port = test.getNextAvailableTCPPort()
        stdout = os.path.join(test.output, 'ganache.out')
        stderr = os.path.join(test.output, 'ganache.err')

        arguments = []
        if port is not None: arguments.extend(('--port', str(port)))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().privateKey()))
        hprocess = test.startProcess(command=PROJECT.ganacheBin, displayName='ganache', workingDir=test.output,
                                     environs=os.environ,
                                     arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)

        test.waitForSignal(stdout, expr='Listening on 127.0.0.1:%d' % port, timeout=10)
        return hprocess, port


    @classmethod
    def connect(cls, test, host='127.0.0.1', port=3000):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        account = web3.eth.account.privateKeyToAccount(Properties().privateKey())
        web3.eth.default_account = account.address
        return web3, account

    @classmethod
    def build_transaction(cls, test, web3, contract, account):
        pass

    @classmethod
    def send_transaction(cls, test, web3, contract, account, build_tx):
        return contract.transact()

    @classmethod
    def wait_for_transaction(cls, test, web3, tx_hash):
        return web3.eth.wait_for_transaction_receipt(tx_hash)