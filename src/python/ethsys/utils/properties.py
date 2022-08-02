import getpass, configparser
from pysys.constants import *


class Properties:

    def __init__(self):
        file = os.path.join(PROJECT.root, '.'+getpass.getuser()+'.properties')
        self.config = configparser.ConfigParser()
        if os.path.exists(file): self.config.read(filenames=file)

    # default accounts used generally
    def account1pk(self):
        infura = self.config['default']
        return infura.get('Account1PK', '')

    def account2pk(self):
        infura = self.config['default']
        return infura.get('Account2PK', '')

    def account3pk(self):
        infura = self.config['default']
        return infura.get('Account3PK', '')

    # obscuro specific properties
    def management_bridge_address(self):
        obscuro = self.config['obscuro']
        return obscuro.get('ManagementBridgeAddress', '')

    def funded_deployment_account_pk(self):
        obscuro = self.config['obscuro']
        return obscuro.get('FundedDeploymentAccountPK', '')

    def l1_obx_token_address(self):
        obscuro = self.config['obscuro']
        return obscuro.get('TokenOBXContractAddressL1', '')

    def l2_obx_token_address(self):
        obscuro = self.config['obscuro']
        return obscuro.get('TokenOBXContractAddressL2', '')

    def l1_eth_token_address(self):
        obscuro = self.config['obscuro']
        return obscuro.get('TokenETHContractAddressL1', '')

    def l2_eth_token_address(self):
        obscuro = self.config['obscuro']
        return obscuro.get('TokenETHContractAddressL2', '')

    # infura related
    def infuraProjectID(self):
        infura = self.config['infura']
        return infura.get('ProjectID', '')