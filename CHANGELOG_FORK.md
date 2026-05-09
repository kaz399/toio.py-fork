# Changelog for toio.py-fork

This file summarizes changes made in the independent `toio.py-fork` branch.
For the upstream project changelog, see [CHANGELOG.md](./CHANGELOG.md).

## [Unreleased]

### Added

- Started independent fork distribution as `toio-py-fork` while keeping the import package name `toio`.
- Added scanner scan strategies:
  - `strategy="best"` keeps scanning until timeout and returns the best sorted candidates.
  - `strategy="quick"` returns as soon as the requested number of cubes are found.
- Added keyword argument (`**kwargs`) support to `MultipleToioCoreCubes` and `ToioCoreCube` initialization. This allows intuitive configuration of scan settings, such as `strategy="quick"`.
- Added the scanner strategies in response to [toio/toio.py#15](https://github.com/toio/toio.py/issues/15), which reported that `scan(num=N)` always waited for the full timeout while scans by cube ID or BLE address terminated early.
- Added `UniversalBleScanner.scan_best()` and `UniversalBleScanner.scan_quick()` helpers.
- Added validation for scanner strategy values.
- Added definition-level tests that do not require physical cubes:
  - BLE connection state handling for Bleak versions whose `connect()` and `disconnect()` methods return `None`.
  - Configuration command bytes for `set_collision_detection_threshold()`.
  - Scanner strategy behavior for `best` and `quick`.
  - `ToioCoreCube` initialization from `CubeInfo`.
- Added this fork-specific changelog.

### Changed

- Migrated package management from Poetry to uv with Hatchling as the build backend.
- Replaced `poetry.lock` and `poetry.toml` with `uv.lock`.
- Converted `pyproject.toml` from Poetry metadata to PEP 621 project metadata.
- Changed the PyPI distribution name from `toio.py` / `toio-py` to `toio-py-fork`.
- Updated project metadata and documentation links for the `toio.py-fork` repository.
- Updated the supported Python requirement metadata from Python 3.8.1 or later to Python 3.10 or later.
- Updated the Bleak requirement to `bleak>=3,<4`.
- Removed Poetry itself from the development dependency group.
- Updated tests and tooling metadata for the uv-based project layout.

### Fixed

- Fixed `Configuration.set_collision_detection_threshold()` to send `SetCollisionDetectionThreshold` instead of the horizontal detection threshold command.
- Fixed `BleCube.connect()` and `BleCube.disconnect()` handling for Bleak versions whose connect and disconnect methods return `None`.
- Fixed `BleCube` connection state tracking so `self.connected` follows `BleakClient.is_connected` after connect and disconnect operations.
- Fixed `ToioCoreCube` initialization with `CubeInfo`:
  - `CubeInfo.interface` is now used as the actual cube interface.
  - `CubeInfo.name` is used as the default cube name when no explicit name is provided.
- Fixed `ToioCoreCube` initialization in response to [toio/toio.py#14](https://github.com/toio/toio.py/issues/14), where the documentation described `CubeInfo` initialization but `connect()` failed because the `CubeInfo` object itself was used as the cube interface.
- Updated README examples to pass `CubeInfo` directly to `ToioCoreCube`.
- Fixed README motor notification examples to parse notifications with `Motor.is_my_data()`.
- Fixed README sample cleanup issues, including outdated arguments and trailing blank lines.
- Fixed definition-only test runs so they skip physical cube setup.
- Fixed the test helper command that generates `_cubes.py` to use the correct script path and safely quote paths.

### Documentation

- Added a README notice that this repository is an independent, unofficial fork and is not affiliated with, endorsed by, or sponsored by Sony Interactive Entertainment Inc. or toio(tm).
- Updated setup guides and contribution instructions to use `toio.py-fork` repository URLs and the `toio-py-fork` distribution name.
- Updated README installation examples to use `toio-py-fork`.
- Updated repository, package, and contribution references for the fork distribution.
- Documented the `CubeInfo` initialization fix for issue [toio/toio.py#14](https://github.com/toio/toio.py/issues/14).
- Documented scanner strategy usage and the relation to issue [toio/toio.py#15](https://github.com/toio/toio.py/issues/15).

### Commit Reference

- `e5b6d13`: Fixed `set_collision_detection_threshold()`.
- `a0fd102`, `7d12485`, `846c52f`: Fixed README sample code.
- `b1e3ac6`: Migrated package management from Poetry to uv.
- `b58637b`: Fixed Bleak connection state handling and improved definition-only tests.
- `af1a598`: Added a regression test for the collision threshold fix from `e5b6d13`.
- `871313a`: Fixed `ToioCoreCube` initialization from `CubeInfo` for [toio/toio.py#14](https://github.com/toio/toio.py/issues/14).
- `6c07f21`: Added scanner strategies for [toio/toio.py#15](https://github.com/toio/toio.py/issues/15).
- `fbf96d7`: Renamed the distribution and documentation references for `toio.py-fork`.
- `b2fabe3`: Added this fork changelog.
