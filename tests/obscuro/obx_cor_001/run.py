import json, os
from pysys.constants import PROJECT
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        web3_2, account2 = network.connect_account2()
        web3_1, account1 = network.connect_account1()
        self.log.info('Using account with address %s' % account1.address)

        # grab a handle to the OBX ERC20 contract on the obscuro layer 1
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract = web3_2.eth.contract(address=Properties().l1_obx_token_address(), abi=json.load(f))

        # check initial allocations
        balance1_0 = contract.functions.balanceOf(account1.address).call()
        balance2_0 = contract.functions.balanceOf(account2.address).call()
        self.log.info('Balances before transfer')
        self.log.info('  Account1 balance = %d ' % balance1_0)
        self.log.info('  Account2 balance = %d ' % balance2_0)

        # transfer from account1 into account2
        network.transact(self, web3_1, contract.functions.transfer(account2.address, 200), account1, 7200000)
        balance1_1 = contract.functions.balanceOf(account1.address).call()
        balance2_1 = contract.functions.balanceOf(account2.address).call()
        self.log.info('Balances after transfer')
        self.log.info('  Account1 balance = %d ' % contract.functions.balanceOf(account1.address).call())
        self.log.info('  Account2 balance = %d ' % contract.functions.balanceOf(account2.address).call())
        self.assertTrue((balance1_1 - balance1_0) == -200)
        self.assertTrue((balance2_1 - balance2_0) == 200)
