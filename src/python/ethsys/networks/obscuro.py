import requests, time, json
from web3 import Web3
from pysys.constants import *
from ethsys.networks.default import DefaultNetwork
from ethsys.utils.properties import Properties
from eth_account.messages import encode_defunct

class ObscuroNetwork(DefaultNetwork):
    HOST = '127.0.0.1'
    OWNER1_PORT = 3000
    ACCOUNT1_PORT = 4000
    ACCOUNT2_PORT = 5000

    @classmethod
    def connect_owner(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.OWNER1_PORT)))
        private_key = Properties().ownerPK()
        account = web3.eth.account.privateKeyToAccount(private_key)
        cls.__generateViewingKey(web3, cls.HOST, cls.OWNER1_PORT, account, private_key)
        return web3, account

    @classmethod
    def connect_account1(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.ACCOUNT1_PORT)))
        private_key = Properties().account1PK()
        account = web3.eth.account.privateKeyToAccount(private_key)
        cls.__generateViewingKey(web3, cls.HOST, cls.ACCOUNT1_PORT, account, private_key)
        return web3, account

    @classmethod
    def connect_account2(cls):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (cls.HOST, cls.ACCOUNT2_PORT)))
        private_key = Properties().account2PK()
        account = web3.eth.account.privateKeyToAccount(private_key)
        cls.__generateViewingKey(web3, cls.HOST, cls.ACCOUNT2_PORT, account, private_key)
        return web3, account

    @classmethod
    def chain_id(cls):
        return 777

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
                'gasPrice': 1499934385,
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
        start = time.time()
        tx_receipt = None
        while tx_receipt is None:
            if (time.time() - start) > 60:
                test.log.error('Timed out waiting for transaction receipt ... aborting')
                test.addOutcome(TIMEDOUT, abortOnError=TRUE)

            try:
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            except Exception as e:
                time.sleep(1)

        if tx_receipt.status == 1:
            test.log.info('Transaction complete gasUsed=%d' % tx_receipt.gasUsed)
            test.log.info('Transaction receipt block hash %s' % tx_receipt.blockHash.hex())
        else:
            test.log.error('Transaction receipt failed')
            test.log.error('Full receipt: %s' % tx_receipt)
            test.addOutcome(FAILED, abortOnError=TRUE)
        return tx_receipt

    @classmethod
    def __generateViewingKey(cls, web3, host, port, account, private_key):
        # generate a viewing key for this account, sign and post it to the wallet extension
        response = requests.get('http://%s:%d/generateviewingkey/' % (host, port))
        signed_msg = web3.eth.account.sign_message(encode_defunct(text='vk' + response.text), private_key=private_key)

        data = {"address": account.address, "signature": signed_msg.signature.hex()}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post('http://%s:%d/submitviewingkey/' % (host, port), data=json.dumps(data), headers=headers)
