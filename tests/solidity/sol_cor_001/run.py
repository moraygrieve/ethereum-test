import os
from web3 import Web3
from pysys.basetest import BaseTest
from ethsys.ganache.ganache import GanacheHelper
from ethsys.solidity.compile import SolidityCompiler

class PySysTest(BaseTest):
	def execute(self):
		port=self.getNextAvailableTCPPort()
		GanacheHelper.run(self, port=port)

		# compile the solidity contract
		bytecode, abi = SolidityCompiler.compileFile(os.path.join(self.input, 'Greeter.sol'))

		# construct the web3.py instance
		w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:%d'%port))

		# set pre-funded account as sender
		w3.eth.default_account = w3.eth.accounts[0]

		# create the contract and subit the transaction that deploys it
		greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
		tx_hash = greeter.constructor().transact()

		# wait for the transaction receipt
		tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
		greeter = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
		value = greeter.functions.greet().call()

		# assert the response
		self.assertTrue(value == 'Hello World')

	def validate(self):
		pass
	