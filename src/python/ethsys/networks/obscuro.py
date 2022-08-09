import requests, time, json
from web3 import Web3
from pysys.constants import *
from ethsys.networks.default import Default
from ethsys.utils.properties import Properties
from ethsys.networks.geth import Geth
from eth_account.messages import encode_defunct


class ObscuroL1(Geth):
    HOST = 'testnet-gethnetwork.uksouth.azurecontainer.io'
    PORT = 8025
    PROPS_KEY = 'obscuro'

    @classmethod
    def connect_account1(cls):
        return cls.connect(Properties().funded_deployment_account_pk(cls.PROPS_KEY), cls.HOST, cls.PORT)


class ObscuroL1Local(Geth):
    HOST = '127.0.0.1'
    PORT = 8025
    PROPS_KEY = 'obscuro.local'

    @classmethod
    def connect_account1(cls):
        return cls.connect(Properties().funded_deployment_account_pk(cls.PROPS_KEY), cls.HOST, cls.PORT)


class Obscuro(Default):
    """The Obscuro wallet extension giving access to the underlying network."""
    HOST = '127.0.0.1'
    ACCOUNT1_PORT = 3000
    ACCOUNT2_PORT = 4000
    ACCOUNT3_PORT = 5000
    PROPS_KEY = 'obscuro'

    @classmethod
    def chain_id(cls):
        return 777

    @classmethod
    def connect(cls, private_key, host, port):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        account = web3.eth.account.privateKeyToAccount(private_key)
        cls.__generate_viewing_key(web3, host, port, account, private_key)
        return web3, account

    @classmethod
    def connect_account1(cls):
        return cls.connect(Properties().account1pk(), cls.HOST, cls.ACCOUNT1_PORT)

    @classmethod
    def connect_account2(cls):
        return cls.connect(Properties().account2pk(), cls.HOST, cls.ACCOUNT2_PORT)

    @classmethod
    def connect_account3(cls):
        return cls.connect(Properties().account3pk(), cls.HOST, cls.ACCOUNT3_PORT)

    @classmethod
    def wait_for_transaction(cls, test, web3, tx_hash):
        start = time.time()
        tx_receipt = None
        while tx_receipt is None:
            if (time.time() - start) > 120:
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
    def __generate_viewing_key(cls, web3, host, port, account, private_key):
        # generate a viewing key for this account, sign and post it to the wallet extension
        response = requests.get('http://%s:%d/generateviewingkey/' % (host, port))
        signed_msg = web3.eth.account.sign_message(encode_defunct(text='vk' + response.text), private_key=private_key)

        data = {"address": account.address, "signature": signed_msg.signature.hex()}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post('http://%s:%d/submitviewingkey/' % (host, port), data=json.dumps(data), headers=headers)
