import hashlib

from secp256k1 import PrivateKey
import bech32

from cosmospy.typing import Wallet


def generate_wallet() -> Wallet:
    privkey = PrivateKey().serialize()
    return {
        "private_key": privkey,
        "public_key": privkey_to_pubkey(privkey),
        "address": privkey_to_address(privkey),
    }


def privkey_to_pubkey(privkey: str) -> str:
    privkey_obj = PrivateKey(bytes.fromhex(privkey))
    return privkey_obj.pubkey.serialize().hex()


def pubkey_to_address(pubkey: str) -> str:
    pubkey_bytes = bytes.fromhex(pubkey)
    s = hashlib.new("sha256", pubkey_bytes).digest()
    r = hashlib.new("ripemd160", s).digest()
    return bech32.bech32_encode("cosmos", bech32.convertbits(r, 8, 5))


def privkey_to_address(privkey: str) -> str:
    pubkey = privkey_to_pubkey(privkey)
    return pubkey_to_address(pubkey)
