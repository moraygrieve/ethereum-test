Ethsys
------
PySys test repo for building and running solidity smart contracts on Ethereum 
(or related simulator e.g. ganache).


Initial notes (WIP) 
-------------------

#python dependencies
python3 -m pip install web3
python3 -m pip install pysys=1.6.1
python3 -m pip install py-solc-x

#install solc (which differs from solcjs and is used by python solcx)
brew tap ethereum/ethereum
brew install solidity

#install homebrew and node.js
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew upgrade
brew install node

#install solcjs
npm install -g solc@0.8.15
$ solcjs --bin -o output contracts/Faucet.sol

start a local private blockchain
$ ganache-cli

connect to the server node using web3.py
```
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.isConnected()
```