import hashlib

import bech32
from ecdsa import SigningKey, SECP256k1
from secp256k1 import PrivateKey

from cosmospy.typing import Wallet


def generate_wallet() -> Wallet:
    # privkey = PrivateKey().serialize()
    privkey = SigningKey.generate(curve=SECP256k1).to_string().hex()
    pubkey = privkey_to_pubkey(privkey)
    address = pubkey_to_address(pubkey)
    return {"private_key": privkey, "public_key": pubkey, "address": address}


def privkey_to_pubkey(privkey: str) -> str:
    privkey_obj = SigningKey.from_string(bytes.fromhex(privkey), curve=SECP256k1)
    return privkey_obj.get_verifying_key().to_string("compressed").hex()


def pubkey_to_address(pubkey: str) -> str:
    pubkey_bytes = bytes.fromhex(pubkey)
    s = hashlib.new("sha256", pubkey_bytes).digest()
    r = hashlib.new("ripemd160", s).digest()
    return bech32.bech32_encode("cosmos", bech32.convertbits(r, 8, 5))


def privkey_to_address(privkey: str) -> str:
    pubkey = privkey_to_pubkey(privkey)
    return pubkey_to_address(pubkey)
