from ethsys.basetest import EthereumTest
from ethsys.contracts.erc20.obx import OBXCoin
from ethsys.networks.factory import NetworkFactory


class PySysTest(EthereumTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        web3_3, account3 = network.connect_account3()
        web3_2, account2 = network.connect_account2()
        web3_1, account1 = network.connect_account1()
        self.log.info('Using account with address %s' % account1.address)

        # deploy the contract
        self.log.info('Deploy the OBXCoin contract')
        erc20 = OBXCoin(self, web3_1)
        tx_receipt = network.transact(self, web3_1, erc20.contract, account1, erc20.GAS)

        # construct contract instance
        self.log.info('Construct an instance using the contract address and abi')
        self.log.info('Contract address is %s' % tx_receipt.contractAddress)

        contract = web3_1.eth.contract(address=tx_receipt.contractAddress, abi=erc20.abi)

        # check initial allocations
        self.log.info('Balances before transfer')
        self.log.info('  Account1 balance = %d ' % contract.functions.balanceOf(account1.address).call())
        self.log.info('  Account2 balance = %d ' % contract.functions.balanceOf(account2.address).call())
        self.log.info('  Account3 balance = %d ' % contract.functions.balanceOf(account3.address).call())
        self.assertTrue(contract.functions.balanceOf(account1.address).call() == 1000000)
        self.assertTrue(contract.functions.balanceOf(account2.address).call() == 0)
        self.assertTrue(contract.functions.balanceOf(account3.address).call() == 0)

        # transfer from account1 into account2
        network.transact(self, web3_1, contract.functions.transfer(account2.address, 200), account1, erc20.GAS)
        self.log.info('Balances after transfer')
        self.log.info('  Account1 balance = %d ' % contract.functions.balanceOf(account1.address).call())
        self.log.info('  Account2 balance = %d ' % contract.functions.balanceOf(account2.address).call())
        self.log.info('  Account3 balance = %d ' % contract.functions.balanceOf(account3.address).call())
        self.assertTrue(contract.functions.balanceOf(account1.address).call() == 999800)
        self.assertTrue(contract.functions.balanceOf(account2.address).call() == 200)
        self.assertTrue(contract.functions.balanceOf(account3.address).call() == 0)

        # account1 approves account2 to withdraw 1000
        network.transact(self, web3_1, contract.functions.approve(account2.address, 1000), account1, erc20.GAS)

        # account2 withdraws from account1 into account3
        network.transact(self, web3_2, contract.functions.transferFrom(account1.address, account3.address, 100), account2, erc20.GAS)
        self.log.info('Balances before transfer')
        self.log.info('  Account1 balance = %d ' % contract.functions.balanceOf(account1.address).call())
        self.log.info('  Account2 balance = %d ' % contract.functions.balanceOf(account2.address).call())
        self.log.info('  Account3 balance = %d ' % contract.functions.balanceOf(account3.address).call())
        self.assertTrue(contract.functions.balanceOf(account1.address).call() == 999700)
        self.assertTrue(contract.functions.balanceOf(account2.address).call() == 200)
        self.assertTrue(contract.functions.balanceOf(account3.address).call() == 100)