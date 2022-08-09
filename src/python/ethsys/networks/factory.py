from ethsys.networks.default import Default
from ethsys.networks.ganache import Ganache
from ethsys.networks.ropsten import Ropsten
from ethsys.networks.obscuro import Obscuro
from ethsys.networks.obscuro import ObscuroL1
from ethsys.networks.obscuro import ObscuroL1Local


class NetworkFactory:

    @classmethod
    def get_network(cls, test):
        if test.mode == 'ganache':
            return Ganache
        elif test.mode == 'ropsten':
            return Ropsten
        elif (test.mode == 'obscuro') or (test.mode == 'obscuro.local'):
            return Obscuro
        return Default

    @classmethod
    def get_l1_network(cls, test):
        if test.mode == 'obscuro':
            return ObscuroL1
        elif test.mode == 'obscuro.local':
            return ObscuroL1Local
        return Default