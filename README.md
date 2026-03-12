# mikata-arm-ros2
[![Build](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml)

MikataArmロボット用のROS 2パッケージ（MoveIt2対応）

## 開発環境

このプロジェクトはVS Code Dev Containersを使用して開発しています。

## 前提条件

以下のソフトウェアがインストールされている必要があります：

### Docker

- **バージョン**: Docker 20.10以降推奨
- **インストール方法**:
  - **Ubuntu/Debian**: [公式ガイド](https://docs.docker.com/engine/install/ubuntu/)
  - **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

インストール後、以下のコマンドでバージョンを確認してください：

```bash
docker --version
# 出力例: Docker version 20.10.x, build xxxxx
```

### Visual Studio Code

- **バージョン**: VS Code 1.70以降推奨
- **インストール方法**: [公式サイト](https://code.visualstudio.com/)からダウンロード

### Dev Containers拡張機能

VS Codeの拡張機能です。セットアップ手順の中でインストール方法を説明します。

## 1. セットアップ

### 1.1. リポジトリのクローン

ターミナルで以下のコマンドを実行してリポジトリをクローンします：

```bash
git clone https://github.com/MikataBots/mikata-arm-ros2.git
cd mikata-arm-ros2
```

### 1.2. VS Codeで開く

```bash
# ~/ws_mikata_arm/src/mikata-arm-ros2 において
code .
```

VS Codeが起動します。

### 1.3. Dev Containers拡張機能のインストール（初回のみ）

Dev Containers拡張機能がインストールされていない場合は、以下の手順でインストールしてください：

1. VS Codeの左サイドバーで **拡張機能アイコン**（四角が4つ並んだアイコン）をクリック
2. 検索ボックスに `Dev Containers` と入力
3. **Dev Containers**（Microsoft製）を選択して **インストール** をクリック

### 1.4. Dev Containerで開く

以下のいずれかの方法でコンテナを起動します：

**方法1: 通知から起動（推奨）**

VS Codeがプロジェクトを開くと、右下に以下のような通知が表示されます：

```
Folder contains a Dev Container configuration file. Reopen folder to develop in a container.
```

この通知の **Reopen in Container** ボタンをクリックしてください。

**方法2: コマンドパレットから起動**

1. `F1` キーまたは `Ctrl+Shift+P`（macOSは `Cmd+Shift+P`）でコマンドパレットを開く
2. `Dev Containers: Reopen in Container` と入力して選択

**方法3: 左下の緑色アイコンから起動**

1. VS Code左下の `><` アイコンをクリック
2. メニューから **Reopen in Container** を選択

### 1.5. コンテナのビルドと起動を待つ

**初回起動時**は、Dockerイメージのビルドに **5〜10分程度** かかります。VS Code下部のステータスバーに進捗が表示されます：

```
Dev Containers: Building... (Step X/Y)
```

ビルドが完了すると、以下のような表示に変わります：

```
Dev Container: MikataArm MoveIt2 Humble Dev
```

VS Code左下の緑色アイコンが `Dev Container: MikataArm MoveIt2 Humble Dev` と表示されていれば、コンテナ内で開発できる状態です。

**2回目以降**は、既存のイメージを使用するため **数秒〜1分程度** で起動します。

### 1.6. 起動確認

コンテナが正しく起動したか確認します。VS Code内のターミナルを開いて（`` Ctrl+` `` または `表示` → `ターミナル`）、以下を実行：

```bash
# ROS 2のバージョンを確認
ros2 --version

# 出力例: ros2 cli version: 0.18.x
```

ROS 2のバージョンが表示されれば、セットアップ完了です。

### 1.7. セットアップのトラブルシューティング

#### コンテナのビルドが失敗する

**エラー例**: `ERROR: failed to solve: process "/bin/sh -c ..."`

**対処法**:
1. Dockerが正しく起動しているか確認：
   ```bash
   docker ps
   ```
2. Dockerのディスク容量を確認（最低10GB以上の空き容量が必要）
3. VS Codeを再起動してから再度 `Reopen in Container` を実行

#### X11転送（GUI表示）が動作しない

**症状**: RVizなどのGUIアプリケーションが起動しない、または画面が表示されない

**対処法**:

**Linux**:
```bash
xhost +local:docker
```

**Windows/macOS（Docker Desktop使用時）**:
- Docker Desktopの設定で、ファイル共有やリソース割り当てを確認
- VcXsrvやXQuartzなどのX11サーバーが起動しているか確認

#### コンテナが起動しない・途中で止まる

**対処法**:
1. Docker Desktopを再起動
2. VS Codeの出力パネルで詳細なエラーログを確認：
   - `表示` → `出力` → ドロップダウンから `Dev Containers` を選択
3. 既存のコンテナを削除して再度ビルド：
   ```bash
   docker ps -a  # コンテナ一覧を確認
   docker rm mikata-arm-ros2-dev  # 既存コンテナを削除
   ```
   その後、VS Codeで `Dev Containers: Rebuild Container` を実行

## 2. MoveIt2の動作確認

devcontainerが正しく設定され、MoveIt2とGUI表示が動作することを確認します。

### 2.1. Pandaロボットのデモを起動

コンテナ内のターミナルで以下のコマンドを実行：

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

### 2.2. 確認ポイント

- ✅ RVizが起動してPandaロボットが表示される
- ✅ MotionPlanningプラグインでゴール位置を設定できる（インタラクティブマーカーをドラッグ）
- ✅ 「Plan」ボタンで経路計画ができる
- ✅ 「Execute」ボタンで計画した経路を実行できる

これらが確認できれば、MoveIt2とX11転送（GUI表示）が正しく動作しています。

## 3. MikataArmのモデルをrviz上で表示させて動作確認する

シミュレーションモードでMikataArmの動作を確認します。

### 3.1. シミュレーションモードでのデモ起動

1) （未ビルドの場合）ワークスペースをビルド

ワークスペースのルートディレクトリに移動してからビルドします：

```bash
cd /home/ros/ws_mikata_arm
colcon build --symlink-install
```

2) install/setup.bashの実行

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

3) デモ起動

MikataArmに接続せず、シミュレーションモードで動作確認を行います。

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=true
```

### 3.2. トラブルシュート（ロボットが表示されないとき）

- RVizで「ロボットが表示されない」場合、まず `move_group` が落ちていないか確認してください。
   - 目安: 起動ログに `process has died`（`move_group`）が出ていないこと
   - RViz側で `robot_description_semantic` が見つからない（SRDFが読めない）系のエラーが出る場合、`move_group` 側の起動失敗が原因のことが多いです。
- `InvalidParameterTypeException` で `move_group` が落ちる場合、YAMLの数値型（int/float）が原因になりえます。
   - 例: `mikata_arm_moveit/config/joint_limits.yaml` の `max_velocity` / `max_acceleration` は `7` ではなく `7.0`、`0` ではなく `0.0` のように **浮動小数表記**に統一してください（MoveItが `double` として取得するため）。


## 4. MikataArmに接続してデモを実行する

実機のMikataArmに接続してデモを実行する手順を説明します。

> **前提**: 3章のシミュレーションモードでのビルドと動作確認が完了していることを確認してください。

### 4.1. デバイスのパーミッション設定

実機のMikataArmに接続するには、USBシリアルデバイスへのアクセス権限が必要です。

> **注意**: このプロジェクトのDocker設定では `privileged: true` が有効なため、USBデバイス（`/dev/ttyUSB0` など）はコンテナから自動的に見えています。また、Dockerイメージのビルド時に `ros` ユーザーを `dialout` グループに追加しているため、**通常は追加の設定は不要**です。

既存のコンテナを使用している場合は、最新のDockerイメージでリビルドしてください：

```
VS Codeで `Dev Containers: Rebuild Container` を実行
```

コンテナ内で以下を実行して、設定が正しいか確認：

```bash
# dialoutグループに所属しているか確認
groups
# 出力に "dialout" が含まれていればOK

# デバイスを確認
ls -l /dev/ttyUSB* /dev/ttyACM*
# 出力例: crw-rw---- 1 root dialout 188, 0 Mar 12 10:00 /dev/ttyUSB0
```

通常は `/dev/ttyUSB0` ですが、接続ポートによっては `/dev/ttyACM0` などと表示される場合もあります。

### 4.2. 実機への接続とデモ実行

1) install/setup.bashの実行

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

2) MikataArmに接続してデモを起動

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false
```

デバイスが `/dev/ttyUSB0` 以外の場合は、`usb_port` パラメータを指定してください：

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0
```


## 5. トラブルシューティング

実機接続時に問題が発生した場合の対処法を説明します。

### 5.1. USBデバイスが見つからない場合

`ls -l /dev/ttyUSB* /dev/ttyACM*` を実行しても該当デバイスが見つからない場合、以下の手順で調査してください。

#### 1. USBデバイスの接続確認

```bash
# 接続されているUSBデバイスを確認
lsusb
```

MikataArmが接続されている場合、以下のような出力が表示されます：
- FTDI製のUSB-シリアル変換チップを使用している場合: `Future Technology Devices International`
- その他のシリアル変換チップの場合: チップメーカー名（例: `Prolific`, `Silicon Labs`）

#### 2. デバイスファイルの確認

```bash
# すべてのシリアルデバイスを確認
ls -l /dev/tty* | grep -E "(USB|ACM)"

# または、dmesgでカーネルログを確認
dmesg | grep -i "tty"
```

MikataArmを抜き差しして、どのデバイス名が追加/削除されるか確認してください。

#### 3. デバイス名がttyUSB0以外の場合

デバイスが `/dev/ttyACM0` や `/dev/ttyUSB1` など、`/dev/ttyUSB0` 以外の名前の場合、起動時にパラメータで指定できます：

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0
```

または、設定ファイルを直接編集する場合は、[mikata_arm_description/urdf/mikata_arm.ros2_control.xacro](mikata_arm_description/urdf/mikata_arm.ros2_control.xacro#L9) の `usb_port` パラメータを変更してください。

### 5.2. dialoutグループの権限問題

古いコンテナを使用している場合や、何らかの理由で `dialout` グループに所属していない場合は、以下のコマンドを実行：

```bash
sudo usermod -aG dialout ros
```

その後、コンテナを再起動：

```bash
# ホスト側で実行
docker restart mikata-arm-ros2-dev
```

VS Codeで再接続してください。

### 5.3. Permission deniedエラー

`dialout` グループに所属しても「Permission denied」エラーが出る場合、デバイスのパーミッションを確認してください：

```bash
ls -l /dev/ttyUSB0
```

グループが `dialout` でない場合（例: `root`）、一時的に権限を変更：

```bash
sudo chmod 666 /dev/ttyUSB0
```

恒久的に解決するには、ホスト側でudevルールを設定（推奨）：

```bash
# ホスト側で /etc/udev/rules.d/99-usb-serial.rules を作成
sudo bash -c 'echo "KERNEL==\"ttyUSB*\", MODE=\"0666\"" > /etc/udev/rules.d/99-usb-serial.rules'
sudo bash -c 'echo "KERNEL==\"ttyACM*\", MODE=\"0666\"" >> /etc/udev/rules.d/99-usb-serial.rules'

# ルールを適用
sudo udevadm control --reload-rules
sudo udevadm trigger
```


## 6. colcon成果物のクリーン方法

このリポジトリのコンテナ設定では、起動高速化のため `build/ install/ log/` はDockerの名前付きボリュームとして `/home/ros/ws_mikata_arm/{build,install,log}` にマウントされています。そのため、コンテナ内で `rm -rf build/ install/ log/` を実行すると「Device or resource busy（マウントポイントのため削除不可）」になることがあります。

### 6.1. コンテナ内で「中身だけ」消す（推奨）

コンテナ内で以下を実行します：

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/clean_colcon_artifacts.sh
```

### 6.2. 1コマンドで「クリーン→再ビルド」

コンテナ内で以下を実行します：

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/rebuild_colcon.sh
```
