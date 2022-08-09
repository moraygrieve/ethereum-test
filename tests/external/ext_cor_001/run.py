from ethsys.basetest import EthereumTest
from ethsys.external.contracts.guesser.guesser import GuessingGame
from ethsys.networks.factory import NetworkFactory


class PySysTest(EthereumTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        web3_1, account_1 = network.connect_account1()
        web3_2, account_2 = network.connect_account2()
        self.log.info('Using account with address %s' % account_1.address)

        # create the game python wrapper
        guesser = GuessingGame(self, web3_1)

        # deploy the ERC20 basic contract
        self.log.info('Deploy the ERC20Basic contract')
        erc20_contract = guesser.construct_erc20_basic()
        tx_receipt = network.transact(self, web3_1, erc20_contract, account_1, guesser.GAS)
        erc20_address = tx_receipt.contractAddress
        erc20_contract = web3_1.eth.contract(address=erc20_address, abi=guesser.erc20_abi)

        # deploy the guessing game contract
        self.log.info('Deploy the guessing contract')
        guessing_contract = guesser.construct_guesser(10, erc20_address)
        tx_receipt = network.transact(self, web3_1, guessing_contract, account_1, guesser.GAS)
        guessing_address = tx_receipt.contractAddress
        guessing_contract = web3_1.eth.contract(address=guessing_address, abi=guesser.guessing_abi)

        # allocate funds to account2 and check their balance
        network.transact(self, web3_1, erc20_contract.functions.transfer(account_2.address, 2000), account_1, guesser.GAS)
        self.assertTrue(erc20_contract.functions.balanceOf(account_2.address).call() == 2000)

        # account2 approves account1 1 token
        network.transact(self, web3_2, erc20_contract.functions.approve(guessing_address, 1), account_2, guesser.GAS)
        self.assertTrue(erc20_contract.functions.allowance(account_2.address, guessing_address).call() == 1)
        self.assertTrue(guessing_contract.functions.getBalance().call() == 0)

        # make a guess
        network.transact(self, web3_2, guessing_contract.functions.attempt(35), account_2, guesser.GAS)
        self.assertTrue(erc20_contract.functions.allowance(account_2.address, guessing_address).call() == 0)
        self.assertTrue(guessing_contract.functions.getBalance().call() == 1)

        for i in range(1,10):
            self.log.info('Guessing number as %d' % i)
            network.transact(self, web3_2, erc20_contract.functions.approve(guessing_address, 1), account_2, guesser.GAS)
            network.transact(self, web3_2, guessing_contract.functions.attempt(i), account_2, guesser.GAS)
            balance = guessing_contract.functions.getBalance().call()
            self.log.info('Games balance is %d' % guessing_contract.functions.getBalance().call())
            if balance == 0:
                self.log.info('Won the prize with a guess of %d' % i)
                self.assertTrue(erc20_contract.functions.balanceOf(account_2.address).call() == 2000)
                break
