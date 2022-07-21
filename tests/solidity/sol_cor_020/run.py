from web3 import Web3
from pysys.basetest import BaseTest
from ethsys.utils.properties import Properties
from ethsys.contracts.guesser import Guesser


class PySysTest(BaseTest):
    def execute(self):
        props = Properties()

        # connect to the network and get the account
        w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/%s' % props.infuraProjectID()))
        account = w3.eth.account.privateKeyToAccount(props.privateKey())

        # create guesser abstraction, compile and deploy
        guesser = Guesser(self, 0, 100)

        self.log.info('Compiling the guessing game application')
        bytecode, abi = guesser.compile()
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        build_tx = contract.constructor(guesser.secret).buildTransaction(
            {
                'from': account.address,
                'nonce': w3.eth.getTransactionCount(account.address),
                'gasPrice': w3.eth.gasPrice,
                'chainId': 3
            }
        )

        self.log.info('Signing and sending raw transaction')
        signed_tx = account.signTransaction(build_tx)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # wait for the transaction receipt
        self.log.info('Waiting for transaction receipt')
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

        # make the guess until we get the right number
        self.log.info('Starting guessing game')
        guesser.guess(contract)

    def validate(self):
        pass
