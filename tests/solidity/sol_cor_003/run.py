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
		bytecode, abi = SolidityCompiler.compileFile(os.path.join(self.input, 'Incrementer.sol'))

		# construct the web3.py instance
		w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/266273d6b9a544f3ad56c725f38dfd56'))


	def validate(self):
		pass
	