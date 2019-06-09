[![Build Status](https://travis-ci.com/hukkinj1/cosmospy.svg?branch=master)](https://travis-ci.com/hukkinj1/cosmospy)
[![codecov.io](https://codecov.io/gh/hukkinj1/cosmospy/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/cosmospy)
[![LoC](https://tokei.rs/b1/github/hukkinj1/cosmospy)](https://tokei.rs/b1/github/hukkinj1/cosmospy)
[![PyPI version](https://badge.fury.io/py/cosmospy.svg)](https://badge.fury.io/py/cosmospy)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
# cosmospy

<!--- Don't edit the version line below manually. Let bump2version do it for you. -->
> Version 0.0.1

> Tools for Cosmos wallet management and offline transaction signing

## Requirements
```bash
apt-get install libsecp256k1-dev
```

## Installing
Installing from PyPI repository (https://pypi.org/project/cosmospy):
```bash
pip install cosmospy
```

## Usage

### Generating a wallet
```python
from cosmospy.addresses import generate_wallet
wallet = generate_wallet()
```
The value assigned to `wallet` will be a dictionary just like:
```python
{
    'private_key': '6dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515afa',
    'public_key': '03e8005aad74da5a053602f86e3151d4f3214937863a11299c960c28d3609c4775',
    'address': 'cosmos1jkc7hv9j92gj7r6sqq0l630lv4kqyac7t2dj2t'
 }
 ```

 ### Signing transactions
 TODO: Update the README. The functionality is already in place in code.
 