import json, os, time
from pysys.constants import PROJECT
from ethsys.basetest import EthereumTest
from ethsys.utils.properties import Properties
from ethsys.networks.factory import NetworkFactory
from ethsys.networks.obscuro import Obscuro


class PySysTest(EthereumTest):

    def execute(self):
        # connect to the L1 network (depends on mode)
        l1 = NetworkFactory.get_l1_network(self)
        bridge_address = Properties().management_bridge_address(l1.PROPS_KEY)
        web3_l1, deploy_account = l1.connect_account1()
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract_l1 = web3_l1.eth.contract(address=Properties().l1_jam_token_address(l1.PROPS_KEY), abi=json.load(f))
        deploy_balance_l1_before = contract_l1.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l1_before = contract_l1.functions.balanceOf(bridge_address).call()
        self.log.info('L1 Balances before transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l1_before)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l1_before)

        # connect to the L2 network
        l2 = Obscuro
        web3_l2, deploy_account = l2.connect(Properties().funded_deployment_account_pk(l2.PROPS_KEY), l2.HOST, l2.ACCOUNT1_PORT)
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract_l2 = web3_l2.eth.contract(address=Properties().l2_jam_token_address(l2.PROPS_KEY), abi=json.load(f))
        deploy_balance_l2_before = contract_l2.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l2_before = contract_l2.functions.balanceOf(bridge_address).call()
        self.log.info('L2 Balances before transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l2_before)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l2_before)

        # transfer funds from the deployment address to the bridge address on l1
        l1.transact(self, web3_l1, contract_l1.functions.transfer(bridge_address, 1000), deploy_account, 7200000)

        deploy_balance_l1_after = contract_l1.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l1_after = contract_l1.functions.balanceOf(bridge_address).call()
        self.log.info('L1 Balances after transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l1_after)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l1_after)

        time.sleep(20)
        deploy_balance_l2_after = contract_l2.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l2_after = contract_l2.functions.balanceOf(bridge_address).call()
        self.log.info('L2 Balances after transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l2_after)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l2_after)

        self.assertTrue((bridge_balance_l1_after - bridge_balance_l1_before) == 1000)
        self.assertTrue((deploy_balance_l2_after - deploy_balance_l2_before) == 1000)

        # transfer funds from the deployment address to another account on l2
        _, user_account = l2.connect_account2()
        l2.transact(self, web3_l2, contract_l2.functions.transfer(user_account.address, 50), deploy_account, 7200000)
        user_balance_l2_after = contract_l2.functions.balanceOf(user_account.address).call()
        deploy_balance_l2_after = contract_l2.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l2_after = contract_l2.functions.balanceOf(bridge_address).call()
        self.log.info('L2 Balances after transfer')
        self.log.info('  User   Account balance = %d ' % user_balance_l2_after)
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l2_after)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l2_after)