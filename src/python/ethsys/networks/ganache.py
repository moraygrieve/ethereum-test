from web3 import Web3
from pysys.constants import *
from ethsys.utils.properties import Properties
from ethsys.networks.default import DefaultNetwork


class GanacheNetwork(DefaultNetwork):
    HOST = '127.0.0.1'
    PORT = 8545

    @classmethod
    def connect_account1(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.PORT)))
        private_key = Properties().account1PK()
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account

    @classmethod
    def connect_account2(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.PORT)))
        private_key = Properties().account2PK()
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account

    @classmethod
    def connect_account3(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.PORT)))
        private_key = Properties().account3PK()
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account

    @classmethod
    def chain_id(cls):
        return 1337

    @classmethod
    def transact(cls, test, web3, target, account, gas):
        tx_sign = cls.build_transaction(test, web3, target, account, gas)
        tx_hash = cls.send_transaction(test, web3, target, tx_sign)
        tx_recp = cls.wait_for_transaction(test, web3, tx_hash)
        return tx_recp

    @classmethod
    def build_transaction(cls, test, web3, target, account, gas):
        build_tx = target.buildTransaction(
            {
                'nonce': web3.eth.get_transaction_count(account.address),
                'gasPrice': web3.eth.gas_price,
                'gas': gas,
                'chainId': cls.chain_id()
            }
        )
        signed_tx = account.sign_transaction(build_tx)
        return signed_tx

    @classmethod
    def send_transaction(cls, test, web3, target, signed_tx):
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

        if tx_receipt.status == 1:
            test.log.info('Transaction complete gasUsed=%d' % tx_receipt.gasUsed)
            test.log.info('Transaction receipt block hash %s' % tx_receipt.blockHash.hex())
        else:
            test.log.error('Transaction receipt failed')
            test.log.error('Full receipt: %s' % tx_receipt)
            test.addOutcome(FAILED, abortOnError=TRUE)
        return tx_receipt