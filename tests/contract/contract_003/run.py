from pysys.basetest import BaseTest
from ethsys.contracts.guesser import Guesser
from ethsys.networks.obscuro import ObscuroNetwork


class PySysTest(BaseTest):

    def execute(self):
        network = ObscuroNetwork

        # connect to the network, create a local private key and convert into the account
        web3, private_key, account = network.connect(self)
        self.log.info('Using account with address %s' % account.address)

        # compile the guessing game and build the deployment transaction
        self.log.info('Compiling the guessing game application')
        guesser = Guesser(self, web3, 0, 100)
        build_tx = network.buildTransaction(self, web3, guesser.contract, account)

        # Sign the transaction and send to the network
        self.log.info('Signing and sending raw transaction')
        send_tx = network.sendRawTransaction(self, web3, account, build_tx)

        # wait for the transaction receipt and check the status
        self.log.info('Waiting for the send transaction')
        tx_receipt = network.waitForTransaction(self, web3, send_tx)

        # construct the contract using the contract address
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=guesser.abi)

        # guess the number
        self.log.info('Starting guessing game')
        self.assertTrue(guesser.guess(contract) == guesser.secret)
