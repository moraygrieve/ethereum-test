from pysys.constants import *
from solcx import compile_source


class ERC20:
    GAS = 7200000

    def __init__(self, test, web3, name, symbol):
        """Create an instance of the ERC20 contract, compile and construct a web3 instance

        Contract wrappers will contain a reference to the web3 instance for their connection, and
        will compile and create an initial instance of the contract ready for deployment.
        :param test: The owning testcase
        :param web3: Reference to the web3 instance
        :param name: The name of the ERC20 token
        :param web3: The symbol of the ERC20 token
        """
        self.bytecode = None
        self.abi = None
        self.contract = None
        self.test = test
        self.web3 = web3
        self.name = name
        self.symbol = symbol
        self.construct(test)

    def construct(self, test):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, 'utils', 'contracts', 'erc20', 'ERC20.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary='/opt/homebrew/bin/solc',
                                          base_path=os.path.dirname(file))
            contract_interface = compiled_sol['<stdin>:ERC20']
            self.bytecode = contract_interface['bin']
            self.abi = contract_interface['abi']
        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor(self.name, self.symbol)


