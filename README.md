# mikata-arm-ros2
[![Build](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/MikataBots/mikata-arm-ros2/actions/workflows/build.yml)

MikataArmロボット用のROS 2パッケージ（MoveIt2対応）

## 開発環境

このプロジェクトはVS Code Dev Containersを使用して開発します。

## 前提条件

- Docker
- VS Code
- Dev Containers拡張機能

## 1.セットアップ

1. このリポジトリをクローン
   ```bash
   git clone <repository-url>
   cd mikata-arm-ros2
   ```

2. VS Codeで開く
   ```bash
   code .
   ```

3. VS Codeで `Dev Containers: Reopen in Container` を実行

## 2.MoveIt2の動作確認

devcontainerが正しく設定され、MoveIt2とGUI表示が動作することを確認します。

### Pandaロボットのデモを起動

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

## MikataArmのデモの動作確認

このリポジトリの3分割構成（`mikata_arm_description` / `mikata_arm_moveit` / `mikata_arm_bringup`）を使って、MikataArmのRVizデモを起動します。

1) （未ビルドの場合）ワークスペースをビルド

```bash
bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/scripts/rebuild_colcon.sh
```

2) overlay を反映

```bash
source /home/ros/ws_mikata_arm/install/setup.bash
```

3) デモ起動

```bash
ros2 launch mikata_arm_bringup bringup.launch.py
```

#### トラブルシュート（ロボットが表示されないとき）

- RVizで「ロボットが出ない」場合、まず `move_group` が落ちていないか確認してください。
   - 目安: 起動ログに `process has died`（`move_group`）が出ていないこと
   - RViz側で `robot_description_semantic` が見つからない（SRDFが読めない）系のエラーが出る場合、`move_group` 側の起動失敗が原因のことが多いです。
- `InvalidParameterTypeException` で `move_group` が落ちる場合、YAMLの数値型（int/float）が原因になりえます。
   - 例: `mikata_arm_moveit/config/joint_limits.yaml` の `max_velocity` / `max_acceleration` は `7` ではなく `7.0`、`0` ではなく `0.0` のように **浮動小数表記**に統一してください（MoveItが `double` として取得するため）。


## colcon成果物（build/install/log）のクリーン

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

### ボリューム自体を削除して完全リセット（ホスト側）

ホスト側で、リポジトリ直下から以下を実行します（`down -v` なのでボリュームが消えます）：

```bash
bash docker/reset_colcon_volumes.sh
```

その後、再度コンテナを起動してください。

