from solcx import compile_source
from pysys.constants import *
from ethsys.utils.solidity import Solidity


class Storage:
    GAS = 720000

    def __init__(self, test, web3, initial):
        """Create an instance of the storage contract, compile and construct a web3 instance

        Contract wrappers will contain a reference to the web3 instance for their connection, and
        will compile and create an initial instance of the contract ready for deployment.
        :param test: The owning testcase
        :param web3: Reference to the web3 instance
        :param initial: The initial value
        """
        self.bytecode = None
        self.abi = None
        self.contract = None
        self.test = test
        self.web3 = web3
        self.initial = initial
        self.construct()

    def construct(self):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, 'utils', 'contracts', 'storage', 'Storage.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary=Solidity.get_compiler())
            contract_id, contract_interface = compiled_sol.popitem()
            self.bytecode = contract_interface['bin']
            self.abi = contract_interface['abi']

        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor(self.initial)
