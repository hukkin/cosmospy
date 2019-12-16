Changelog
=========

This log documents all public API breaking backwards incompatible changes.

**unreleased major**
-----
- Changed
    - Renamed `cosmospy.transactions` as `cosmospy.transaction`
    - Renamed `cosmospy.addresses` as `cosmospy.wallet`

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
