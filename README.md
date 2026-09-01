# Kestrel-1 rover

Firmware and tools for the Kestrel-1 rover.

| Folder | What is in it |
|---|---|
| src/ | Python firmware: motion commands, range sensor, limits |
| tools/ | The obstacle detector |
| data/ | Field run logs (they stay on your machine) |
| tests/ | Unit tests |

## Team rule

`main` holds only reviewed work. Start every new piece of work on its own branch.

## Quick check

    python3 tests/test_rover.py
