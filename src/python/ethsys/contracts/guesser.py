import random
from pysys.constants import *
from ethsys.solidity.compile import SolidityCompiler


class Guesser:

    def __init__(self, test,  lower=0, upper=100,):
        self.test = test
        self.lower = lower
        self.upper = upper
        self.secret = random.randrange(0, 100)
        self.test.log.info("The secret number will be %s" % self.secret)


    def compile(self):
        path = os.path.join(PROJECT.root, 'utils', 'contracts', 'Guesser.sol')
        bytecode, abi = SolidityCompiler.compileFile(path)
        return (bytecode, abi)


    def guess(self, contract, max_guesses=100):
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
