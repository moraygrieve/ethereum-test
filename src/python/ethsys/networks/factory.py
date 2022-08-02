from ethsys.networks.default import DefaultNetwork
from ethsys.networks.obscuro import ObscuroNetwork
from ethsys.networks.ropsten import RopstenNetwork
from ethsys.networks.ganache import GanacheNetwork
from ethsys.networks.obscuro import ObscuroL1
from ethsys.networks.obscuro import ObscuroL1Local


class NetworkFactory:

    @classmethod
    def get_network(cls, test):
        if test.mode == 'ganache':
            return GanacheNetwork
        elif test.mode == 'ropsten':
            return RopstenNetwork
        elif test.mode == 'obscuro':
            return ObscuroNetwork
        elif test.mode == 'obscuro_l1':
            return ObscuroL1
        elif test.mode == 'obscuro_l1_local':
            return ObscuroL1Local
        return DefaultNetwork
