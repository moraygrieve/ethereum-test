from ethsys.basetest import EthereumTest
from ethsys.contracts.storage.storage import Storage
from ethsys.networks.factory import NetworkFactory


class PySysTest(EthereumTest):

    def execute(self):
        # connect to the network
        network = NetworkFactory.get_network(self)
        web3, account = network.connect_account1()
        self.log.info('Using account with address %s' % account.address)

        # deploy the contract
        self.log.info('Deploy the Storage contract')
        storage = Storage(self, web3, 100)
        tx_receipt = network.transact(self, web3, storage.contract, account, storage.GAS)

        # construct contract instance
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=storage.abi)

        # retrieve via a call
        self.log.info('Call shows value %d' % contract.functions.retrieve().call())

        # set the value via a transaction, compare to call and transaction log
        tx_receipt = network.transact(self, web3, contract.functions.store(200), account, storage.GAS)
        self.log.info('Call shows value %d' % contract.functions.retrieve().call())

        tx_log = contract.events.Stored().processReceipt(tx_receipt)[0]
        args_value = tx_log['args']['value']
        self.log.info('Transaction log shows value %d' % args_value)
        self.assertTrue(args_value == 200)
