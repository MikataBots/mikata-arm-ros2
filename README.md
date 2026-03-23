# mikata-arm-ros2
[![Build](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml)

MikataArmロボット用のROS 2パッケージ（MoveIt2対応）

## 開発環境

このプロジェクトはVS Code Dev Containersを使用して開発します。

## 前提条件

- **Docker** 20.10以降 - [インストールガイド](https://docs.docker.com/engine/install/)
- **VS Code** 1.70以降 - [ダウンロード](https://code.visualstudio.com/)
- **Dev Containers拡張機能** - VS Codeの拡張機能ストアから「Dev Containers」をインストール

> **詳細なセットアップ手順**: [docs/setup-detailed.md](docs/setup-detailed.md)を参照してください。

## 1. セットアップ

### 1.1. リポジトリのクローン

```bash
git clone https://github.com/MikataBots/mikata-arm-ros2.git
cd mikata-arm-ros2
```

### 1.2. VS Codeでプロジェクトを開く

```bash
code .
```

### 1.3. Dev Containerで開く

VS Codeでプロジェクトを開くと、右下に通知が表示されます：

```
Folder contains a Dev Container configuration file.
Reopen folder to develop in a container.
```

**Reopen in Container** ボタンをクリックしてください。

> **通知が表示されない場合**: `F1` → `Dev Containers: Reopen in Container` を実行

**初回起動時はDockerイメージのビルドに5〜10分かかります。** ステータスバーに進捗が表示されます。

### 1.4. 起動確認

コンテナが起動したら、VS Codeのターミナルを開いて、以下のコマンドで確認します：

```bash
ros2 doctor

# 出力例
# $ros2 doctor
# ...(中略)...
# /opt/ros/humble/lib/python3.10/site-packages/ros2doctor/api/package.py: 119: UserWarning: Cannot find the latest versions of packages: pantilt_bot_description mikata_arm_bringup mikata_arm_moveit mikata_arm_description [...] Use `ros2 doctor --report` to see full list.
# 
# All 5 checks passed
# 
```

> **セットアップの確認**: 環境が正しく動作するか確認する方法は、[docs/setup-detailed.md](docs/setup-detailed.md#セットアップの確認)を参照してください。

> **トラブルシューティング**: セットアップで問題が発生した場合は、[docs/setup-detailed.md](docs/setup-detailed.md#トラブルシューティング)を参照してください。


## 2. MikataArmのシミュレーション

シミュレーションモードでMikataArmを動かします。

### 2.1. ビルドとデモ起動

1) ワークスペースをビルド

```bash
cd /home/ros/ws_mikata_arm
colcon build --symlink-install
```

2) セットアップスクリプトを読み込む

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

3) シミュレーションモードでデモを起動

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=true
```

### 2.2. RVizでの操作確認

デモが起動すると、RVizウィンドウが表示されます。

**期待される表示**:
- 左側: MikataArmのロボットモデル（6軸アーム + グリッパー）
- 右側: MotionPlanningプラグインのコントロールパネル

**基本的な操作手順**:

1. **ゴール位置の設定**
   - 青色の球体（インタラクティブマーカー）をドラッグして、目標位置を設定
   - マーカーの矢印をドラッグすると、軸に沿って移動
   - リング部分をドラッグすると、回転

2. **経路計画**
   - MotionPlanningパネルの **Planning** タブを開く
   - **Plan** ボタンをクリック
   - 半透明なロボットの動作が表示されれば経路計画成功

3. **実行**
   - **Execute** ボタンをクリック
   - ロボットが計画された経路に沿って動く

4. **グリッパーの操作**
   - **Planning Group** で `hand` を選択
   - **Select Goal State** で `open` または `close` を選択
   - **Plan & Execute** をクリック

### 2.3. トラブルシュート

**ロボットが表示されない**

- RVizのFixedFrameが `world` または `base_link` に設定されているか確認
- ターミナルのログで `move_group` が正常に起動しているか確認
  - `process has died [move_group]` が出ていないこと

**`move_group` が起動失敗する**

- `InvalidParameterTypeException` エラーが出る場合、YAMLファイルの数値型を確認
  - [mikata_arm_moveit/config/joint_limits.yaml](mikata_arm_moveit/config/joint_limits.yaml)の値は浮動小数表記（例: `7.0`）にする


## 3. 実機への接続

実機のMikataArmに接続してデモを実行します。

> **前提**: 2章のシミュレーションが正常に動作することを確認してください。

### 3.1. ハードウェアのセットアップ

**デバイスの確認**:

MikataArmをUSBで接続し、デバイスが認識されているか確認します：

```bash
ls -l /dev/ttyUSB* /dev/ttyACM*
# 出力例: crw-rw---- 1 root dialout 188, 0 Mar 12 10:00 /dev/ttyUSB0
```

通常は `/dev/ttyUSB0` ですが、`/dev/ttyACM0` などの場合もあります。

**デバイスが見つからない場合**: [4.1章](#41-usbデバイスが見つからない場合)を参照

**パーミッションの確認**:

```bash
groups
# 出力に "dialout" が含まれていればOK
```

> **注意**: このプロジェクトのDockerイメージは、dialoutグループへの追加が自動で設定されています。古いコンテナを使用している場合は、`Dev Containers: Rebuild Container` でリビルドしてください。

### 3.2. 実機でのデモ実行

1) セットアップスクリプトを読み込む（未実行の場合）

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

2) 実機モードでデモを起動

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false
```

デバイスが `/dev/ttyUSB0` 以外の場合：

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0
```

### 3.3. 実機での動作確認と注意点

**起動時の確認**:

ターミナルに以下のようなログが表示されれば、実機との接続成功です：

```
[ros2_control_node]: Loaded controller 'mikata_arm_controller'
[ros2_control_node]: Loaded controller 'hand_controller'
[ros2_control_node]: Configured and activated all controllers
```

**実機操作時の注意点**:

⚠️ **安全上の注意**:
- 初めて動かす際は、緊急停止できる準備をしてください
- ロボットの動作範囲に障害物や人がいないことを確認してください
- 大きな移動をする前に、小さな動きでテストしてください

**推奨される動作確認手順**:

1. **グリッパーのテスト**
   - Planning Group: `hand`
   - Select Goal State: `open` を選択
   - **Plan & Execute** をクリック
   - `open` ↔ `close` を繰り返して動作確認

2. **既定のポーズに移動**
   - Planning Group: `mikata_arm`
   - Select Goal State: `rest` を選択
   - **Plan & Execute** をクリック
   - ロボットが安全な姿勢（rest pose）に移動します

3. **小さな動きでテスト**
   - インタラクティブマーカーを **少しだけ** ドラッグ
   - **Plan** でパスを確認
   - 軌跡が問題なさそうなら **Execute**


**トラブルシューティング**:
- ロボットが動かない → [4章](#4-トラブルシューティング)を参照
- 接続エラーが出る → USBポートとパーミッションを確認


## 4. トラブルシューティング

### 4.1. USBデバイスが見つからない場合

`ls -l /dev/ttyUSB* /dev/ttyACM*` を実行してもデバイスが表示されない場合：

#### 1. USBデバイスの接続確認

```bash
lsusb
```

MikataArmが接続されていれば、以下のような出力が表示されます：
- FTDI製チップ: `Future Technology Devices International`
- その他のチップ: メーカー名（例: `Prolific`, `Silicon Labs`）

デバイスが表示されない場合、USBケーブルや接続を確認してください。

#### 2. デバイスファイルの特定

```bash
# すべてのシリアルデバイスを確認
ls -l /dev/tty* | grep -E "(USB|ACM)"

# またはdmesgでカーネルログを確認
dmesg | grep -i "tty"
```

MikataArmを抜き差しして、どのデバイス名が追加/削除されるか確認してください。

#### 3. デバイス名が ttyUSB0 以外の場合

起動時に `usb_port` パラメータで指定：

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0
```

### 4.2. dialoutグループの権限問題

古いコンテナを使用している場合：

```bash
sudo usermod -aG dialout ros
```

その後、コンテナを再起動：

```bash
# ホスト側で実行
docker restart mikata-arm-ros2-dev
```

VS Codeで再接続してください。

### 4.3. Permission deniedエラー

`dialout` グループに所属しても「Permission denied」が出る場合：

```bash
ls -l /dev/ttyUSB0
```

グループが `dialout` でない場合（例: `root`）、一時的に権限を変更：

```bash
sudo chmod 666 /dev/ttyUSB0
```

**恒久的な解決（推奨）**: ホスト側でudevルールを設定

```bash
# /etc/udev/rules.d/99-usb-serial.rules を作成
sudo bash -c 'echo "KERNEL==\"ttyUSB*\", MODE=\"0666\"" > /etc/udev/rules.d/99-usb-serial.rules'
sudo bash -c 'echo "KERNEL==\"ttyACM*\", MODE=\"0666\"" >> /etc/udev/rules.d/99-usb-serial.rules'

# ルールを適用
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 4.4. セットアップ関連の問題

セットアップ時の問題（コンテナビルド失敗、X11転送の問題など）については、[docs/setup-detailed.md](docs/setup-detailed.md#トラブルシューティング)を参照してください。


## 付録A: colcon成果物のクリーン方法

このプロジェクトでは、`build/`、`install/`、`log/`がDockerボリュームとしてマウントされています。

### A.1. ビルド成果物のクリーン

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/clean_colcon_artifacts.sh
```

### A.2. クリーン→再ビルド（1コマンド）

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/rebuild_colcon.sh
```
