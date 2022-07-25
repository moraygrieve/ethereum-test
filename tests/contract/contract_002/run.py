from pysys.basetest import BaseTest
from ethsys.contracts.guesser import Guesser
from ethsys.networks.ropsten import RopstenNetwork


class PySysTest(BaseTest):

    def execute(self):
        network = RopstenNetwork

        # connect to the network, create a local private key and convert into the account
        web3, private_key, account = network.connect(self)
        self.log.info('Using account with address %s' % account.address)

        # compile the guessing game and build the deployment transaction
        self.log.info('Compiling the guessing game application')
        guesser = Guesser(self, web3, 0, 100)
        build_tx = network.buildTransaction(self, web3, guesser.contract, account)

        # Sign the transaction and send to the network
        self.log.info('Signing and sending raw transaction')
        send_tx = network.sendRawTransaction(self, web3, account, build_tx)

        # wait for the transaction receipt and check the status
        self.log.info('Waiting for the send transaction')
        tx_receipt = network.waitForTransaction(self, web3, send_tx)

        # construct the contract using the contract address
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=guesser.abi)

        # guess the number
        self.log.info('Starting guessing game')
        self.assertTrue(guesser.guess(contract) == guesser.secret)





# import secrets
# from web3 import Web3
# from pysys.constants import *
# from pysys.basetest import BaseTest
# from ethsys.utils.properties import Properties
# from ethsys.contracts.guesser import Guesser
#
#
# class PySysTest(BaseTest):
#
#     def __init__(self, descriptor, outsubdir, runner):
#         super().__init__(descriptor, outsubdir, runner)
#         self.guesser = Guesser(self, 0, 100)
#
#     def execute(self):
#
#         # connect to the network, create a local private key and convert into the account
#         w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/%s' % Properties().infuraProjectID()))
#         private_key = Properties().privateKey()
#         account = w3.eth.account.privateKeyToAccount(private_key)
#         self.log.info('Using account with address %s' % account.address)
#
#         # compile the guessing game and build the deployment transaction
#         self.log.info('Compiling the guessing game application')
#         bytecode, abi = self.guesser.compile()
#         contract = w3.eth.contract(abi=abi, bytecode=bytecode)
#         build_tx = contract.constructor(self.guesser.secret).buildTransaction(
#             {
#                 'from': account.address,
#                 'nonce': w3.eth.getTransactionCount(account.address),
#                 'gasPrice': w3.eth.gasPrice,
#                 'gas': 720000,
#                 'chainId': 3
#             }
#         )
#
#         # Sign the transaction and send to the network
#         self.log.info('Signing and sending raw transaction')
#         signed_tx = account.signTransaction(build_tx)
#         tx_hash = None
#         try:
#             tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#         except Exception as e:
#             self.log.error('Error sending raw transaction %s' % e)
#             self.addOutcome(BLOCKED, abortOnError=TRUE)
#
#         # wait for the transaction receipt and check the status
#         self.log.info('Waiting for transaction receipt')
#         tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#         if tx_receipt.status == 0:
#             self.log.error('Transaction receipt has failed status ... aborting')
#             self.addOutcome(BLOCKED, abortOnError=TRUE)
#
#         # construct the contract using the contract address
#         contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#
#         # guess the number
#         self.log.info('Starting guessing game')
#         self.guessed_value = self.guesser.guess(contract)
#
#
#     def validate(self):
#         self.assertTrue(self.guessed_value == self.guesser.secret)
