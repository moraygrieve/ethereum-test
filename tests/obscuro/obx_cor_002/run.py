import json, os, time
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
        web3_user, game_user = l2.connect(Properties().gameuserpk(), l2.HOST, l2.ACCOUNT1_PORT)
        self.log.info('Game user account is %s' % game_user.address)

        # the user needs to get the token and game contracts to interact with them
        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            obxt_contract = web3_user.eth.contract(address=obxt_add, abi=json.load(f))

        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'guesser', 'guessing_game.abi')) as f:
            game_contract = web3_user.eth.contract(address=game_add, abi=json.load(f))

        self.log_balances(obxt_contract, game_contract, depl_account.address, game_user.address, game_add)

        # the user starts making guesses (first needs to approve the game to take tokens)
        for i in range(40, 50):
            self.log.info('Guessing number as %d' % i)
            l2.transact(self, web3_user, obxt_contract.functions.approve(game_add, 1), game_user, 720000 * 4)
            l2.transact(self, web3_user, game_contract.functions.attempt(i), game_user, 720000 * 4)
            prize = self.log_balances(obxt_contract, game_contract, depl_account.address, game_user.address,
                                      game_add)
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
