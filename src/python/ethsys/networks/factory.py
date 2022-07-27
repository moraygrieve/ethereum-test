from ethsys.networks.default import DefaultNetwork
from ethsys.networks.obscuro import ObscuroNetwork
from ethsys.networks.ropsten import RopstenNetwork
from ethsys.networks.ganache import GanacheNetwork


class NetworkFactory:

    @classmethod
    def get_network(cls, test):
        if test.mode == 'ropsten':
            return RopstenNetwork
        elif test.mode == 'obscuro':
            return ObscuroNetwork
        elif test.mode == 'ganache':
            return GanacheNetwork
        return DefaultNetwork
