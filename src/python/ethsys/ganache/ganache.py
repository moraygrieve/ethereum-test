from pysys.constants import *

class GanacheHelper:

    @classmethod
    def run(cls, test, port=8454):
        stdout = os.path.join(test.output, 'ganache.out')
        stderr = os.path.join(test.output, 'ganache.err')

        arguments = []
        if port is not None: arguments.extend(('--port', str(port)))
        hprocess = test.startProcess(command=PROJECT.ganacheBin, displayName='ganache', workingDir=test.output,
                                 arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)

        test.waitForSignal(stdout, expr='Listening on 127.0.0.1:%d'%port, timeout=120)
        return hprocess