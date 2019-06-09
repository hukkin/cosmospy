import cosmospy.addresses as address

test_vector = {
    "private_key": "8088c2ed2149c34f6d6533b774da4e1692eb5cb426fdbaef6898eeda489630b7",
    "public_key": "02ba66a84cf7839af172a13e7fc9f5e7008cb8bca1585f8f3bafb3039eda3c1fdd",
    "address": "cosmos1r5v5srda7xfth3hn2s26txvrcrntldjumt8mhl",
}


def test_privkey_to_pubkey():
    assert address.privkey_to_pubkey(test_vector["private_key"]) == test_vector["public_key"]


def test_privkey_to_address():
    assert address.privkey_to_address(test_vector["private_key"]) == test_vector["address"]


def test_generate_wallet(mocker):
    mock_urandom = mocker.patch("os.urandom")
    mock_urandom.return_value = (
        b"\x1e\xd2\x7f9\xa7\x0em\xfd\xa0\xb4\xaa\xc4\x0b\x83\x0e%\xbf\xe6DG\x7f:a\xe6#qa\x1ch5D\xaa"
    )  # noqa: E501
    expected_wallet = {
        "private_key": "1ed27f39a70e6dfda0b4aac40b830e25bfe644477f3a61e62371611c683544aa",
        "public_key": "02a0ebf78f928723ee4fed610115263a33e49492502b6ead39e61481d6d5b096c6",
        "address": "cosmos1z47ev5u5ujmc7kwv49tut7raesg55tjyplywdy",
    }
    assert address.generate_wallet() == expected_wallet
