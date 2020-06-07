import hashlib
import hmac

import bech32
from bip32 import BIP32
import ecdsa
import mnemonic

from cosmospy.typing import Wallet

DEFAULT_DERIVATION_PATH = "m/44'/118'/0'/0/0"


def generate_wallet() -> Wallet:
    while True:
        phrase = mnemonic.Mnemonic(language="english").generate(strength=256)
        try:
            privkey = seed_to_privkey(phrase)
            break
        except ecdsa.MalformedPointError:
            pass
    pubkey = privkey_to_pubkey(privkey)
    address = pubkey_to_address(pubkey)
    return {
        "seed": phrase,
        "derivation_path": DEFAULT_DERIVATION_PATH,
        "private_key": privkey,
        "public_key": pubkey,
        "address": address,
    }


def seed_to_privkey(seed: str, path: str = DEFAULT_DERIVATION_PATH) -> bytes:
    """Get a private key from a mnemonic seed and a derivation path.

    Assumes a BIP39 mnemonic seed with no passphrase. Raises
    `ecdsa.MalformedPointError` if the resulting private key is invalid.
    """
    seed_bytes = mnemonic.Mnemonic.to_seed(seed, passphrase="")

    # Generate wallet master key as per BIP32
    bip32_magic_string = b"Bitcoin seed"
    seed_hmac = hmac.new(bip32_magic_string, seed_bytes, digestmod=hashlib.sha512).digest()
    master_key = seed_hmac[:32]
    chain_code = seed_hmac[32:]

    # Derive a private key from the given path
    derived_privkey = BIP32(chain_code, privkey=master_key).get_privkey_from_path(path)

    # Validate the derived private key. Can raise ecdsa.MalformedPointError here.
    ecdsa.SigningKey.from_string(derived_privkey, curve=ecdsa.SECP256k1)

    return derived_privkey


def privkey_to_pubkey(privkey: bytes) -> bytes:
    privkey_obj = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
    pubkey_obj = privkey_obj.get_verifying_key()
    return pubkey_obj.to_string("compressed")


def pubkey_to_address(pubkey: bytes) -> str:
    s = hashlib.new("sha256", pubkey).digest()
    r = hashlib.new("ripemd160", s).digest()
    five_bit_r = bech32.convertbits(r, 8, 5)
    assert five_bit_r is not None, "Unsuccessful bech32.convertbits call"
    return bech32.bech32_encode("cosmos", five_bit_r)


def privkey_to_address(privkey: bytes) -> str:
    pubkey = privkey_to_pubkey(privkey)
    return pubkey_to_address(pubkey)
