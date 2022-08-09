import os
from pysys.constants import PROJECT, BACKGROUND
from pysys.exceptions import AbortExecution
from ethsys.networks.ganache import Ganache
from ethsys.networks.obscuro import Obscuro
from ethsys.utils.properties import Properties


class EthereumRunnerPlugin():

    def setup(self, runner):
        mode = 'obscuro' if runner.mode is None else runner.mode
        runner.log.info('Runner is executing in mode %s' % mode)

        self.output = os.path.join(PROJECT.root, '.runner')
        if not os.path.exists(self.output ): os.makedirs(self.output)

        try:
            if mode == 'obscuro':
                self.run_wallets(runner, 'testnet.obscu.ro')
            elif mode == 'obscuro.local':
                self.run_wallets(runner, '127.0.0.1')
            elif mode == 'ganache':
                self.run_ganache(runner)
        except AbortExecution:
            runner.log.info('Error executing runner plugin')

    def run_ganache(self, runner):
        stdout = os.path.join(self.output , 'ganache.out')
        stderr = os.path.join(self.output , 'ganache.err')

        arguments = []
        arguments.extend(('--port', str(Ganache.PORT)))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().account1pk()))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().account2pk()))
        arguments.extend(('--account', '0x%s,1000000000000000000' % Properties().account3pk()))
        hprocess = runner.startProcess(command=PROJECT.ganacheBin, displayName='ganache',
                                       workingDir=self.output , environs=os.environ, quiet=True,
                                       arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)

        runner.waitForSignal(stdout, expr='Listening on 127.0.0.1:%d' % Ganache.PORT, timeout=10)
        runner.addCleanupFunction(lambda: self.stop_process(hprocess))

    def run_wallets(self, runner, host):
        self.run_wallet(runner, host, Obscuro.ACCOUNT1_PORT)
        self.run_wallet(runner, host, Obscuro.ACCOUNT2_PORT)
        self.run_wallet(runner, host, Obscuro.ACCOUNT3_PORT)

    def run_wallet(self, runner, host, port):
        runner.log.info('Starting wallet extension on %s %d' % (host, port))
        stdout = os.path.join(self.output, 'wallet_%d.out' % port)
        stderr = os.path.join(self.output, 'wallet_%d.err' % port)

        arguments = []
        arguments.extend(('--nodeHost', host))
        arguments.extend(('--nodePortHTTP', '13000'))
        arguments.extend(('--nodePortWS', '13001'))
        arguments.extend(('--port', str(port)))
        arguments.extend(('-logPath', 'wallet_%d_logs.txt' % port))
        hprocess = runner.startProcess(command=os.path.join(PROJECT.root, 'artifacts', 'wallet_extension'),
                                       displayName='wallet_extension', workingDir=self.output , environs=os.environ,
                                       quiet=True, arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)
        runner.waitForSignal(stdout, expr='Wallet extension started', timeout=10)
        runner.addCleanupFunction(lambda: self.stop_process(hprocess))

    def stop_process(self, hprocess):
        hprocess.stop()