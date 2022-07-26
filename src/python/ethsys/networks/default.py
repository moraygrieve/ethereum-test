class DefaultNetwork:

    @classmethod
    def init(cls, test):
        return None, None, None

    @classmethod
    def connect(cls, test, host, port):
        return None, None

    @classmethod
    def chain_id(cls):
        return None

    @classmethod
    def get_chain_id(cls, web3):
        return web3.eth.chain_id

    @classmethod
    def get_block_number(cls, web3):
        return web3.eth.get_block_number()

    @classmethod
    def get_balance(cls, web3, account):
        return web3.eth.get_balance(account)

    @classmethod
    def get_block_by_number(cls, web3, block_number):
        return web3.eth.get_block(block_number)

    @classmethod
    def get_block_by_hash(cls, web3, block_hash):
        return web3.eth.get_block(block_hash)

    @classmethod
    def gas_price(cls, web3):
        return web3.eth.gas_price

    @classmethod
    def build_transaction(cls, test, web3, contract, account, gas):
        return None

    @classmethod
    def send_transaction(cls, test, web3, contract, account, build_tx):
        return None

    @classmethod
    def wait_for_transaction(cls, test, web3, tx_hash):
        return None


