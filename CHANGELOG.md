Changelog
=========

This log should always be updated when doing backwards incompatible changes, resulting in a major version bump. Feel free to add a log for lesser version bumps as well, but for major bumps it's a must.

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
