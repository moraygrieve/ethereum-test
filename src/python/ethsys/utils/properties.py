import getpass, configparser
from pysys.constants import *


class Properties():

    def __init__(self):
        file = os.path.join(PROJECT.root, '.'+getpass.getuser()+'.properties')
        self.config = configparser.ConfigParser()
        if os.path.exists(file): self.config.read(filenames=file)

    def ownerPK(self):
        infura = self.config['keys']
        return infura.get('OwnerPK', '')

    def account1PK(self):
        infura = self.config['keys']
        return infura.get('Account1PK', '')

    def account2PK(self):
        infura = self.config['keys']
        return infura.get('Account2PK', '')


    def infuraProjectID(self):
        infura = self.config['infura']
        return infura.get('ProjectID', '')