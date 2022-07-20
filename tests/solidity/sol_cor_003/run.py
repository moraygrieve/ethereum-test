import requests, json, secrets
from web3 import Web3
from pysys.basetest import BaseTest
from eth_account.messages import encode_defunct


class PySysTest(BaseTest):
    def execute(self):
        # create the web3 instance
        port = 3000
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:%d' % port))

        # locally generate a private key and it's corresponding account
        private_key = secrets.token_hex(32)
        account = w3.eth.account.privateKeyToAccount(private_key)
        self.log.info('Using account with address %s' % account.address)

        # generate a viewing key for this account, sign and post it to the wallet extension
        response = requests.get('http://127.0.0.1:%d/generateviewingkey/' % port)
        signed_msg = w3.eth.account.sign_message(encode_defunct(text='vk'+response.text), private_key=private_key)

        data = {"address": account.address, "signature": signed_msg.signature.hex()}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post('http://127.0.0.1:%d/submitviewingkey/' % port, data=json.dumps(data), headers=headers)

        # get the balance before adding a viewing key
        balance = w3.eth.get_balance(account.address)
        self.assertTrue(balance == 1000000000000000000000000)
