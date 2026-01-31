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
