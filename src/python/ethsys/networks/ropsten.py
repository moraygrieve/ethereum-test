from web3 import Web3
from ethsys.utils.properties import Properties
from pysys.constants import *


class RopstenNetwork:

    @classmethod
    def init(cls, test):
        return None, 'ropsten.infura.io/v3', None

    @classmethod
    def connect(cls, test, host, port):
        web3 = Web3(Web3.HTTPProvider('https://%s/%s' % (host, Properties().infuraProjectID())))
        private_key = Properties().privateKey()
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account

    @classmethod
    def build_transaction(cls, test, web3, contract, account):
        build_tx = contract.buildTransaction(
            {
                'nonce': web3.eth.get_transaction_count(account.address),
                'gasPrice': web3.eth.gas_price,
                'gas': 720000,
                'chainId': 3
            }
        )
        signed_tx = account.sign_transaction(build_tx)
        return signed_tx

    @classmethod
    def send_transaction(cls, test, web3, contract, account, signed_tx):
        tx_hash = None
        try:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except Exception as e:
            test.log.error('Error sending raw transaction %s' % e)
            test.addOutcome(BLOCKED, abortOnError=TRUE)
        test.log.info('Transaction sent with hash %s' % tx_hash.hex())
        return tx_hash

    @classmethod
    def wait_for_transaction(cls, test, web3, tx_hash):
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 0:
            test.log.error('Transaction receipt has failed status ... aborting')
            test.addOutcome(BLOCKED, abortOnError=TRUE)
        test.log.info('Transaction receipt for block hash %s' % tx_receipt.blockHash.hex())
        return tx_receipt
