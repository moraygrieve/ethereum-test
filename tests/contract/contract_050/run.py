from pysys.basetest import BaseTest
from ethsys.contracts.storage.storage import Storage
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        network = NetworkFactory.get_network(self)
        process, host, port = network.init(self)

        # connect to the network, create a local private key and convert into the account
        web3, account = network.connect(self, host, port)
        self.log.info('Using account with address %s' % account.address)

        # compile the guessing game and build the deployment transaction
        self.log.info('Compiling the erc20 ccntract')
        storage = Storage(self, web3, 100)
        signed_tx = network.build_transaction(self, web3, storage.contract, account, storage.GAS)

        # Sign the transaction and send to the network
        self.log.info('Signing and sending raw transaction')
        tx_hash = network.send_transaction(self, web3, storage.contract, signed_tx)

        # wait for the transaction receipt and check the status
        self.log.info('Waiting for the send transaction')
        tx_receipt = network.wait_for_transaction(self, web3, tx_hash)

        # construct the contract using the contract address
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=storage.abi)

        # retrieve the stored value via a call (not state change and synchronous)
        self.log.info('Call shows value %d' % contract.functions.retrieve().call())

        # store and then retrieve a new value
        build_tx = contract.functions.store(200).buildTransaction({
            "from": account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gasPrice': web3.eth.gas_price,
            'gas': 72000,
            'chainId': 3}
        )
        signed_tx = account.sign_transaction(build_tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = network.wait_for_transaction(self, web3, tx_hash)
        self.log.info('Transaction logs show value %d' % contract.events.Stored().processReceipt(tx_receipt)[0]['args']['value'])
        self.log.info('Call shows value %d' % contract.functions.retrieve().call())