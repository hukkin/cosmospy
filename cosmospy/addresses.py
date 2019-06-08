import hashlib
from typing import Dict

from secp256k1 import PrivateKey
import bech32


def generate_wallet() -> Dict[str, str]:
    privkey = PrivateKey().serialize()
    return {
        'private_key': privkey,
        'public_key': privkey_to_pubkey(privkey),
        'address': privkey_to_address(privkey),
    }


def privkey_to_pubkey(private_key: str) -> str:
    privkey = PrivateKey(bytes.fromhex(private_key))
    return privkey.pubkey.serialize().hex()


def privkey_to_address(private_key: str) -> str:
    pubkey = privkey_to_pubkey(private_key)
    pubkey_bytes = bytes.fromhex(pubkey)
    s = hashlib.new('sha256', pubkey_bytes).digest()
    r = hashlib.new('ripemd160', s).digest()
    return bech32.bech32_encode('cosmos', bech32.convertbits(r, 8, 5))
