import json
from pysys.constants import *
from pysys.basetest import BaseTest
from ethsys.contracts.erc20.obx import OBXCoin
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        web3_2, account2 = network.connect_account2()
        web3_1, account1 = network.connect_account1()
        self.log.info('Using account with address %s' % account1.address)

        # deploy the contract
        self.log.info('Deploy the OBXCoin contract')
        erc20 = OBXCoin(self, web3_1)
        tx_receipt = network.transact(self, web3_1, erc20.contract, account1, erc20.GAS)

        # check for contract deployment and get a reference for account1 using the compiled abi
        self.log.info('Check to see if the contract is deployed using compiled abi')
        contract1 = web3_1.eth.contract(address=tx_receipt.contractAddress, abi=erc20.abi)
        bytecode1 = web3_2.eth.getCode(tx_receipt.contractAddress)
        self.assertTrue(bytecode1 != b'')
        self.assertTrue(contract1.functions.balanceOf(account1.address).call() == 1000000)

        # transfer some money into account2
        network.transact(self, web3_1, contract1.functions.transfer(account2.address, 200), account1, erc20.GAS)

        # check for contract deployment and get a reference for account2 using the json abi
        self.log.info('Check to see if the contract is deployed using json abi')
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract2 = web3_2.eth.contract(address=tx_receipt.contractAddress, abi=json.load(f))
            bytecode2 = web3_2.eth.getCode(tx_receipt.contractAddress)
            self.assertTrue(bytecode2 != b'')
            self.assertTrue(bytecode2 == bytecode1)
            self.assertTrue(contract1.functions.balanceOf(account1.address).call() == 999800)
            self.assertTrue(contract2.functions.balanceOf(account2.address).call() == 200)





