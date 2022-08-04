# import json, os
# from pysys.constants import PROJECT
# from pysys.basetest import BaseTest
# from ethsys.utils.properties import Properties
# from ethsys.networks.obscuro import ObscuroNetwork
#
#
# class PySysTest(BaseTest):
#
#     def execute(self):
#         # connect to the L2 network
#         l2 = ObscuroNetwork
#         game_address = Properties().guessing_game_address(l2.PROPS_KEY)
#         token_address = Properties().l2_obx_token_address(l2.PROPS_KEY)
#         web3_depl, deploy_account = l2.connect(Properties().funded_deployment_account_pk(l2.PROPS_KEY), l2.HOST, l2.ACCOUNT1_PORT)
#         web3_user, user_account = l2.connect_account2()
#
#         # create the contracts from their addresses and abi (OBX token and guessing game)
#         with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
#             token_l2 = web3_user.eth.contract(address=token_address, abi=json.load(f))
#
#         with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'guesser', 'guessing_game.abi')) as f:
#             contract_l2 = web3_user.eth.contract(address=game_address, abi=json.load(f))
#
#
#
#         for i in range(1,10):
#             self.log.info('Guessing number as %d' % i)
#             l2.transact(self, web3_user, token_l2.functions.approve(game_address, 1), user_account, 720000 * 4)
#             l2.transact(self, web3_user, contract_l2.functions.attempt(i), user_account, 720000 * 4)
#             prize = contract_l2.functions.getBalance().call()
#             depl_balance = token_l2.functions.balanceOf(deploy_account.address).call()
#             user_balance = token_l2.functions.balanceOf(user_account.address).call()
#             game_balance = token_l2.functions.balanceOf(game_address).call()
#             self.log.info('Prize fund stands at %d' % prize)
#             self.log.info('Token balances')
#             self.log.info('  Depl balance = %d ' % depl_balance)
#             self.log.info('  User balance = %d ' % user_balance)
#             self.log.info('  Game balance = %d ' % game_balance)
#
#             if balance == 0:
#                 self.log.info('Won the prize with a guess of %d' % i)
#                 break
#


import json, os
from pysys.constants import PROJECT
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties
from ethsys.networks.obscuro import ObscuroNetwork


class PySysTest(BaseTest):

    def execute(self):
        # get the game address and the obx token address from the properties
        l2 = ObscuroNetwork
        game_add = Properties().guessing_game_address(l2.PROPS_KEY)
        obxt_add = Properties().l2_obx_token_address(l2.PROPS_KEY)

        # get the connections for the deployment (faucet) and game user
        _, depl_account = l2.connect(Properties().funded_deployment_account_pk(l2.PROPS_KEY), l2.HOST, l2.ACCOUNT1_PORT)
        web3_user, user_account = l2.connect_account2()

        # the user needs to get the token and game contracts to interact with them
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            obxt_contract = web3_user.eth.contract(address=obxt_add, abi=json.load(f))

        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'guesser', 'guessing_game.abi')) as f:
            game_contract = web3_user.eth.contract(address=game_add, abi=json.load(f))

        self.log_balances(obxt_contract, game_contract, depl_account.address, user_account.address, game_add)

        # the user starts making guesses (first needs to approve the game to take tokens)
        for i in range(1,10):
            self.log.info('Guessing number as %d' % i)
            l2.transact(self, web3_user, obxt_contract.functions.approve(game_add, 1), user_account, 720000 * 4)
            l2.transact(self, web3_user, game_contract.functions.attempt(i), user_account, 720000 * 4)
            prize = self.log_balances(obxt_contract, game_contract, depl_account.address, user_account.address, game_add)
            if prize == 0:
                self.log.info('Won the prize with a guess of %d' % i)
                break

    def log_balances(self, token, game, depl_add, user_add, game_add):
        prize = game.functions.getBalance().call()
        depl_balance = token.functions.balanceOf(depl_add).call()
        user_balance = token.functions.balanceOf(user_add).call()
        game_balance = token.functions.balanceOf(game_add).call()
        self.log.info('Prize fund stands at %d' % prize)
        self.log.info('Token balances')
        self.log.info('  Depl balance = %d ' % depl_balance)
        self.log.info('  User balance = %d ' % user_balance)
        self.log.info('  Game balance = %d ' % game_balance)
        return prize