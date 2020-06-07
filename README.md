[![Build Status](https://travis-ci.com/hukkinj1/cosmospy.svg?branch=master)](https://travis-ci.com/hukkinj1/cosmospy)
[![codecov.io](https://codecov.io/gh/hukkinj1/cosmospy/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/cosmospy)
[![PyPI version](https://badge.fury.io/py/cosmospy.svg)](https://badge.fury.io/py/cosmospy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# cosmospy

<!--- Don't edit the version line below manually. Let bump2version do it for you. -->
> Version 5.0.0

> Tools for Cosmos wallet management and offline transaction signing

## Installing
Installing from PyPI repository (https://pypi.org/project/cosmospy):
```bash
pip install cosmospy
```

## Usage

### Generating a wallet
```python
from cosmospy import generate_wallet
wallet = generate_wallet()
```
The value assigned to `wallet` will be a dictionary just like:
```python
{
    "seed": "arch skill acquire abuse frown reject front second album pizza hill slogan guess random wonder benefit industry custom green ill moral daring glow elevator",
    "derivation_path": "m/44'/118'/0'/0/0",
    "private_key": b"\xbb\xec^\xf6\xdcg\xe6\xb5\x89\xed\x8cG\x05\x03\xdf0:\xc9\x8b \x85\x8a\x14\x12\xd7\xa6a\x01\xcd\xf8\x88\x93",
    "public_key": b"\x03h\x1d\xae\xa7\x9eO\x8e\xc5\xff\xa3sAw\xe6\xdd\xc9\xb8b\x06\x0eo\xc5a%z\xe3\xff\x1e\xd2\x8e5\xe7",
    "address": "cosmos1uuhna3psjqfxnw4msrfzsr0g08yuyfxeht0qfh",
}
 ```

### Converter functions
#### Mnemonic seed to private key
```python
from cosmospy import seed_to_privkey
seed = "teach there dream chase fatigue abandon lava super senior artefact close upgrade"
privkey = seed_to_privkey(seed, path="m/44'/118'/0'/0/0")
 ```
#### Private key to public key
```python
from cosmospy import privkey_to_pubkey
privkey = bytes.fromhex("6dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515afa")
pubkey = privkey_to_pubkey(privkey)
 ```
#### Public key to address
```python
from cosmospy import pubkey_to_address
pubkey = bytes.fromhex("03e8005aad74da5a053602f86e3151d4f3214937863a11299c960c28d3609c4775")
addr = pubkey_to_address(pubkey)
 ```
#### Private key to address
```python
from cosmospy import privkey_to_address
privkey = bytes.fromhex("6dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515afa")
addr = privkey_to_address(privkey)
 ```

### Signing transactions
```python
from cosmospy import Transaction
tx = Transaction(
    privkey=bytes.fromhex("26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59"),
    account_num=11335,
    sequence=0,
    fee=1000,
    gas=70000,
    memo="",
    chain_id="cosmoshub-3",
    sync_mode="sync",
)
tx.add_transfer(recipient="cosmos103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf", amount=387000)
tx.add_transfer(recipient="cosmos1lzumfk6xvwf9k9rk72mqtztv867xyem393um48", amount=123)
pushable_tx = tx.get_pushable()
```
One or more token transfers can be added to a transaction by calling the `add_transfer` method.

When the transaction is fully prepared, calling `get_pushable` will return a signed transaction in the form of a JSON string. This can be used as request body when calling the `POST /txs` endpoint of the [Cosmos REST API](https://cosmos.network/rpc).
