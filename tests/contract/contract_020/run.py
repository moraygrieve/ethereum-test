import secrets
from pysys.basetest import BaseTest
from ethsys.contracts.erc20.obx import OBXCoin
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        w3_recip2, recip2 = network.connect_account2()
        w3_recip1, recip1 = network.connect_account1()
        w3_accnt, account = network.connect_owner()
        self.log.info('Using account with address %s' % account.address)

        # deploy the contract
        self.log.info('Deploy the OBXCoin contract')
        erc20 = OBXCoin(self, w3_accnt)
        tx_receipt = network.transact(self, w3_accnt, erc20.contract, account, erc20.GAS)

        # construct contract instance
        self.log.info('Construct an instance using the contract address and abi')
        contract = w3_accnt.eth.contract(address=tx_receipt.contractAddress, abi=erc20.abi)

        # check initial allocations
        self.log.info('Balances before transfer')
        self.log.info('  Owner  balance = %d ' % contract.functions.balanceOf(account.address).call())
        self.log.info('  Recip1 balance = %d ' % contract.functions.balanceOf(recip1.address).call())
        self.log.info('  Recip2 balance = %d ' % contract.functions.balanceOf(recip2.address).call())
        self.assertTrue(contract.functions.balanceOf(account.address).call() == 1000000)
        self.assertTrue(contract.functions.balanceOf(recip1.address).call() == 0)
        self.assertTrue(contract.functions.balanceOf(recip2.address).call() == 0)

        # transfer from owner account into the recipient account
        network.transact(self, w3_accnt, contract.functions.transfer(recip1.address, 200), account, erc20.GAS)
        self.log.info('Balances after transfer')
        self.log.info('  Owner  balance = %d ' % contract.functions.balanceOf(account.address).call())
        self.log.info('  Recip1 balance = %d ' % contract.functions.balanceOf(recip1.address).call())
        self.log.info('  Recip2 balance = %d ' % contract.functions.balanceOf(recip2.address).call())
        self.assertTrue(contract.functions.balanceOf(account.address).call() == 999800)
        self.assertTrue(contract.functions.balanceOf(recip1.address).call() == 200)
        self.assertTrue(contract.functions.balanceOf(recip2.address).call() == 0)

        # approve recip 1 to send out of the owners account
        network.transact(self, w3_accnt, contract.functions.approve(recip1.address, 1000), account, erc20.GAS)

        # recip 1 sends funds from owner to recip 2
        network.transact(self, w3_accnt, contract.functions.transferFrom(account.address, recip2.address, 100), recip1, erc20.GAS)
        self.log.info('Balances before transfer')
        self.log.info('  Owner  balance = %d ' % contract.functions.balanceOf(account.address).call())
        self.log.info('  Recip1 balance = %d ' % contract.functions.balanceOf(recip1.address).call())
        self.log.info('  Recip2 balance = %d ' % contract.functions.balanceOf(recip2.address).call())
        self.assertTrue(contract.functions.balanceOf(account.address).call() == 999700)
        self.assertTrue(contract.functions.balanceOf(recip1.address).call() == 200)
        self.assertTrue(contract.functions.balanceOf(recip2.address).call() == 100)