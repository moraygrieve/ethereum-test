import os
from web3 import Web3

class GanacheNetwork:

    @classmethod
    def run(cls, test, port=8454):
        stdout = os.path.join(test.output, 'ganache.out')
        stderr = os.path.join(test.output, 'ganache.err')

        arguments = []
        if port is not None: arguments.extend(('--port', str(port)))
        hprocess = test.startProcess(command=PROJECT.ganacheBin, displayName='ganache', workingDir=test.output,
                                     environs=os.environ,
                                     arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)

        test.waitForSignal(stdout, expr='Listening on 127.0.0.1:%d' % port, timeout=10)
        return hprocess

    @classmethod
    def connect(cls, test, host='127.0.0.1', port=None):
        if port is None: port = test.getNextAvailableTCPPort()
        w3 = Web3(Web3.HTTPProvider('http://%s:%d' % (host, port)))
        w3.eth.default_account = w3.eth.accounts[0]
        return (None, w3.eth.default_account)

    @classmethod
    def waitForTransaction(cls):
        raise NotImplementedError
