# mikata-arm-ros2
[![Build](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml)

MikataArmロボット用のROS 2パッケージ（MoveIt2対応）

## 開発環境

このプロジェクトはVS Code Dev Containersを使用して開発します。

## 前提条件

- Docker
- VS Code
- Dev Containers拡張機能

## 1. セットアップ

1. このリポジトリをクローンする
   ```bash
   git clone <repository-url>
   cd mikata-arm-ros2
   ```

2. VS Codeで開く
   ```bash
   code .
   ```

3. VS Codeで `Dev Containers: Reopen in Container` を実行

## 2. MoveIt2の動作確認

devcontainerが正しく設定され、MoveIt2とGUI表示が動作することを確認します。

### 2.1. Pandaロボットのデモを起動

コンテナ内のターミナルで以下のコマンドを実行：

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

### 確認ポイント

- ✅ RVizが起動してPandaロボットが表示される
- ✅ MotionPlanningプラグインでゴール位置を設定できる（インタラクティブマーカーをドラッグ）
- ✅ 「Plan」ボタンで経路計画ができる
- ✅ 「Execute」ボタンで計画した経路を実行できる

これらが確認できれば、MoveIt2とX11転送（GUI表示）が正しく動作しています。

## 3. MikataArmのモデルをrviz上で表示させて動作確認する

MikataArmのデモを起動する方法を示します。

1) （未ビルドの場合）ワークスペースをビルド

```bash
colcon build --symlink-install
```

2) install/setup.bashの実行

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

3) デモ起動

MikataArmに接続せず、動作確認を行います。以下のコマンドを実行してください。

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=true
```


### トラブルシュート（ロボットが表示されないとき）

- RVizで「ロボットが表示されない」場合、まず `move_group` が落ちていないか確認してください。
   - 目安: 起動ログに `process has died`（`move_group`）が出ていないこと
   - RViz側で `robot_description_semantic` が見つからない（SRDFが読めない）系のエラーが出る場合、`move_group` 側の起動失敗が原因のことが多いです。
- `InvalidParameterTypeException` で `move_group` が落ちる場合、YAMLの数値型（int/float）が原因になりえます。
   - 例: `mikata_arm_moveit/config/joint_limits.yaml` の `max_velocity` / `max_acceleration` は `7` ではなく `7.0`、`0` ではなく `0.0` のように **浮動小数表記**に統一してください（MoveItが `double` として取得するため）。


## 4. MikataArmに接続してデモを実行する

### 4.1. デバイスのパーミッション設定

実機のMikataArmに接続するには、USBシリアルデバイスへのアクセス権限が必要です。

> **注意**: このプロジェクトのDocker設定では `privileged: true` が有効なため、USBデバイス（`/dev/ttyUSB0` など）はコンテナから自動的に見えています。また、Dockerイメージのビルド時に `ros` ユーザーを `dialout` グループに追加しているため、**通常は追加の設定は不要**です。

#### コンテナを最新バージョンにリビルド

既存のコンテナを使用している場合は、最新のDockerイメージでリビルドしてください：

VS Codeで `Dev Containers: Rebuild Container` を実行

#### パーミッションの確認

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

#### トラブルシューティング: デバイスが見つからない場合

`ls -l /dev/ttyUSB* /dev/ttyACM*` を実行しても該当デバイスが見つからない場合、以下の手順で調査してください：

1. **USBデバイスの接続確認**

```bash
# 接続されているUSBデバイスを確認
lsusb
```

MikataArmが接続されている場合、以下のような出力が表示されます：
- FTDI製のUSB-シリアル変換チップを使用している場合: `Future Technology Devices International`
- その他のシリアル変換チップの場合: チップメーカー名（例: `Prolific`, `Silicon Labs`）

2. **デバイスファイルの確認**

```bash
# すべてのシリアルデバイスを確認
ls -l /dev/tty* | grep -E "(USB|ACM)"

# または、dmesgでカーネルログを確認
dmesg | grep -i "tty"
```

MikataArmを抜き差しして、どのデバイス名が追加/削除されるか確認してください。

3. **デバイス名がttyUSB0以外の場合**

デバイスが `/dev/ttyACM0` や `/dev/ttyUSB1` など、`/dev/ttyUSB0` 以外の名前の場合、起動時にパラメータで指定できます：

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0
```

または、設定ファイルを直接編集する場合は、[mikata_arm_description/urdf/mikata_arm.ros2_control.xacro](mikata_arm_description/urdf/mikata_arm.ros2_control.xacro#L9) の `usb_port` パラメータを変更してください。

#### トラブルシューティング: dialoutグループに所属していない場合

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

#### トラブルシューティング: Permission deniedエラーが出る場合

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

### 4.2. MikataArmに接続してデモの動作を確認する

1) install/setup.bashの実行

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

2) MikataArmに接続して動作確認を行う場合は以下のコマンドを使用してください。

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false
```

デバイスが `/dev/ttyUSB0` 以外の場合は、`usb_port` パラメータを指定してください：

```bash
ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0
```


## colcon成果物（build/install/log）のクリーン方法

このリポジトリのコンテナ設定では、起動高速化のため `build/ install/ log/` はDockerの名前付きボリュームとして `/home/ros/ws_mikata_arm/{build,install,log}` にマウントされています。
そのため、コンテナ内で `rm -rf build/ install/ log/` を実行すると「Device or resource busy（マウントポイントのため削除不可）」になることがあります。

### コンテナ内で「中身だけ」消す（推奨）

コンテナ内で以下を実行します：

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/clean_colcon_artifacts.sh
```

### 1コマンドで「クリーン→再ビルド」

コンテナ内で以下を実行します：

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/rebuild_colcon.sh
```



