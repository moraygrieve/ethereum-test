Ethsys
------
PySys test repo for building and running solidity smart contracts on Ethereum 
(or related simulator e.g. ganache).


Initial notes (WIP) 
-------------------
npm install -g solc@0.4.19

to build the contract
$ solcjs --bin -o output contracts/Faucet.sol

start a local private blockchain
$ ganache-cli

connect to the server node using web3.py
```
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.isConnected()
```