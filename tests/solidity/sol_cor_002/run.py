from web3 import Web3
from pysys.basetest import BaseTest
from ethsys.ganache.ganache import GanacheHelper
from ethsys.contracts.guesser import Guesser

class PySysTest(BaseTest):
	def execute(self):
		# run ganache
		port = self.getNextAvailableTCPPort()
		GanacheHelper.run(self, port=port)

		# connect to the network and get the account
		w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:%d'%port))
		w3.eth.default_account = w3.eth.accounts[0]

		# create guesser abstraction, compile and deploy
		guesser = Guesser(self, 0, 100)
		bytecode, abi = guesser.compile()
		contract = w3.eth.contract(abi=abi, bytecode=bytecode)
		transaction = contract.constructor(guesser.secret).transact()

		# wait for the transaction receipt then get the actual contract from the blockchain
		tx_receipt = w3.eth.wait_for_transaction_receipt(transaction)
		contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

		# make the guess until we get the right number
		guesser.guess(contract)

	def validate(self):
		pass
	