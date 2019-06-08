from typing import Dict, List, Any
import json
import base64

from secp256k1 import PrivateKey

from cosmospy.addresses import privkey_to_address, privkey_to_pubkey


def sign(private_key: str, message: Dict[str, Any]) -> str:
    message_str = json.dumps(message, separators=(',', ':'), sort_keys=True)
    message_bytes = message_str.encode('utf-8')

    privkey = PrivateKey(bytes.fromhex(private_key))
    signature = privkey.ecdsa_sign(message_bytes)
    signature_compact = privkey.ecdsa_serialize_compact(signature)

    signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
    return signature_base64_str


def _make_atom_transfer_msg(sender: str, recipient: str, amount: int) -> Dict[str, Any]:
    return {
        "type": "cosmos-sdk/MsgSend",
        "value": {
            "from_address": sender,
            "to_address": recipient,
            "amount": [
                {
                    "denom": "uatom",
                    "amount": str(amount),
                },
            ],
        },
    }


def _make_sign_message(msgs: List[Dict], account_num: int, sequence: int, fee: int, gas: int,
                       memo: str, chain_id: str) -> Dict[str, Any]:
    return {
        "chain_id": chain_id,
        "account_number": str(account_num),
        "fee": {
            "gas": str(gas),
            "amount": [{"amount": str(fee), "denom": "uatom"}],
        },
        "memo": memo,
        "sequence": str(sequence),
        "msgs": msgs,
    }


def _make_pushable_tx(msgs: List[Dict], signature: str, public_key: str, account_num: int,
                      sequence: int, fee: int, gas: int, memo: str, mode: str) -> str:
    base64_pubkey = base64.b64encode(bytes.fromhex(public_key)).decode("utf-8")
    pushable_tx = {
        "tx": {
            "msg": msgs,
            "fee": {
                "gas": str(gas),
                "amount": [
                    {
                        "denom": "uatom",
                        "amount": str(fee),
                    },
                ],
            },
            "memo": memo,
            "signatures": [
                {
                    "signature": signature,
                    "pub_key": {
                        "type": "tendermint/PubKeySecp256k1",
                        "value": base64_pubkey,
                    },
                    "account_number": str(account_num),
                    "sequence": str(sequence),
                },
            ],
        },
        "mode": mode,
    }
    return json.dumps(pushable_tx, separators=(',', ':'))


def sign_atom_transfer(private_key: str, to: str, amount: int, account_num: int, sequence: int,
                       fee: int, gas: int = 37000, memo: str = '', chain_id: str = 'cosmoshub-2',
                       ) -> str:
    sender = privkey_to_address(private_key)
    transfer_message = _make_atom_transfer_msg(sender, to, amount)
    sign_message = _make_sign_message([transfer_message], account_num, sequence,
                                      fee, gas, memo, chain_id)
    sig = sign(private_key, sign_message)
    pubkey = privkey_to_pubkey(private_key)
    pushable_tx = _make_pushable_tx([transfer_message], sig, pubkey, account_num, sequence, fee,
                                    gas, memo, 'sync')
    return pushable_tx
