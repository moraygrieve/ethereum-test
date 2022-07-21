from web3 import Web3
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties


class PySysTest(BaseTest):
	def execute(self):
		props = Properties()

		# connect to the network and get the account
		w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/%s' % props.infuraProjectID()))
		account = w3.eth.account.privateKeyToAccount(props.privateKey())
		self.log.info('Using account with address %s' % account.address)

		# get the chain id
		chain_id = w3.eth.chain_id
		self.log.info('Chain id is %d' % chain_id)
		self.assertTrue(chain_id == 3)

		# get the block number
		block_number = w3.eth.get_block_number()
		self.log.info('Block number is %d' % block_number)
		self.assertTrue(block_number > 0)

		# get the balance
		balance = w3.eth.get_balance(account.address)
		self.log.info('Balance for new accounts is %d' % balance)
		self.assertTrue(balance >= 0)

		# get block by number
		block = w3.eth.get_block(block_number)
		self.log.info('Block %s' % block)
		self.log.info('Block has number %s' % block.number)
		self.assertTrue(block.number == block_number)

		# get block by hash
		block = w3.eth.get_block(block.parentHash)
		self.log.info('Block has number %s' % block.number)
		self.assertTrue(block.number == block_number-1)

		# get gas price
		gas_price = w3.eth.gas_price
		self.log.info('Gas price is %s' % gas_price)
		self.assertTrue(gas_price >= 0)


