import os, random
from web3 import Web3
from pysys.basetest import BaseTest
from ethsys.ganache.ganache import GanacheHelper
from ethsys.solidity.compile import SolidityCompiler

class PySysTest(BaseTest):
	def execute(self):
		port=self.getNextAvailableTCPPort()
		GanacheHelper.run(self, port=port)

		# compile the solidity contract
		bytecode, abi = SolidityCompiler.compileFile(os.path.join(self.input, 'Guesser.sol'))

		# construct the web3.py instance
		w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:%d'%port))

		# set pre-funded account as sender
		w3.eth.default_account = w3.eth.accounts[0]

		# create the contract and subit the transaction that deploys it
		guesser = w3.eth.contract(abi=abi, bytecode=bytecode)
		tx_hash = guesser.constructor().transact()

		# wait for the transaction receipt
		tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
		guesser = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)

		upper=100;
		lower=0;

		while True:
			guess=random.randrange(lower, upper)
			value = guesser.functions.guess(guess).call()
			if value == 1:
				self.log.info("Guess is %d, need to go higher" % guess)
				lower = guess+1
			elif value == -1:
				self.log.info("Guess is %d, need to go lower" % guess)
				upper = guess
			else:
				self.log.info("You've guessed it!")
				break

	def validate(self):
		pass
	