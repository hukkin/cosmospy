from typing import Dict, List, Any
import json
import base64

from secp256k1 import PrivateKey

from cosmospy.addresses import privkey_to_address, privkey_to_pubkey


class UnsignedTransaction:
    def __init__(
        self,
        privkey: str,
        account_num: int,
        sequence: int,
        fee: int,
        gas: int,
        memo: str = "",
        chain_id: str = "cosmoshub-2",
        sync_mode: str = "sync",
    ) -> None:
        self.privkey = privkey
        self.account_num = account_num
        self.sequence = sequence
        self.fee = fee
        self.gas = gas
        self.memo = memo
        self.chain_id = chain_id
        self.sync_mode = sync_mode
        self.msgs: List[Dict] = []

    def add_atom_transfer(self, recipient: str, amount: int) -> None:
        self.msgs.append(
            {
                "type": "cosmos-sdk/MsgSend",
                "value": {
                    "from_address": privkey_to_address(self.privkey),
                    "to_address": recipient,
                    "amount": [{"denom": "uatom", "amount": str(amount)}],
                },
            }
        )

    def _get_sign_message(self) -> Dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "account_number": str(self.account_num),
            "fee": {"gas": str(self.gas), "amount": [{"amount": str(self.fee), "denom": "uatom"}]},
            "memo": self.memo,
            "sequence": str(self.sequence),
            "msgs": self.msgs,
        }

    def _sign(self) -> str:
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = PrivateKey(bytes.fromhex(self.privkey))
        signature = privkey.ecdsa_sign(message_bytes)
        signature_compact = privkey.ecdsa_serialize_compact(signature)

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str

    def get_pushable_tx(self) -> str:
        pubkey = privkey_to_pubkey(self.privkey)
        base64_pubkey = base64.b64encode(bytes.fromhex(pubkey)).decode("utf-8")
        pushable_tx = {
            "tx": {
                "msg": self.msgs,
                "fee": {
                    "gas": str(self.gas),
                    "amount": [{"denom": "uatom", "amount": str(self.fee)}],
                },
                "memo": self.memo,
                "signatures": [
                    {
                        "signature": self._sign(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                        "account_number": str(self.account_num),
                        "sequence": str(self.sequence),
                    }
                ],
            },
            "mode": self.sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))
