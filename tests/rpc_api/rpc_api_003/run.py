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

        # get the chain id
        chain_id = w3.eth.chain_id
        self.log.info('Chain id is %d' % chain_id)
        self.assertTrue(chain_id == 777)

        # get the block number
        block_number = w3.eth.get_block_number()
        self.log.info('Block number is %d' % block_number)
        self.assertTrue(block_number > 0)

        # get the balance
        balance = w3.eth.get_balance(account.address)
        self.log.info('Balance for new accounts is %d' % balance)
        self.assertTrue(balance == 1000000000000000000000000)

        # get block by number
        block = w3.eth.get_block(block_number)
        self.log.info('Block %s' % block)
        self.log.info('Block has number %s' % block.number)
        self.assertTrue(block.number == block_number)

        # get block by hash
        block = w3.eth.get_block(block.parenthash)
        self.log.info('Block has number %s' % block.number)
        self.assertTrue(block.number == block_number-1)

        # get gas price
        gas_price = w3.eth.gas_price
        self.log.info('Gas price is %s' % gas_price)
        self.assertTrue(gas_price == 0)
