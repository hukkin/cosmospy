import base64
import json
from typing import Any, Dict, List

from secp256k1 import PrivateKey

from cosmospy.addresses import privkey_to_address, privkey_to_pubkey
from cosmospy.typing import SyncMode


class Transaction:
    """A Cosmos transaction.

    After initialization, one or more atom transfers can be added by
    calling the `add_transfer()` method. Finally, call
    `get_pushable_tx()` to get a signed transaction that can be pushed
    to the `POST /txs` endpoint of the Cosmos REST API.
    """

    def __init__(
        self,
        *,
        privkey: str,
        account_num: int,
        sequence: int,
        fee: int,
        gas: int,
        memo: str = "",
        chain_id: str = "cosmoshub-3",
        sync_mode: SyncMode = "sync",
    ) -> None:
        self._privkey = privkey
        self._account_num = account_num
        self._sequence = sequence
        self._fee = fee
        self._gas = gas
        self._memo = memo
        self._chain_id = chain_id
        self._sync_mode = sync_mode
        self._msgs: List[dict] = []

    def add_transfer(self, recipient: str, amount: int, denom: str = "uatom") -> None:
        transfer = {
            "type": "cosmos-sdk/MsgSend",
            "value": {
                "from_address": privkey_to_address(self._privkey),
                "to_address": recipient,
                "amount": [{"denom": denom, "amount": str(amount)}],
            },
        }
        self._msgs.append(transfer)

    def get_pushable_tx(self) -> str:
        pubkey = privkey_to_pubkey(self._privkey)
        base64_pubkey = base64.b64encode(bytes.fromhex(pubkey)).decode("utf-8")
        pushable_tx = {
            "tx": {
                "msg": self._msgs,
                "fee": {
                    "gas": str(self._gas),
                    "amount": [{"denom": "uatom", "amount": str(self._fee)}],
                },
                "memo": self._memo,
                "signatures": [
                    {
                        "signature": self._sign(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                        "account_number": str(self._account_num),
                        "sequence": str(self._sequence),
                    }
                ],
            },
            "mode": self._sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    def _sign(self) -> str:
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = PrivateKey(bytes.fromhex(self._privkey))
        signature = privkey.ecdsa_sign(message_bytes)
        signature_compact = privkey.ecdsa_serialize_compact(signature)

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str

    def _get_sign_message(self) -> Dict[str, Any]:
        return {
            "chain_id": self._chain_id,
            "account_number": str(self._account_num),
            "fee": {
                "gas": str(self._gas),
                "amount": [{"amount": str(self._fee), "denom": "uatom"}],
            },
            "memo": self._memo,
            "sequence": str(self._sequence),
            "msgs": self._msgs,
        }
