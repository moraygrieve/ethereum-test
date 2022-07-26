from pysys.basetest import BaseTest
from ethsys.networks.factory import NetworkFactory


class PySysTest(BaseTest):
    def execute(self):
        network = NetworkFactory.get_network(self)
        process, host, port = network.init(self)

        # connect to the network, create a local private key and convert into the account
        web3, account = network.connect(self, host, port)
        self.log.info('Using account with address %s' % account.address)

        # get the chain id
        chain_id = network.chain_id()
        self.log.info('Chain id is %d' % chain_id)
        self.assertTrue(chain_id == network.chain_id())

        # get the block number
        block_number = network.get_block_number(web3)
        self.log.info('Block number is %d' % block_number)
        self.assertTrue(block_number >= 0)

        # get the balance
        balance = network.get_balance(web3, account.address)
        self.log.info('Balance for new accounts is %d' % balance)
        self.assertTrue(balance >= 0)

        # get block by number
        block = network.get_block_by_number(web3, block_number)
        self.log.info('Block %s' % block)
        self.log.info('Block has number %s' % block.number)
        self.assertTrue(block.number == block_number)

        # get block by hash
        block = network.get_block_by_hash(web3, block.parentHash)
        self.log.info('Block has number %s' % block.number)
        self.assertTrue(block.number == block_number - 1)

        # get gas price
        gas_price = network.gas_price(web3)
        self.log.info('Gas price is %s' % gas_price)
        self.assertTrue(gas_price >= 0)
