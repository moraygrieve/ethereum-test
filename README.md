Ethereum Test Framework (multiple networks)
-------------------------------------------
Project repo for building and running solidity smart contracts on Ethereum against a variety of networks e.g. 
[ganache](https://trufflesuite.com/ganache/), [ropsten via infura](https://infura.io/) and [obscuro](https://obscu.ro/). 
The repo uses the [Pysys](https://pysys-test.github.io/pysys-test/) test framework to manage all tests and their 
execution. All tests are fully system level using [web3.py](https://web3py.readthedocs.io/en/stable/) to interact with 
the networks which are managed outside the scope of the tests. Note the project is currently under continuous active 
development and further information on running the tests will be added to this readme over time. 


Repository Structure
--------------------
The top level structure of the project is as below;

```
├── README.md            # Readme 
├── pysysproject.xml     # The pysys project file
├── src                  # The project source root for test execution 
│    └── python          # Python source code as extension to pysys for ethereum interaction
├── tests                # The project test root for all tests
│    ├── api             # Network agnostic tests against the RPC API
│    └── contract        # Network agnostic tests against a library of smart contracts
└── utils                # The project utils root for utilities used by the tests
    └── contracts        # A library of smart contracts 
```


Dependencies 
-------------

The following python dependencies and their installation is as given below;

```bash
# install python dependencies
python3 -m pip install web3
python3 -m pip install pysys==1.6.1
python3 -m pip install py-solc-x
```

The following node.js, ethereum and solidity dependencies and their installation is as given below;

```bash
# install homebrew and node.js
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew upgrade
brew install node

# install solc (which differs from solcjs and is used by python solcx)
brew tap ethereum/ethereum
brew install solidity

# install solcjs
npm install -g solc@0.8.15
$ solcjs --bin -o output contracts/Faucet.sol
```




