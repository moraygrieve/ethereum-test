from pysys.constants import *
from solcx import compile_source
from ethsys.utils.solidity import Solidity


class OBXCoin:
    GAS = 7200000

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
        self.construct(test)

    def construct(self, test):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'OBXCoin.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary=Solidity.get_compiler(),
                                          base_path=os.path.dirname(file))
            contract_interface = compiled_sol['<stdin>:OBXCoin']
            self.bytecode = contract_interface['bin']
            self.abi = contract_interface['abi']
        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor()


