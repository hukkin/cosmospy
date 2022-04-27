from unittest.mock import Mock

from ward import test

from cosmospy import Transaction, seed_to_privkey


@test("make transaction pushable to the HTTP API")  # type: ignore[no-redef]
def _():
    expected_pushable_tx = '{' \
                               '"tx_bytes": ' \
                                '"CpIBCo8BChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEm8KLWNvc21vczFsZ2hhcnpnZHM4OWxwc2hyN3E4a2NtZDJlc254a2Zwd3Z1ejV0chItY29zbW9zMTAzbDc1OHBzNzQwM3NkOWMweThqNmhyZnc0eHlsNzBqNG1td2tmGg8KBXVhdG9tEgYzODcwMDASZQpOCkYKHy9jb3Ntb3MuY3J5cHRvLnNlY3AyNTZrMS5QdWJLZXkSIwohA49sjCd3Eul+ZXyof7qO460UaO73otrmySHyTNSLW+XnEgQKAggBEhMKDQoFdWF0b20SBDEwMDAQiKECGkCCxnkkE/Rqp4q+qAb41KV3JWhzb/BFMO3+9b0hN9TcQx2mfz6Nv1XQ1NT5LQ7EnaErq56siOXV2dQTy0zt5TqC", ' \
                               '"mode": "BROADCAST_MODE_SYNC"' \
                           '}'
    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        privkey=bytes.fromhex("26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59"),
        account_num=11335,
        sequence=0,
        fee=fee,
        gas=37000,
        chain_id="cosmoshub-4",
    )
    tx.add_transfer(recipient="cosmos103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf", amount=amount)
    pushable_tx = tx.get_api_pushable()
    assert pushable_tx == expected_pushable_tx

@test("check ibc transactions and non cosmos transaction")  # type: ignore[no-redef]
def _():
    expected_pushable_tx = '{"jsonrpc": "2.0", "id": 1, "method": "broadcast_tx_sync", "params": {"tx": "CoUCCrwBCikvaWJjLmFwcGxpY2F0aW9ucy50cmFuc2Zlci52MS5Nc2dUcmFuc2ZlchKOAQoIdHJhbnNmZXISCWNoYW5uZWwtMRoPCgV1YnRzZxIGMTAwMDAwIi5iaXRzb25nMWczbXFwM2hqMmt4cmh4dXUybGVsaG5oOTIzdTZla3VzcWhmdGN4Ki1jb3Ntb3MxNGo4NGdzcWE4Y2E0bDl0NXNmMHY2OW1tcnBkcGVsanh1dW5obHgyBwgEEOys8wQSRFRoaXMgSUJDIHRyYW5zZmVyIGhhcyBiZWVuIG1hZGUgdGhyb3VnaCBjb3Ntb3NweS4gUHl0aG9uIGdvZXMgSUJDQ0NDEmYKTgpGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQPbp/M6yrmPLCwUmKk+i5M02RwLZod04J5GF6mOr4FBWBIECgIIARIUCg0KBXVidHNnEgQxMDAwEKDq4QEaQAl6y+Xfnwf/MLjGCBI8QtXBu2YnrQk32/jO0gMEkeVnAZgJhVqcNW6BhCDohW/URcdOiSBdzDL/LlU/KQ2fZ3c="}}'
    tx = Transaction(
        privkey=seed_to_privkey("agent pistol potato melt wagon buyer web infant sound loyal rapid buzz",
                                path="m/44'/639'/0'/0/0"),
        hrp="bitsong",
        account_num=20809,
        sequence=0,
        fee=1000,
        fee_denom="ubtsg",
        gas=3700000,
        chain_id="bitsong-2b",
        memo="This IBC transfer has been made through cosmospy. Python goes IBCCCC"
    )
    tx.add_ibc_transfer(recipient="cosmos14j84gsqa8ca4l9t5sf0v69mmrpdpeljxuunhlx", amount=100000, channel="channel-1",
                        denom="ubtsg", hrp="bitsong", timeout_height=10278508)  #

    pushable_tx = tx.get_rpc_pushable() # https://www.mintscan.io/bitsong/txs/84F47E0F770D60674E33EC3ABF785DB06A3C3AEBB61133967CD71085F1D0DD34
    assert pushable_tx == expected_pushable_tx
