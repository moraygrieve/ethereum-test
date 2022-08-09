from ethsys.networks.default import Default


class Ganache(Default):
    """A Ganache node giving access to the underlying network."""
    HOST = '127.0.0.1'
    PORT = 8545

    @classmethod
    def chain_id(cls): return 1337
