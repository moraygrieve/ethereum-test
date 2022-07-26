import random
from pysys.constants import *
from ethsys.solidity.compile import SolidityCompiler


class Guesser:

    def __init__(self, test, web3, lower=0, upper=100):
        """Create an instance of the guesser contract, compile and construct a web3 instance

        Contract wrappers will contain a reference to the web3 instance for their connection, and
        will compile and create an initial instance of the contract ready for deployment.
        :param test: The owning testcase
        :param web3: Reference to the web3 instance
        :param lower: The lower bounds of the number to guess
        :param upper: The upper bounds of the number to guess
        """
        self.bytecode = None
        self.abi = None
        self.contract = None
        self.test = test
        self.web3 = web3
        self.lower = lower
        self.upper = upper
        self.construct()

    def construct(self):
        """Compile and construct an instance. """
        path = os.path.join(PROJECT.root, 'utils', 'contracts', 'guesser', 'Guesser.sol')

        self.bytecode, self.abi = SolidityCompiler.compileFile(path)
        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode).constructor()

    def guess(self, contract, max_guesses=100):
        """Perform a guessing game to get the secret number.

        :param contract:
        :param max_guesses:
        :return:
        """
        lower = self.lower
        upper = self.upper
        nguess = 0
        while True:
            nguess += 1
            if nguess > max_guesses:
                self.test .log.warn("Exceeded guess count ... exiting")
                self.test .addOutcome(FAILED)
                return None

            guess = random.randrange(lower, upper)
            ret = contract.functions.guess(guess).call()
            if ret == 1:
                self.test.log.info("Guess is %d, need to go higher" % guess)
                lower = guess+1
            elif ret == -1:
                self.test.log.info("Guess is %d, need to go lower" % guess)
                upper = guess
            else:
                self.test.log.info("You've guessed the secret %s" % guess)
                self.test.addOutcome(PASSED)
                return guess
