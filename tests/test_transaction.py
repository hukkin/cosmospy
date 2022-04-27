from unittest.mock import Mock

from ward import test

from cosmospy import Transaction



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
    pushable_tx = tx.get_pushable()
    assert pushable_tx == expected_pushable_tx
