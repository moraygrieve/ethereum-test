from pysys.constants import PLATFORM, PROJECT


class Solidity:

    @classmethod
    def get_compiler(cls):
        if PLATFORM == 'darwin':
            return PROJECT.solcBin_darwin
        elif PLATFORM == 'darwin':
            return PROJECT.solcBin_linux
        return 'solc'
