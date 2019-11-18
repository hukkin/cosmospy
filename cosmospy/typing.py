import sys

if sys.version_info < (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict


# Valid transaction broadcast modes for the `POST /txs` endpoint of the
# Cosmos REST API.
SyncMode = Literal["sync", "async", "block"]


class Wallet(TypedDict):
    private_key: str
    public_key: str
    address: str
