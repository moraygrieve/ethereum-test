from web3 import Web3
from ethsys.utils.properties import Properties
from pysys.constants import *


class RopstenNetwork:

    @classmethod
    def chain_id(cls):
        return 3

    @classmethod
    def run(cls):
        raise NotImplementedError

    @classmethod
    def connect(cls, test, host=None, port=None):
        web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/%s' % Properties().infuraProjectID()))
        private_key = Properties().privateKey()
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, private_key, account

    @classmethod
    def buildTransaction(cls, test, web3, contract, account):
        return contract.build_transaction(
            {
                'from': account.address,
                'nonce': web3.eth.getTransactionCount(account.address),
                'gasPrice': web3.eth.gas_price,
                'gas': 720000,
                'chainId': cls.chain_id()
            }
        )

    @classmethod
    def sendRawTransaction(cls, test, web3, account, build_tx):
        signed_tx = account.signTransaction(build_tx)
        tx_hash = None
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except Exception as e:
            test.log.error('Error sending raw transaction %s' % e)
            test.addOutcome(BLOCKED, abortOnError=TRUE)
        return tx_hash

    @classmethod
    def waitForTransaction(cls, test, web3, tx_hash):
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            test.log.error('Transaction receipt has failed status ... aborting')
            test.addOutcome(BLOCKED, abortOnError=TRUE)
        return tx_receipt
