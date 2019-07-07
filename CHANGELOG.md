Changelog
=========

This log should always be updated when doing backwards incompatible changes, resulting in a major version bump. Feel free to add a log for lesser version bumps as well, but for major bumps it's a must.

**unreleased major**
-----
- Changed
    - `transactions.Transaction` init only takes keyword arguments.

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
