import random
from pysys.constants import *
from ethsys.solidity.compile import SolidityCompiler


class ERC20:

    def __init__(self, test, web3):
        """Create an instance of the ERC20 contract, compile and construct a web3 instance

        Contract wrappers will contain a reference to the web3 instance for their connection, and
        will compile and create an initial instance of the contract ready for deployment.
        :param test: The owning testcase
        :param web3: Reference to the web3 instance
        """
        self.bytecode = None
        self.abi = None
        self.contract = None
        self.test = test
        self.web3 = web3
        self.construct()

    def construct(self):
        """Compile and construct an instance. """
        path = os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'ERC20.sol')
        self.bytecode, self.abi = SolidityCompiler.compileFile(path)
        #self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor()


