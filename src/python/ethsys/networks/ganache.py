import os
from pysys.constants import *
from ethsys.utils.properties import Properties
from ethsys.networks.default import Default


class Ganache(Default):
    """A Ganache node giving access to the underlying network."""
    HOST = '127.0.0.1'
    PORT = 8545

    @classmethod
    def init(cls, test):
        port = test.getNextAvailableTCPPort()
        stdout = os.path.join(test.output, 'ganache.out')
        stderr = os.path.join(test.output, 'ganache.err')

        arguments = []
        if port is not None: arguments.extend(('--port', str(port)))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().account1pk()))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().account2pk()))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().account3pk()))
        hprocess = test.startProcess(command=PROJECT.ganacheBin, displayName='ganache', workingDir=test.output,
                                     environs=os.environ,
                                     arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)

        test.waitForSignal(stdout, expr='Listening on 127.0.0.1:%d' % port, timeout=10)
        return hprocess, '127.0.0.1', port

    @classmethod
    def chain_id(cls): return 1337
