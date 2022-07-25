import secrets, requests, time, json
from web3 import Web3
from eth_account.messages import encode_defunct
from pysys.constants import *

class ObscuroNetwork:

    @classmethod
    def chainID(cls):
        return 777

    @classmethod
    def run(cls):
        raise NotImplementedError

    @classmethod
    def connect(cls, test, host='127.0.0.1', port=3000):
        w3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        private_key = secrets.token_hex(32)
        account = w3.eth.account.privateKeyToAccount(private_key)

        # generate a viewing key for this account, sign and post it to the wallet extension
        response = requests.get('http://%s:%d/generateviewingkey/' % (host, port))
        signed_msg = w3.eth.account.sign_message(encode_defunct(text='vk' + response.text), private_key=private_key)

        data = {"address": account.address, "signature": signed_msg.signature.hex()}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post('http://%s:%d/submitviewingkey/' % (host, port), data=json.dumps(data), headers=headers)

        return (w3, private_key, account)

    @classmethod
    def buildTransaction(cls, test, web3, contract, account):
        return contract.buildTransaction(
            {
                'from': account.address,
                'nonce': web3.eth.getTransactionCount(account.address),
                'gasPrice': 1499934385,
                'gas': 720000,
                'chainId': cls.chainID()
            }
        )

    @classmethod
    def sendRawTransaction(cls, test, web3, account, build_tx):
        signed_tx = account.signTransaction(build_tx)
        tx_hash = None
        try:
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        except Exception as e:
            test.log.error('Error sending raw transaction %s' % e)
            test.addOutcome(BLOCKED, abortOnError=TRUE)
        return tx_hash

    @classmethod
    def waitForTransaction(cls, test, web3, tx_hash):
        start = time.time()
        tx_receipt = None
        while True:
            if (time.time() - start) > 60:
                test.log.error('Timed out waiting for transaction receipt ... aborting')
                test.addOutcome(TIMEDOUT, abortOnError=TRUE)

            try:
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                if tx_receipt.status == 0:
                    test.log.error('Transaction receipt has failed status ... aborting')
                    test.addOutcome(BLOCKED, abortOnError=TRUE)
                else:
                    test.log.info('Received transaction receipt')
                    break
            except Exception as e:
                test.log.warn('Error waiting for transaction receipt %s' % e)
                time.sleep(1)
        return tx_receipt
