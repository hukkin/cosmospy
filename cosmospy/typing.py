from typing_extensions import Literal, TypedDict


SyncMode = Literal["sync", "async", "block"]


class Wallet(TypedDict):
    private_key: str
    public_key: str
    address: str
