# mikata-arm-ros2

MikataArmロボット用のROS 2パッケージ（MoveIt2対応）

## 開発環境

このプロジェクトはVS Code Dev Containersを使用して開発します。

### 前提条件

- Docker
- VS Code
- Dev Containers拡張機能

### セットアップ

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

## MoveIt2の動作確認

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


