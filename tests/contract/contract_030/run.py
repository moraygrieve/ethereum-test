from pysys.basetest import BaseTest
from ethsys.contracts.erc20.obx import OBXCoin
from ethsys.networks.geth import TestNetLayer1Network
from ethsys.utils.properties import Properties

class PySysTest(BaseTest):


    def execute(self):
        # connect to the network
        network = TestNetLayer1Network
        web3, account = network.connect(Properties().funded_deployment_account_pk(), network.HOST, network.PORT)
        self.log.info('Using account with address %s' % account.address)

        # deploy our own ERC20 contract so we have the contract address
        self.log.info('Deploy the OBXCoin contract')
        erc20 = OBXCoin(self, web3)
        tx_receipt = network.transact(self, web3, erc20.contract, account, erc20.GAS)

        self.log.info('Getting byte code for deployed contract %s' % tx_receipt.contractAddress)
        bytecode1 = web3.eth.getCode(tx_receipt.contractAddress)
        self.assertTrue(bytecode1 != b'')

        self.log.info('Getting bytecode for pre-deployed address %s' % Properties().l1_obx_token_address())
        bytecode2 = web3.eth.getCode(Properties().l1_obx_token_address())
        self.assertTrue(bytecode2 != b'')



        with open(os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'erc20.json')) as f:
            contract2 = web3_2.eth.contract(address=tx_receipt.contractAddress, abi=json.load(f))


