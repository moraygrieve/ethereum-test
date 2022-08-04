import json, os, time
from pysys.constants import PROJECT, TIMEDOUT
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties
from ethsys.networks.obscuro import ObscuroNetwork, ObscuroL1


class PySysTest(BaseTest):

    def execute(self):
        # connect to the L1 network
        l1 = ObscuroL1
        bridge_address = Properties().management_bridge_address(l1.PROPS_KEY)
        web3_1, deploy_account = l1.connect_account1()
        self.log.info('Deploy Account address %s' % deploy_account.address)
        self.log.info('Bridge Address address %s' % bridge_address)

        # grab a handle to the OBX ERC20 contract on the obscuro layer 1
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract = web3_1.eth.contract(address=Properties().l1_obx_token_address(l1.PROPS_KEY), abi=json.load(f))

        # check initial allocations
        deploy_balance_l1 = contract.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l1 = contract.functions.balanceOf(bridge_address).call()
        self.log.info('L1 Balances before transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l1)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l1)

        # transfer from deploy_account into bridge_address
        l1.transact(self, web3_1, contract.functions.transfer(bridge_address, 1000), deploy_account, 7200000)
        deploy_balance_l1 = contract.functions.balanceOf(deploy_account.address).call()
        bridge_balance_l1 = contract.functions.balanceOf(bridge_address).call()
        self.log.info('L1 Balances after transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l1)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l1)

        # connect to the L2 network
        l2 = ObscuroNetwork
        web3_2, deploy_account = l2.connect(Properties().funded_deployment_account_pk(l2.PROPS_KEY), l2.HOST, l2.ACCOUNT1_PORT)

        # grab a handle to the OBX ERC20 contract on the obscuro layer 2
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract = web3_2.eth.contract(address=Properties().l2_obx_token_address(l2.PROPS_KEY), abi=json.load(f))

        # check initial allocations
        now = time.time()
        deploy_balance_l2 = 0
        bridge_balance_l2 = 0
        while deploy_balance_l2 != bridge_balance_l1:
            deploy_balance_l2 = contract.functions.balanceOf(deploy_account.address).call()
            bridge_balance_l2 = contract.functions.balanceOf(bridge_address).call()
            time.sleep(1)
            if (time.time() - now) > 20: self.addOutcome(TIMEDOUT, abortOnError=True)

        self.log.info('L2 Balances after transfer')
        self.log.info('  Deploy Account balance = %d ' % deploy_balance_l2)
        self.log.info('  Bridge Address balance = %d ' % bridge_balance_l2)
        self.assertTrue(deploy_balance_l2 == bridge_balance_l1)