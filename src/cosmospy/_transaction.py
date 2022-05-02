from __future__ import annotations

import base64
import hashlib
import json

import ecdsa

from cosmospy._typing import SyncMode
from cosmospy._wallet import DEFAULT_BECH32_HRP, privkey_to_address, privkey_to_pubkey
import cosmospy.interfaces.any_pb2 as Any
import cosmospy.interfaces.coin_pb2 as coin
import cosmospy.interfaces.msg_send_pb2 as transfer
import cosmospy.interfaces.ibc_transfer_pb2 as ibc_transfer
import cosmospy.interfaces.pubkey_pb2 as pubkey
import cosmospy.interfaces.tx_pb2 as tx


class Transaction:
    """A Cosmos transaction.

    After initialization, one or more token transfers can be added by
    calling the `add_transfer()` method. Finally, call `get_pushable()`
    to get a signed transaction that can be pushed to the `POST /txs`
    endpoint of the Cosmos REST API.
    """

    def __init__(
            self,
            *,
            privkey: bytes,
            account_num: int,
            sequence: int,
            fee: int,
            gas: int,
            fee_denom: str = "uatom",
            fee_account: str = "",
            memo: str = "",
            chain_id: str = "cosmoshub-4",
            hrp: str = DEFAULT_BECH32_HRP,
            sync_mode: SyncMode = "broadcast_tx_sync",
    ) -> None:
        self._privkey = privkey
        self._account_num = account_num
        self._sequence = sequence
        self._fee = fee
        self._fee_denom = fee_denom
        self._fee_account = fee_account
        self._gas = gas
        self._chain_id = chain_id
        self._hrp = hrp
        self._sync_mode = sync_mode
        self._tx_body = tx.TxBody()
        self._tx_body.memo = memo
        self._tx_raw = tx.TxRaw()

    def add_transfer(
            self, recipient: str, amount: int, denom: str = "uatom", hrp: str = DEFAULT_BECH32_HRP
    ) -> None:
        msg = transfer.MsgSend()
        msg.from_address = privkey_to_address(self._privkey, hrp=hrp)
        msg.to_address = recipient
        _amount = coin.Coin()
        _amount.denom = denom
        _amount.amount = str(amount)
        msg.amount.append(_amount)
        msg_any = Any.Any()
        msg_any.Pack(msg)
        msg_any.type_url = "/cosmos.bank.v1beta1.MsgSend"
        self._tx_body.messages.append(msg_any)

    def add_ibc_transfer(
            self, recipient: str, amount: int, channel: str, denom: str = "uatom", hrp: str = DEFAULT_BECH32_HRP,
            port: str = "transfer", timeout_height: int = 0, timeout_revision_number: int = 4,
            timeout_timestamp: int = 0
    ) -> None:
        msg = ibc_transfer.MsgTransfer()
        msg.source_port = port
        msg.source_channel = channel
        msg.sender = privkey_to_address(self._privkey, hrp=hrp)
        msg.receiver = recipient
        msg.token.denom = denom
        msg.token.amount = str(amount)

        if timeout_timestamp > 0:
            msg.timeout_timestamp = timeout_timestamp
        elif timeout_height > 0:
            msg.timeout_height.revision_height = timeout_height
            msg.timeout_height.revision_number = timeout_revision_number
        else:
            raise ValueError("You have to set either a timeout height or a timeout timestamp")

        msg_any = Any.Any()
        msg_any.Pack(msg)
        msg_any.type_url = "/ibc.applications.transfer.v1.MsgTransfer"
        self._tx_body.messages.append(msg_any)

    def _get_tx_bytes(self) -> str:
        self._tx_raw.body_bytes = self._tx_body.SerializeToString()
        self._tx_raw.auth_info_bytes = self._get_auth_info().SerializeToString()
        self._tx_raw.signatures.append(self._get_signatures())
        raw_tx = self._tx_raw.SerializeToString()
        tx_bytes = bytes(raw_tx)
        tx_b64 = base64.b64encode(tx_bytes).decode("utf-8")
        return tx_b64

    def _get_signatures(self):
        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            self._get_sign_doc().SerializeToString(),
            hashfunc=hashlib.sha256,
            sigencode=ecdsa.util.sigencode_string_canonize,
        )
        return signature_compact

    def _get_sign_doc(self):
        sign_doc = tx.SignDoc()
        sign_doc.body_bytes = self._tx_body.SerializeToString()
        sign_doc.auth_info_bytes = self._get_auth_info().SerializeToString()
        sign_doc.chain_id = self._chain_id
        sign_doc.account_number = self._account_num
        return sign_doc

    def _get_auth_info(self):
        _auth_info = tx.AuthInfo()
        _auth_info.signer_infos.append(self._get_signer_infos(self._get_pubkey()))
        _auth_info.fee.gas_limit = self._gas
        if self._fee_account:
            _auth_info.fee.granter = self._fee_account
        _auth_info.fee.amount.append(self._get_fee())
        return _auth_info

    def _get_fee(self):
        _fee = coin.Coin()
        _fee.amount = str(self._fee)
        _fee.denom = self._fee_denom
        return _fee

    def _get_pubkey(self):
        pubkey_bytes = privkey_to_pubkey(self._privkey)
        _pubkey = pubkey.PubKey()
        _pubkey.key = pubkey_bytes
        return _pubkey

    def _get_signer_infos(self, _pubkey):
        signer_infos = tx.SignerInfo()
        signer_infos.sequence = self._sequence
        signer_infos.public_key.Pack(_pubkey)
        signer_infos.public_key.type_url = "/cosmos.crypto.secp256k1.PubKey"
        signer_infos.mode_info.single.mode = 1
        return signer_infos

