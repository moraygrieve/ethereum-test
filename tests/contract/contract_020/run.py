from pysys.basetest import BaseTest
from ethsys.contracts.erc20.erc20 import ERC20
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):

    def execute(self):
        network = NetworkFactory.get_network(self)
        process, host, port = network.init(self)

        # connect to the network
        web3, account = network.connect(self, host, port)
        self.log.info('Using account with address %s' % account.address)

        # deploy the contract
        self.log.info('Deploy the ERC20 contract')
        erc20 = ERC20(self, web3, name='OBX TOKEN', symbol='OBX')
        tx_receipt = network.transact(self, web3, erc20.contract, account, erc20.GAS)

        # construct contract instance
        self.log.info('Construct an instance using the contract address and abi')
        contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=erc20.abi)

        # allocate funds