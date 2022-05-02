from unittest import mock

from ward import test

from cosmospy import generate_wallet, privkey_to_address, privkey_to_pubkey, seed_to_privkey
from cosmospy.typing import Wallet

test_vector: Wallet = {
    "seed": "todo",
    "derivation_path": "todo",
    "private_key": bytes.fromhex(
        "8088c2ed2149c34f6d6533b774da4e1692eb5cb426fdbaef6898eeda489630b7"
    ),
    "public_key": bytes.fromhex(
        "02ba66a84cf7839af172a13e7fc9f5e7008cb8bca1585f8f3bafb3039eda3c1fdd"
    ),
    "address": "cosmos1r5v5srda7xfth3hn2s26txvrcrntldjumt8mhl",
}

seed_test_vector: Wallet = {
    "seed": "teach there dream chase fatigue abandon lava super senior artefact close upgrade",
    "derivation_path": "m/44'/118'/0'/0/0",
    "private_key": bytes.fromhex(
        "8d0a8d165cf26d7a6f2dd621ed2fd9ebdb9596281906e48115f80164c0a64e1d"
    ),
    "public_key": bytes.fromhex(
        "036abfed6c95453a552160ca41487d42aafdbcd02aa62074056cc30cca2ea497a4"
    ),
    "address": "cosmos1luqsez2rktxckxmwk8k6g40whzncrv37vp0ufp",
}


@test("seed to privkey")
def _():
    assert (
        seed_to_privkey(seed_test_vector["seed"], path=seed_test_vector["derivation_path"])
        == seed_test_vector["private_key"]
    )


@test("privkey to pubkey")  # type: ignore[no-redef]
def _():
    assert privkey_to_pubkey(test_vector["private_key"]) == test_vector["public_key"]


@test("privkey to address")  # type: ignore[no-redef]
def _():
    assert privkey_to_address(test_vector["private_key"]) == test_vector["address"]


@test("generate wallet")  # type: ignore[no-redef]
def _():
    with mock.patch("os.urandom") as mock_urandom:
        mock_urandom.return_value = b"\x1e\xd2\x7f9\xa7\x0em\xfd\xa0\xb4\xaa\xc4\x0b\x83\x0e%\xbf\xe6DG\x7f:a\xe6#qa\x1ch5D\xa9"  # noqa: E501
        expected_wallet = {
            "seed": "burst negative solar evoke traffic yard lizard next series foster seminar enter wrist captain bulb trap giggle country sword season shoot boy bargain deal",  # noqa: E501
            "derivation_path": "m/44'/118'/0'/0/0",
            "private_key": bytes.fromhex(
                "bb8ac5bf9c342852fa5943d1366375c6f985d4601e596f23c5a49d095bfb2878"
            ),
            "public_key": bytes.fromhex(
                "03a7cc51198fc666901ec7b627926dad0c85d128ebe3251a132f009dcde1d64e03"
            ),
            "address": "cosmos1dep39rnnwztpt63jx0htxrkt3lgku2cdr5qawx",
        }
        assert generate_wallet() == expected_wallet
