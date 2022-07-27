import getpass, configparser
from pysys.constants import *


class Properties():

    def __init__(self):
        file = os.path.join(PROJECT.root, '.'+getpass.getuser()+'.properties')
        self.config = configparser.ConfigParser()
        if os.path.exists(file): self.config.read(filenames=file)

    def privateKey(self):
        infura = self.config['keys']
        return infura.get('PrivateKey', '')

    def infuraProjectID(self):
        infura = self.config['infura']
        return infura.get('ProjectID', '')