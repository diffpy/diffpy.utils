**Added**
- Compatability with Python 3.12, 3.11
- CI Coverage.
- New tests for loadData function.
- loadData function now toggleable. Can return either (a) data read from data blocks or (b) header
information stored above the data block.

**Removed**
- Remove use of pkg_resources (deprecated).
- No longer use Travis.