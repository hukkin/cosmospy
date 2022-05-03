from cosmospy import Transaction
from cosmospy import privkey_to_address
print(privkey_to_address(bytes.fromhex("26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59")))
tx = Transaction(
    privkey=bytes.fromhex(
        "26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59"
    ),
    account_num=24615,
    sequence=4,
    fee=1000,
    gas=70000,
    memo="",
    chain_id="cosmoshub-4",
)
tx.add_transfer(
    recipient="cosmos103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf", amount=387000
)
tx.add_transfer(recipient="cosmos1lzumfk6xvwf9k9rk72mqtztv867xyem393um48", amount=123)


import httpx
import json

tx_bytes = tx.get_tx_bytes()


# Submit the transaction through the Tendermint RPC
rpc_url = "https://rpc.cosmos.network/"
pushable_tx = json.dumps({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "broadcast_tx_sync", # Available methods: broadcast_tx_sync, broadcast_tx_async, broadcast_tx_commit
                "params": {
                    "tx": str(tx_bytes)
                }
              })
print(pushable_tx)

r = httpx.post(rpc_url, data=pushable_tx)
print(r.text)
# Submit the transaction through the Cosmos REST API
rpc_api = "https://api.cosmos.network/cosmos/tx/v1beta1/txs"
pushable_tx = json.dumps({
                "tx_bytes": tx_bytes,
                "mode": "BROADCAST_MODE_SYNC" # Available modes: BROADCAST_MODE_SYNC, BROADCAST_MODE_ASYNC, BROADCAST_MODE_BLOCK
            })

r = httpx.post(rpc_api, data=pushable_tx)
print(r.text)