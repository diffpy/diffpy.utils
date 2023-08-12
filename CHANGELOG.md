# Release notes

## Version 3.2.0 – 2023-08-**

### Added

- CI Coverage.
- New tests for loadData function.
- loadData function now toggleable. Can return either (a) data read from data blocks or (b) header
information stored above the data block.

### Removed

- Remove use of pkg_resources (deprecated).
- No longer use Travis.

## Version 3.1.0 – 2022-12-09

### Added

- Compatibility with Python 3.10, 3.9, 3.8

### Removed

- Remove the support for Python 3.5, 3.6.

## Version 3.0.0 -- 2019-03-12

Differences from version 1.2.2.

### Added

- Compatibility with Python 3.7, 3.6, 3.5 in addition to 2.7.

### Changed

- Switch to platform-independent "noarch" Anaconda package.

### Deprecated

- Variable `__gitsha__` in the `version` module which was renamed
  to `__git_commit__`.
