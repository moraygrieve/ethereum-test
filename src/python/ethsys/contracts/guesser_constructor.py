import random
from pysys.constants import *
from ethsys.solidity.compile import SolidityCompiler
from ethsys.contracts.guesser import Guesser


class GuesserConstructor(Guesser):

    def __init__(self, test, web3, lower=0, upper=100):
        self.secret = random.randint(lower, upper)
        test.log.info('Secret number to guess will be %d' % self.secret)
        super().__init__(test, web3, lower=0, upper=100)

    def construct(self):
        """Compile and construct an instance. """
        path = os.path.join(PROJECT.root, 'utils', 'contracts', 'guesser', 'Guesser_constructor.sol')
        self.bytecode, self.abi = SolidityCompiler.compileFile(path)
        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor(self.secret)

