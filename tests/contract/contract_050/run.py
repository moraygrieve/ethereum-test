from pysys.basetest import BaseTest
from ethsys.contracts.storage.storage import Storage
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        network = NetworkFactory.get_network(self)
        process, host, port = network.init(self)

        # connect to the network
        web3, account = network.connect(self, host, port)
        self.log.info('Using account with address %s' % account.address)

        # deploy the contract
        self.log.info('Deploy the Storage contract')
        storage = Storage(self, web3, 100)
        tx_receipt = network.transact(self, web3, storage.contract, account, storage.GAS)

        # construct contract instance
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=storage.abi)

        # retrieve, store and retrieve a new value
        self.log.info('Call shows value %d' % contract.functions.retrieve().call())
        tx_receipt = network.transact(self, web3, contract.functions.store(200), account, storage.GAS)
        self.log.info('Transaction logs show value %d' % contract.events.Stored().processReceipt(tx_receipt)[0]['args']['value'])
        self.log.info('Call shows value %d' % contract.functions.retrieve().call())