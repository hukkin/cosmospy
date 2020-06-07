Changelog
=========

This log documents all public API breaking backwards incompatible changes.

*unreleased major*
-----
- Added
    - `cosmospy.seed_to_privkey` function
- Changed
    - `cosmospy.typing.Wallet` now includes fields "seed" and "derivation_path"
    - Made private keys and public keys in all public interfaces type `bytes` instead of hex formatted `str`

4.0.0
-----
- Changed
    - `cosmospy.transactions` and `cosmospy.addresses` modules have been removed. All of their functions and classes are now importable directly from the `cosmospy` root. That is, users will have to `from cosmospy import Transaction` instead of `from cosmospy.transactions import Transaction`
    - `get_pushable_tx` method of the `Transaction` class renamed as `get_pushable`

3.0.0
-----
- Changed
    - `transactions.Transaction` init only takes keyword arguments.
    - `transactions.Transaction` keyword argument `chain_id` default value changed from "cosmoshub-2" to "cosmoshub-3"
    - Made all instance variables of `transactions.Transaction` private
    - Renamed `transactions.Transaction.add_atom_transfer` as `transactions.Transaction.add_transfer`

2.0.0
-----
- Changed
    - Renamed `transactions.UnsignedTransaction` as `transactions.Transaction`

1.0.0
-----
- Added
    - `addresses.pubkey_to_address()`
    - `transactions.UnsignedTransaction` class
- Removed
    - `transactions.sign_atom_transfer()`
    - `transactions.sign()`

0.0.1
-----
- Added
    - Code for address generation and transaction signing
