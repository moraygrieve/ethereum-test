import json, os
from pysys.constants import PROJECT
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties
from ethsys.networks.obscuro import ObscuroNetwork


class PySysTest(BaseTest):
    USERS = {
        'MATT':'0x686Ad719004590e98F182feA3516d443780C64a1',
        'GAVIN_OLD':'0x6D0c4F15c048Efef3656F77e393C8cc149aE9262',
        'GAVIN':'0x85E1Cc949Bca27912e3e951ad1F68afD1cc4aB15'
    }
    AMOUNT = 50

    def execute(self):
        # connect to the L2 network
        l2 = ObscuroNetwork
        web3_l2, deploy_account = l2.connect(Properties().funded_deployment_account_pk(l2.PROPS_KEY), l2.HOST,
                                             l2.ACCOUNT1_PORT)
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            obx_cntr = web3_l2.eth.contract(address=Properties().l2_obx_token_address(l2.PROPS_KEY), abi=json.load(f))

        # run for users
        for user in self.USERS.keys():
            user_address = self.USERS[user]
            self.log.info('Running for user %s [%s]' % (user, self.USERS[user]))

            # balance before transaction
            user_balance = obx_cntr.functions.balanceOf(user_address).call()
            deploy_balance = obx_cntr.functions.balanceOf(deploy_account.address).call()
            self.log.info('  L2 balances before transfer')
            self.log.info('    User balance = %d ' % user_balance)
            self.log.info('    Deploy account balance = %d ' % deploy_balance)

            # transfer funds from the deployment address to the user account
            if user_balance == 0:
                self.log.info('User requests funds ... transferring %d' % self.AMOUNT)
                l2.transact(self, web3_l2, obx_cntr.functions.transfer(user_address, self.AMOUNT), deploy_account, 7200000)

                # balance after transaction
                user_balance = obx_cntr.functions.balanceOf(user_address).call()
                deploy_balance = obx_cntr.functions.balanceOf(deploy_account.address).call()
                self.log.info('  L2 balances after transfer')
                self.log.info('    User balance = %d ' % user_balance)
                self.log.info('    Deploy account balance = %d ' % deploy_balance)
            else:
                self.log.info('  User has funds so not transferring any more')
            self.log.info('  ')