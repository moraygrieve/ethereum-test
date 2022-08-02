from ethsys.networks.default import DefaultNetwork


class GethNetwork(DefaultNetwork):
    HOST = 'testnet.obscu.ro'
    PORT = 8025

    @classmethod
    def chain_id(cls): return 1337
