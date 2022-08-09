import random
from solcx import compile_source
from pysys.constants import *
from ethsys.utils.solidity import Solidity
from ethsys.contracts.guesser.guesser import Guesser


class GuesserConstructor(Guesser):

    def __init__(self, test, web3, lower=0, upper=100):
        self.secret = random.randint(lower, upper)
        test.log.info('Secret number to guess will be %d' % self.secret)
        super().__init__(test, web3, lower=0, upper=100)

    def construct(self):
        """Compile and construct an instance. """
        file = os.path.join(PROJECT.root, 'utils', 'contracts', 'guesser', 'Guesser_constructor.sol')
        with open(file, 'r') as fp:
            compiled_sol = compile_source(source=fp.read(), output_values=['abi', 'bin'], solc_binary=Solidity.get_compiler())
            contract_id, contract_interface = compiled_sol.popitem()
            self.bytecode = contract_interface['bin']
            self.abi = contract_interface['abi']

        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor(self.secret)

