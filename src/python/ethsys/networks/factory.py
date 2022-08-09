from ethsys.networks.ganache import Ganache
from ethsys.networks.ropsten import Ropsten
from ethsys.networks.obscuro import Obscuro
from ethsys.networks.obscuro import ObscuroL1
from ethsys.networks.obscuro import ObscuroL1Local


class NetworkFactory:
    """Factory class to return a network node for a given mode the test is run in. """

    @classmethod
    def get_network(cls, test):
        """Get the network node.

        Currently supported networks are ganache, ropsten and obscuro.local (obscuro being
        the default network used in all tests)
        """
        if test.mode == 'ganache':
            return Ganache
        elif test.mode == 'ropsten':
            return Ropsten
        elif test.mode == 'obscuro.local':
            return Obscuro
        return Obscuro

    @classmethod
    def get_l1_network(cls, test):
        """Get the layer 1 network used by a layer 2.

        Currently this is only for Obscuro networks and returns either a node in the L1 running
        in a local deployment, or in the testnet deployment.
        """
        if test.mode == 'obscuro.local':
            return ObscuroL1Local
        return ObscuroL1