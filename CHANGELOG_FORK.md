# Changelog for toio.py-fork

This file summarizes changes made in the independent `toio.py-fork` branch.
For the upstream project changelog, see [CHANGELOG.md](./CHANGELOG.md).

## [Unreleased]

### Added

- Started independent fork distribution as `toio-py-fork` while keeping the import package name `toio`.
- Added scanner strategies:
  - `strategy="best"` keeps scanning until timeout and returns the best sorted candidates.
  - `strategy="quick"` returns as soon as the requested number of cubes are found.
- Added `UniversalBleScanner.scan_best()` and `UniversalBleScanner.scan_quick()` helpers.
- Added definition-level tests for BLE connection state handling, configuration commands, scanner strategies, and `ToioCoreCube` initialization.

### Changed

- Migrated package management from Poetry to uv with Hatchling as the build backend.
- Updated project metadata and documentation links for the `toio.py-fork` repository.
- Changed the PyPI distribution name from `toio.py` / `toio-py` to `toio-py-fork`.
- Updated the package requirement metadata to Python 3.10 or later and `bleak>=3,<4`.
- `ToioCoreCube` now accepts `CubeInfo` during initialization and derives the cube interface and default name from it.

### Fixed

- Fixed `Configuration.set_collision_detection_threshold()` to send `SetCollisionDetectionThreshold` instead of the horizontal detection threshold command.
- Fixed `BleCube.connect()` and `BleCube.disconnect()` handling for Bleak versions whose connect and disconnect methods return `None`.
- Fixed README examples to pass `CubeInfo.interface` to `ToioCoreCube`.
- Fixed README motor notification examples to parse notifications with `Motor.is_my_data()`.

### Documentation

- Added a README notice that this repository is an independent, unofficial fork and is not affiliated with, endorsed by, or sponsored by Sony Interactive Entertainment Inc. or toio(tm).
- Updated setup guides and contribution instructions to use `toio.py-fork` repository URLs and the `toio-py-fork` distribution name.
