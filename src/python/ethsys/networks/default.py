from web3 import Web3
from pysys.constants import *
from ethsys.utils.properties import Properties


class Default:
    """A default node giving access to an underlying network."""
    HOST = None
    PORT = None

    @classmethod
    def chain_id(cls): return None

    @classmethod
    def connect(cls, private_key, host, port):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        account = web3.eth.account.privateKeyToAccount(private_key)
        return web3, account

    @classmethod
    def connect_account1(cls):
        return cls.connect(Properties().account1pk(), cls.HOST, cls.PORT)

    @classmethod
    def connect_account2(cls):
        return cls.connect(Properties().account2pk(), cls.HOST, cls.PORT)

    @classmethod
    def connect_account3(cls):
        return cls.connect(Properties().account3pk(), cls.HOST, cls.PORT)

    @classmethod
    def transact(cls, test, web3, target, account, gas):
        tx_sign = cls.build_transaction(test, web3, target, account, gas)
        tx_hash = cls.send_transaction(test, web3, target, tx_sign)
        tx_recp = cls.wait_for_transaction(test, web3, tx_hash)
        return tx_recp

    @classmethod
    def build_transaction(cls, test, web3, target, account, gas):
        test.log.info('Nonce being used is %d' % web3.eth.get_transaction_count(account.address)  )
        build_tx = target.buildTransaction(
            {
                'nonce': web3.eth.get_transaction_count(account.address),
                'gasPrice': web3.eth.gas_price,
                'gas': gas,
                'chainId': web3.eth.chain_id
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

    @classmethod
    def get_block_number(cls, web3):
        return web3.eth.get_block_number()

    @classmethod
    def get_balance(cls, web3, account):
        return web3.eth.get_balance(account)

    @classmethod
    def get_block_by_number(cls, web3, block_number):
        return web3.eth.get_block(block_number)

    @classmethod
    def get_block_by_hash(cls, web3, block_hash):
        return web3.eth.get_block(block_hash)

    @classmethod
    def gas_price(cls, web3):
        return web3.eth.gas_price



