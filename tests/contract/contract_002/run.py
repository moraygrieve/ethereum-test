from pysys.basetest import BaseTest
from ethsys.contracts.guesser.guesser_constructor import GuesserConstructor
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        network = NetworkFactory.get_network(self)
        process, host, port = network.init(self)

        # connect to the network, create a local private key and convert into the account
        web3, account = network.connect(self, host, port)
        self.log.info('Using account with address %s' % account.address)

        # compile the guessing game and build the deployment transaction
        self.log.info('Compiling the guessing game application')
        guesser = GuesserConstructor(self, web3, 0, 100)
        signed_tx = network.build_transaction(self, web3, guesser.contract, account, guesser.GAS)

        # Sign the transaction and send to the network
        self.log.info('Signing and sending raw transaction')
        tx_hash = network.send_transaction(self, web3, guesser.contract, signed_tx)

        # wait for the transaction receipt and check the status
        self.log.info('Waiting for the send transaction')
        tx_receipt = network.wait_for_transaction(self, web3, tx_hash)

        # construct the contract using the contract address
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=guesser.abi)

        # guess the number
        self.log.info('Starting guessing game')
        self.assertTrue(guesser.guess(contract) == guesser.secret)
