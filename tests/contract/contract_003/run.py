import secrets, requests, json, time
from web3 import Web3
from pysys.constants import *
from pysys.basetest import BaseTest
from ethsys.contracts.guesser import Guesser
from eth_account.messages import encode_defunct


class PySysTest(BaseTest):

    def __init__(self, descriptor, outsubdir, runner):
        super().__init__(descriptor, outsubdir, runner)
        self.guesser = Guesser(self, 0, 100)

    def execute(self):

        # connect to the network, create a local private key and convert into the account
        port = 3000
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:%d' % port))
        private_key = secrets.token_hex(32)
        account = w3.eth.account.privateKeyToAccount(private_key)
        self.log.info('Using account with address %s' % account.address)

        # generate a viewing key for this account, sign and post it to the wallet extension
        response = requests.get('http://127.0.0.1:%d/generateviewingkey/' % port)
        signed_msg = w3.eth.account.sign_message(encode_defunct(text='vk' + response.text), private_key=private_key)

        data = {"address": account.address, "signature": signed_msg.signature.hex()}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        requests.post('http://127.0.0.1:%d/submitviewingkey/' % port, data=json.dumps(data), headers=headers)

        # compile the guessing game and build the deployment transaction
        self.log.info('Compiling the guessing game application')
        bytecode, abi = self.guesser.compile()
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        build_tx = contract.constructor(self.guesser.secret).buildTransaction(
            {
                'from': account.address,
                'nonce': w3.eth.getTransactionCount(account.address),
                'gasPrice': 1499934385,
                'gas': 720000,
                'chainId': 777
            }
        )

        # Sign the transaction and send to the network
        self.log.info('Signing and sending raw transaction')
        signed_tx = account.signTransaction(build_tx)
        tx_hash = None
        try:
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        except Exception as e:
            self.log.error('Error sending raw transaction %s' % e)
            self.addOutcome(BLOCKED, abortOnError=TRUE)

        # wait for the transaction receipt and check the status
        self.log.info('Waiting for transaction receipt')
        start = time.time()
        tx_receipt = None
        while True:
            if (time.time() - start) > 60:
                self.log.error('Timed out waiting for transaction receipt ... aborting')
                self.addOutcome(TIMEDOUT, abortOnError=TRUE)

            try:
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                if tx_receipt.status == 0:
                    self.log.error('Transaction receipt has failed status ... aborting')
                    self.addOutcome(BLOCKED, abortOnError=TRUE)
                else:
                    self.log.info('Received transaction receipt')
                    break
            except Exception as e:
                self.log.warn('Error waiting for transaction receipt %s' % e)
                time.sleep(1)

        # construct the contract using the contract address
        contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

        # guess the number
        self.log.info('Starting guessing game')
        self.guessed_value = self.guesser.guess(contract)

    def validate(self):
        self.assertTrue(self.guessed_value == self.guesser.secret)
