from solcx import compile_source

class SolidityCompiler():

    @classmethod
    def compileFile(cls, file):
        bytecode=None
        abi=None
        with open(file, 'r') as fp:
            compiled_sol = compile_source(fp.read(), output_values=['abi', 'bin'])
            contract_id, contract_interface = compiled_sol.popitem()
            bytecode = contract_interface['bin']
            abi = contract_interface['abi']
        return bytecode, abi