import json, os
from pysys.constants import PROJECT
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties
from ethsys.networks.obscuro import ObscuroNetwork, ObscuroL1


class PySysTest(BaseTest):

    def execute(self):
        # connect to the network
        l1 = ObscuroL1
        bridge_address = Properties().management_bridge_address(l1.PROPS_KEY)
        web3_2, faucet_account = l1.connect_account2()
        web3_1, deploy_account = l1.connect_account1()
        self.log.info('Deploy Account address %s' % deploy_account.address)
        self.log.info('Faucet Account address %s' % faucet_account.address)
        self.log.info('Bridge Address address %s' % bridge_address)

        # grab a handle to the OBX ERC20 contract on the obscuro layer 1
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract = web3_1.eth.contract(address=Properties().l1_obx_token_address(l1.PROPS_KEY), abi=json.load(f))

        # check initial allocations
        balance1_0 = contract.functions.balanceOf(deploy_account.address).call()
        balance2_0 = contract.functions.balanceOf(faucet_account.address).call()
        self.log.info('Balances before transfer')
        self.log.info('  Deploy Account balance = %d ' % balance1_0)
        self.log.info('  Faucet Account balance = %d ' % balance2_0)

        # transfer from deploy_account into faucet_account
        l1.transact(self, web3_1, contract.functions.transfer(faucet_account.address, 1000), deploy_account, 7200000)
        balance1_1 = contract.functions.balanceOf(deploy_account.address).call()
        balance2_1 = contract.functions.balanceOf(faucet_account.address).call()
        self.log.info('Balances after transfer')
        self.log.info('  Deploy Account balance = %d ' % balance1_1)
        self.log.info('  Faucet Account balance = %d ' % balance2_1)
        self.assertTrue((balance1_1 - balance1_0) == -1000)
        self.assertTrue((balance2_1 - balance2_0) == 1000)

        # transfer from deploy_account into bridge_address
        l1.transact(self, web3_1, contract.functions.transfer(bridge_address, 1000), deploy_account, 7200000)
        balance1_2 = contract.functions.balanceOf(deploy_account.address).call()
        balance2_2 = contract.functions.balanceOf(bridge_address).call()
        self.log.info('Balances after transfer')
        self.log.info('  Deploy Account balance = %d ' % balance1_2)
        self.log.info('  Bridge Address balance = %d ' % balance2_2)
