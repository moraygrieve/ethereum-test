from ethsys.networks.default import DefaultNetwork


class GanacheNetwork(DefaultNetwork):
    HOST = '127.0.0.1'
    PORT = 8545

    @classmethod
    def chain_id(cls): return 1337
