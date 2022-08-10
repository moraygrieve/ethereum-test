Ethereum Test Framework (multiple networks)
-------------------------------------------
Project repo for building and running solidity smart contracts on Ethereum against a variety of networks e.g. 
[ganache](https://trufflesuite.com/ganache/), [ropsten via infura](https://infura.io/), 
[geth](https://geth.ethereum.org/docs/getting-started), and  [obscuro](https://obscu.ro/). The repo uses the 
[pysys](https://pysys-test.github.io/pysys-test/) test framework to manage all tests and their execution. All tests are 
fully system level using [web3.py](https://web3py.readthedocs.io/en/stable/) to interact with the networks which are 
managed outside the scope of the tests. Note the project is currently under continuous active development and further 
information on running the tests will be added to this readme over time. 


Repository Structure
--------------------
The top level structure of the project is as below;

```
├── README.md            # Readme 
├── .default.properties  # Default properties file detailing connection and keys required for running 
├── pysysproject.xml     # The pysys project file
├── admin                # Used for administering Obscuro testnet 
├── artifacts            # Artifacts used during test execution (e.g. Obscuro wallet extension)
├── src                  # The project source root for test execution 
│    └── python          # Python source code as extension to pysys for ethereum interaction
├── tests                # The project test root for all tests
│    ├── external        # Tests against contract supplied externally 
│    ├── generic         # Network agnostic tests 
│    └── obscuro         # Obscuro specific tests 
└── utils                # The project utils root for utilities used by the tests
    └── contracts        # A library of smart contracts 
```

The [.user.properties](./.user.properties) template file should be copied and renamed to the username of the account 
executing the tests e.g. `.fredjones.properties`. As this file will contain private keys of accounts used for testing 
it should never be committed back into the main repo (the [.gitignore](./.gitignore) should prevent this). See the
[.user.properties](./.user.properties) for more information on the properties that need to be setup. 


Setup
-----
The easiest way to set up a host to run the tests is to create a docker container with all dependencies pre-installed. 
The repository should be cloned into the same parent directory as [go-obscuro](https://github.com/obscuronet/go-obscuro)
as running the tests will use the wallet_extension built from the working copy of the go-obscuro repository. To build 
the docker container, in the root of the repository use;

```bash
/utils/docker/build_image.sh
```













