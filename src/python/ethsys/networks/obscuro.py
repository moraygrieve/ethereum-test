import secrets, requests, time, json
from web3 import Web3
from eth_account.messages import encode_defunct
from pysys.constants import *
from ethsys.networks.default import DefaultNetwork


class ObscuroNetwork(DefaultNetwork):

    @classmethod
    def init(cls, test):
        return None, '127.0.0.1', 3000

    @classmethod
    def connect(cls, test, host, port):
        web3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        private_key = secrets.token_hex(32)
        account = web3.eth.account.privateKeyToAccount(private_key)

        # generate a viewing key for this account, sign and post it to the wallet extension
        response = requests.get('http://%s:%d/generateviewingkey/' % (host, port))
        signed_msg = web3.eth.account.sign_message(encode_defunct(text='vk' + response.text), private_key=private_key)

        data = {"address": account.address, "signature": signed_msg.signature.hex()}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post('http://%s:%d/submitviewingkey/' % (host, port), data=json.dumps(data), headers=headers)
        return web3, account

    @classmethod
    def chain_id(cls):
        return 777

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
