import json, os
from pysys.constants import PROJECT
from ethsys.basetest import EthereumTest
from ethsys.utils.properties import Properties
from ethsys.networks.obscuro import Obscuro


class PySysTest(EthereumTest):
    USERS = {
        'MATT':'0x686Ad719004590e98F182feA3516d443780C64a1',
        'GAVIN':'0x85E1Cc949Bca27912e3e951ad1F68afD1cc4aB15',
        'MORAY':'0x7719A2b2BeC6a98508975C168A565FffCF9Dc266',
        'TUDOR':'0xD993601a218fB40147328ac8BCF086Dcc6eb3867',
        'CAIS':'0x6Bd7B418C4f4e944571F8EE4D7DBD5E44279d579'
    }
    AMOUNT = 50
    DISPLAY_ONLY = False

    def execute(self):
        # connect to the L2 network
        l2 = Obscuro
        web3_l2, deploy_account = l2.connect(Properties().funded_deployment_account_pk(l2.PROPS_KEY), l2.HOST,
                                             l2.ACCOUNT1_PORT)
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            jam_cntr = web3_l2.eth.contract(address=Properties().l2_jam_token_address(l2.PROPS_KEY), abi=json.load(f))

        # run for users
        for user in self.USERS.keys():
            user_address = self.USERS[user]
            self.log.info('Running for user %s [%s]' % (user, self.USERS[user]))

            # balance before transaction
            user_balance = jam_cntr.functions.balanceOf(user_address).call()
            deploy_balance = jam_cntr.functions.balanceOf(deploy_account.address).call()
            self.log.info('  L2 balances')
            self.log.info('    User balance = %d ' % user_balance)
            self.log.info('    Deploy account balance = %d ' % deploy_balance)

            if self.DISPLAY_ONLY: continue

            # transfer funds from the deployment address to the user account
            if user_balance == 0:
                self.log.info('User requests funds ... transferring %d' % self.AMOUNT)
                l2.transact(self, web3_l2, jam_cntr.functions.transfer(user_address, self.AMOUNT), deploy_account, 7200000)

                # balance after transaction
                user_balance = jam_cntr.functions.balanceOf(user_address).call()
                deploy_balance = jam_cntr.functions.balanceOf(deploy_account.address).call()
                self.log.info('  L2 balances')
                self.log.info('    User balance = %d ' % user_balance)
                self.log.info('    Deploy account balance = %d ' % deploy_balance)
            else:
                self.log.info('%s has funds so not transferring any more ' % user)
            self.log.info('  ')