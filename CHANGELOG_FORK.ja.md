# toio.py-fork の変更履歴

このファイルは、独自の `toio.py-fork` ブランチで行った変更をまとめたものです。
公式プロジェクトの変更履歴については [CHANGELOG.md](./CHANGELOG.md) を参照してください。

## [未リリース]

### 追加

- toioコアキューブ技術仕様 v2.5.0 で追加されたAPIへの対応を追加しました：
  - スピーカー消音設定：`SetSpeakerMute` (command 0x33) および `ResponseSpeakerMuteSettings` (response 0xB3)。
  - 保存した設定の初期化：`ResetConfiguration` (command 0x0F) および `ResponseConfigurationReset` (response 0x8F)。
  - リモート電源オフ：`RequestRemotePowerOff` (command 0x34) および `ResponseRemotePowerOff` (response 0xB4)。
  - 現在のコネクションインターバル値の取得：`GetCurrentConnectionIntervalValue` (command 0x32) および `ResponseGettingCurrentConnectionInterval` (response 0xB2)。
  - ランプのなめらかな点滅：`SmoothFlashing` (command 0x70)。
  - これらの機能を `AsyncSimpleCube` に統合しました。
- `ToioCoreCube` の `SUPPORTED_MINOR_VERSION` を `5` に更新しました。
- import package 名 `toio` は維持したまま、PyPI distribution 名を `toio-py-fork` とする独自 fork 配布を開始しました。
- scanner に scan strategy を追加しました。
  - `strategy="best"` は timeout まで scan を続け、sort 後の最良候補を返します。
  - `strategy="quick"` は指定数の cube が見つかった時点で scan を終了して返します。
- `MultipleToioCoreCubes` および `ToioCoreCube` の `__init__` にキーワード引数（`**kwargs`）のサポートを追加しました。これにより、`strategy="quick"` などのスキャン設定を直感的に指定できるようになりました。
- scanner strategy は、`scan(num=N)` が常に timeout まで待つ一方で、cube ID や BLE address を指定した scan は対象がすべて見つかった時点で終了することを指摘した [toio/toio.py#15](https://github.com/toio/toio.py/issues/15) への対応として追加しました。
- `UniversalBleScanner.scan_best()` と `UniversalBleScanner.scan_quick()` の helper を追加しました。
- scanner strategy 値の validation を追加しました。
- 実機 cube を必要としない definition-level test を追加しました。
  - `connect()` / `disconnect()` が `None` を返す Bleak version 向けの BLE connection state handling。
  - `set_collision_detection_threshold()` の configuration command byte。
  - `best` / `quick` の scanner strategy 動作。
  - `CubeInfo` からの `ToioCoreCube` 初期化。
- この fork 専用の changelog を追加しました。

### 変更

- package management を Poetry から uv に移行し、build backend を Hatchling に変更しました。
- `poetry.lock` と `poetry.toml` を削除し、`uv.lock` を追加しました。
- `pyproject.toml` を Poetry metadata 形式から PEP 621 project metadata 形式に移行しました。
- PyPI distribution 名を `toio.py` / `toio-py` から `toio-py-fork` に変更しました。
- `toio.py-fork` repository 用に project metadata と documentation link を更新しました。
- 対応 Python version の metadata を Python 3.8.1 以上から Python 3.10 以上に変更しました。
- Bleak の requirement を `bleak>=3,<4` に更新しました。
- development dependency group から Poetry 自体を削除しました。
- uv ベースの project layout に合わせて tests と tooling metadata を更新しました。

### 修正

- `Configuration.set_collision_detection_threshold()` が horizontal detection threshold command ではなく `SetCollisionDetectionThreshold` を送信するよう修正しました。
- `connect()` / `disconnect()` が `None` を返す Bleak version に対応するため、`BleCube.connect()` と `BleCube.disconnect()` の handling を修正しました。
- `BleCube` の connection state tracking を修正し、connect / disconnect 後に `self.connected` が `BleakClient.is_connected` に追従するようにしました。
- `CubeInfo` を使った `ToioCoreCube` 初期化を修正しました。
  - `CubeInfo.interface` を実際の cube interface として使うようにしました。
  - 明示的に name が指定されていない場合は `CubeInfo.name` を default cube name として使うようにしました。
- 説明文では `CubeInfo` で初期化できると読める一方で、実際には `CubeInfo` 自体を cube interface として扱ってしまい `connect()` に失敗する [toio/toio.py#14](https://github.com/toio/toio.py/issues/14) への対応として、`ToioCoreCube` の `CubeInfo` 初期化を修正しました。
- README の sample code で `ToioCoreCube` に `CubeInfo` を直接渡す例を追加しました。
- README の motor notification example で `Motor.is_my_data()` を使って notification を parse するよう修正しました。
- README sample の古い argument や末尾の不要な空行を修正しました。
- definition-only test 実行時に、実機 cube の setup を skip するよう修正しました。
- `_cubes.py` を生成する test helper command で、正しい script path を使い path を安全に quote するよう修正しました。

### ドキュメント

- この repository が Sony Interactive Entertainment Inc. または toio(tm) と提携、承認、支援関係にない独立した非公式 fork であることを README に追記しました。
- setup guide と contribution instruction を `toio.py-fork` repository URL と `toio-py-fork` distribution 名に更新しました。
- README の installation example を `toio-py-fork` に更新しました。
- fork distribution に合わせて repository、package、contribution 関連の参照を更新しました。
- [toio/toio.py#14](https://github.com/toio/toio.py/issues/14) に対する `CubeInfo` 初期化修正の説明を追加しました。
- [toio/toio.py#15](https://github.com/toio/toio.py/issues/15) に対する scanner strategy の使い方と対応関係を説明しました。
