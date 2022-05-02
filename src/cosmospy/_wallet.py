import hashlib

import bech32
import ecdsa
import hdwallets
import mnemonic

from cosmospy import BIP32DerivationError
from cosmospy.typing import Wallet

DEFAULT_DERIVATION_PATH = "m/44'/118'/0'/0/0"
DEFAULT_BECH32_HRP = "cosmos"


def generate_wallet(
    *, path: str = DEFAULT_DERIVATION_PATH, hrp: str = DEFAULT_BECH32_HRP
) -> Wallet:
    while True:
        phrase = mnemonic.Mnemonic(language="english").generate(strength=256)
        try:
            privkey = seed_to_privkey(phrase, path=path)
            break
        except BIP32DerivationError:
            pass
    pubkey = privkey_to_pubkey(privkey)
    address = pubkey_to_address(pubkey, hrp=hrp)
    return {
        "seed": phrase,
        "derivation_path": path,
        "private_key": privkey,
        "public_key": pubkey,
        "address": address,
    }


def seed_to_privkey(seed: str, path: str = DEFAULT_DERIVATION_PATH) -> bytes:
    """Get a private key from a mnemonic seed and a derivation path.

    Assumes a BIP39 mnemonic seed with no passphrase. Raises
    `cosmospy.BIP32DerivationError` if the resulting private key is
    invalid.
    """
    seed_bytes = mnemonic.Mnemonic.to_seed(seed, passphrase="")
    hd_wallet = hdwallets.BIP32.from_seed(seed_bytes)
    # This can raise a `hdwallets.BIP32DerivationError` (which we alias so
    # that the same exception type is also in the `cosmospy` namespace).
    derived_privkey = hd_wallet.get_privkey_from_path(path)

    return derived_privkey


def privkey_to_pubkey(privkey: bytes) -> bytes:
    privkey_obj = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
    pubkey_obj = privkey_obj.get_verifying_key()
    return pubkey_obj.to_string("compressed")


def pubkey_to_address(pubkey: bytes, *, hrp: str = DEFAULT_BECH32_HRP) -> str:
    s = hashlib.new("sha256", pubkey).digest()
    r = hashlib.new("ripemd160", s).digest()
    five_bit_r = bech32.convertbits(r, 8, 5)
    assert five_bit_r is not None, "Unsuccessful bech32.convertbits call"
    return bech32.bech32_encode(hrp, five_bit_r)


def privkey_to_address(privkey: bytes, *, hrp: str = DEFAULT_BECH32_HRP) -> str:
    pubkey = privkey_to_pubkey(privkey)
    return pubkey_to_address(pubkey, hrp=hrp)
