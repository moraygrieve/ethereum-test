import getpass, configparser
from pysys.constants import *


class Properties:

    def __init__(self):
        file = os.path.join(PROJECT.root, '.'+getpass.getuser()+'.properties')
        self.config = configparser.ConfigParser()
        if os.path.exists(file):
            self.config.read(filenames=file)
        else:
            file = os.path.join(PROJECT.root, '.default.properties')
            self.config.read(filenames=file)

    # default accounts used generally
    def account1pk(self):
        infura = self.config['all']
        return infura.get('Account1PK', '')

    def account2pk(self):
        infura = self.config['all']
        return infura.get('Account2PK', '')

    def account3pk(self):
        infura = self.config['all']
        return infura.get('Account3PK', '')

    def gameuserpk(self):
        infura = self.config['all']
        return infura.get('GameUserPK', '')

    # obscuro specific properties
    def funded_deployment_account_pk(self, key):
        obscuro = self.config[key]
        return obscuro.get('FundedDeploymentAccountPK', '')

    def management_bridge_address(self, key):
        obscuro = self.config[key]
        return obscuro.get('ManagementBridgeAddress', '')

    def guessing_game_address(self, key):
        obscuro = self.config[key]
        return obscuro.get('GuessingGameAddress', '')

    def l1_jam_token_address(self, key):
        obscuro = self.config[key]
        return obscuro.get('TokenJAMContractAddressL1', '')

    def l2_jam_token_address(self, key):
        obscuro = self.config[key]
        return obscuro.get('TokenJAMContractAddressL2', '')

    def l1_eth_token_address(self, key):
        obscuro = self.config[key]
        return obscuro.get('TokenETHContractAddressL1', '')

    def l2_eth_token_address(self, key):
        obscuro = self.config[key]
        return obscuro.get('TokenETHContractAddressL2', '')

    # infura related
    def infuraProjectID(self):
        infura = self.config['ropsten']
        return infura.get('ProjectID', '')