from ethsys.basetest import EthereumTest
from ethsys.contracts.guesser.guesser_constructor import GuesserConstructor
from ethsys.networks.factory import NetworkFactory


class PySysTest(EthereumTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        web3, account = network.connect_account1()
        self.log.info('Using account with address %s' % account.address)

        # deploy the contract
        self.log.info('Deploy the Guesser contract')
        guesser = GuesserConstructor(self, web3, 0, 100)
        tx_receipt = network.transact(self, web3, guesser.contract, account, guesser.GAS)

        # construct contract instance
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=guesser.abi)

        # guess the number
        self.log.info('Starting guessing game')
        self.assertTrue(guesser.guess(contract) == guesser.secret)
