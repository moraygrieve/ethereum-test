Admin controls on Obscuro TestNet
=================================
This directory contains utilities to perform admin operations on the Obscuro Testnet. This is to 

- allocate funds into the layer2 into the OBX ERC20 contract for use by the number guessing game
- transfer funds into a user who wished to play the number guessing game

Running the utilities requires Python3 to be installed, along with the following dependencies;

```bash
# install python dependencies
sudo apt update
sudo apt install python3-pip
python3 -m pip install web3
python3 -m pip install pysys==1.6.1
```

Note that the `pysys.py` script will be installed into the `~/.local/bin/` directory on linux systems which is not 
necessarily on your search path. The wallet_extension should be downloaded from the 
[releases page](https://github.com/obscuronet/go-obscuro/releases) and started using;

```
wallet_extension -nodeHost testnet.obscu.ro -nodePortHTTP 13000 -nodePortWS 13001
```

Funding the faucet
------------------
`fund_faucet` provides the ability to ensure the tokens in the pre-funded deployment account (the owner of the OBC ERC20
token contract) in layer 2 do not fall below a certain threshold (currently set at 1000). When the token amount falls 
below this amount it is increased back up to 1000000. To run a check and perform an allocation if required used;

```bash
pysys.py run fund_faucet
```

Funding users
-------------
`fund_user` provides the ability to add in new user accounts, and for any accounts with a zero balance to increase 
their allocation to 50 tokens. To print out the current fund allocations use;

```bash
pysys.py run -XDISPLAY_ONLY fund_user
```

To transfer 50 tokens to any user whose current allocation is zero use;

```bash
pysys.py run fund_user
```

At the moment users managed are defined in the `fund_user/run.py` script, as a dictionary of logical user name to 
account address. To add a new used edit this file to add in the new user details to the USERS dictionary; 

```python
    USERS = {
        'MATT':'0x686Ad719004590e98F182feA3516d443780C64a1',
        'GAVIN':'0x85E1Cc949Bca27912e3e951ad1F68afD1cc4aB15',
        'MORAY':'0x7719A2b2BeC6a98508975C168A565FffCF9Dc266'
    }
    AMOUNT = 50
```



