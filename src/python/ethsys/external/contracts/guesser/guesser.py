import random
from solcx import compile_source
from pysys.constants import *


class GuessingGame:
    GAS = 720000 * 4

    def __init__(self, test, web3):
        """Create an instance of the guessing game contract, compile and construct a web3 instance

        Contract wrappers will contain a reference to the web3 instance for their connection, and
        will compile and create an initial instance of the contract ready for deployment.
        :param test: The owning testcase
        :param web3: Reference to the web3 instance
        """
        self.erc20_bytecode = None
        self.erc20_abi = None
        self.guessing_bytecode = None
        self.guessing_abi = None
        self.test = test
        self.web3 = web3

    def construct_erc20_basic(self):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, '../', 'number-guessing-game', 'contracts', 'Guess.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary='/opt/homebrew/bin/solc')
            contract_interface = compiled_sol['<stdin>:ERC20Basic']
            self.erc20_bytecode = contract_interface['bin']
            self.erc20_abi = contract_interface['abi']

        return self.web3.eth.contract(abi=self.erc20_abi, bytecode=self.erc20_bytecode).constructor()

    def construct_guesser(self, size, token_address):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, '../', 'number-guessing-game', 'contracts', 'Guess.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary='/opt/homebrew/bin/solc')
            contract_interface = compiled_sol['<stdin>:Guess']
            self.guessing_bytecode = contract_interface['bin']
            self.guessing_abi = contract_interface['abi']

        return self.web3.eth.contract(abi=self.guessing_abi, bytecode=self.guessing_bytecode).constructor(size, token_address)