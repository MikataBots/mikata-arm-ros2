# セットアップ詳細ガイド

このドキュメントでは、Dev ContainersとVS Codeを使った開発環境のセットアップ方法を詳しく説明します。

## 前提条件の詳細

### Docker

**必須バージョン**: Docker 20.10以降

**インストール方法**:

- **Ubuntu/Debian**:
  ```bash
  # 公式リポジトリからインストール
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh

  # 現在のユーザーをdockerグループに追加
  sudo usermod -aG docker $USER

  # ログアウト・ログインして反映
  ```
  詳細: [公式ガイド](https://docs.docker.com/engine/install/ubuntu/)


**インストール確認**:
```bash
docker --version
# 出力例: Docker version 20.10.x, build xxxxx

docker ps
# エラーが出なければOK
```

### Visual Studio Code

**必須バージョン**: VS Code 1.70以降

**インストール方法**: [公式サイト](https://code.visualstudio.com/)からインストーラーをダウンロード

**インストール確認**:
```bash
code --version
```

## Dev Containers拡張機能のインストール

VS CodeでDev Containersを使用するには、専用の拡張機能が必要です。

### インストール手順

1. VS Codeを起動
2. 左サイドバーの**拡張機能アイコン**（四角が4つ並んだアイコン、またはCtrl+Shift+X）をクリック
3. 検索ボックスに `Dev Containers` と入力
4. **Dev Containers**（発行元: Microsoft）を選択
5. **インストール**ボタンをクリック
6. インストール完了後、VS Codeの再起動は不要

## Dev Containerで開く方法

Dev Containerを起動する方法は複数あります。

### 方法1: 通知から起動（推奨・最も簡単）

VS Codeでプロジェクトを開くと、`.devcontainer/devcontainer.json` が検出され、右下に以下の通知が表示されます：

```
Folder contains a Dev Container configuration file.
Reopen folder to develop in a container.
```

通知内の **Reopen in Container** ボタンをクリックすればOKです。

> **通知が表示されない場合**: 方法2または方法3を使用してください。

### 方法2: コマンドパレットから起動

1. `F1` キーまたは `Ctrl+Shift+P`（macOSは `Cmd+Shift+P`）を押してコマンドパレットを開く
2. `Dev Containers: Reopen in Container` と入力
3. 候補から選択してEnter

### 方法3: 左下の緑色アイコンから起動

1. VS Code左下の緑色の **><** アイコンをクリック
2. メニューから **Reopen in Container** を選択

## コンテナのビルドプロセス

### 初回起動時

**所要時間**: 5〜10分程度（ネットワーク速度に依存）

**処理内容**:
1. Dockerイメージのビルド（ROS 2 Humble + MoveIt2環境）
2. 依存パッケージのインストール
3. コンテナの起動
4. VS Codeサーバーのインストール

**進捗確認**:

VS Code下部のステータスバーに進捗が表示されます：

```
Dev Containers: Building... (Step 12/25)
```

ビルドログを確認したい場合：
- `表示` → `出力` → ドロップダウンから `Dev Containers` を選択

### 起動完了の確認

ビルドが完了すると、以下のように変わります：

**ステータスバー表示**:
```
Dev Container: MikataArm MoveIt2 Humble Dev
```

**左下の緑アイコン**: コンテナ名が表示される

**ターミナル**: コンテナ内のbashシェルが開く

### 2回目以降の起動

**所要時間**: 数秒〜1分程度

既存のイメージを使用するため、ビルドプロセスはスキップされます。

## トラブルシューティング

### コンテナのビルドが失敗する

**エラー例**:
```
ERROR: failed to solve: process "/bin/sh -c ..." did not complete successfully
```

**原因と対処法**:

1. **Dockerが起動していない**
   ```bash
   # Dockerの状態確認
   docker ps

   # Docker Desktopを再起動（Windows/macOS）
   # またはDockerデーモンを再起動（Linux）
   sudo systemctl restart docker
   ```

2. **ディスク容量不足**
   ```bash
   # Dockerのディスク使用量を確認
   docker system df

   # 不要なイメージ・コンテナを削除
   docker system prune -a
   ```

   最低10GB以上の空き容量が必要です。

3. **ネットワークエラー**
   - インターネット接続を確認
   - プロキシ設定が必要な環境では、Dockerのプロキシ設定を行う

4. **VS Codeの再起動**
   VS Codeを完全に終了してから再度 `Reopen in Container` を実行

### X11転送（GUI表示）が動作しない

**症状**: RVizやGazeboなどのGUIアプリケーションが起動しない、または画面が真っ黒

**対処法（Linux）**:

```bash
# X11サーバーへのアクセスを許可
xhost +local:docker

# 環境変数を確認
echo $DISPLAY
# :0 または :1 などが表示されるはずtest
```

この設定は再起動後に無効になるため、`~/.bashrc` に追加すると便利です：
```bash
echo "xhost +local:docker > /dev/null 2>&1" >> ~/.bashrc
```

**対処法（Windows）**:

1. **VcXsrv**（X11サーバー）をインストール
   - [VcXsrv公式サイト](https://sourceforge.net/projects/vcxsrv/)からダウンロード

2. XLaunchを起動し、以下の設定で起動：
   - Display number: 0
   - Start no client: チェック
   - **Disable access control**: チェック（重要）

3. Windowsファイアウォールの許可が必要な場合があります

**対処法（macOS）**:

1. **XQuartz**をインストール
   ```bash
   brew install --cask xquartz
   ```

2. XQuartzを起動し、環境設定で以下を確認：
   - `セキュリティ` タブ → `ネットワーククライアントからの接続を許可` にチェック

3. XQuartzを再起動

4. ターミナルで以下を実行：
   ```bash
   xhost + $(hostname)
   ```

### コンテナが起動しない・途中で止まる

**対処法**:

1. **Docker Desktopの再起動**（Windows/macOS）
   Docker Desktopを完全に終了してから再起動

2. **詳細なエラーログを確認**
   - VS Codeで `表示` → `出力`
   - ドロップダウンから `Dev Containers` を選択
   - エラーメッセージをコピーして検索

3. **既存のコンテナを削除して再ビルド**
   ```bash
   # コンテナ一覧を確認
   docker ps -a

   # mikata-arm-ros2-devコンテナを停止・削除
   docker stop mikata-arm-ros2-dev
   docker rm mikata-arm-ros2-dev

   # イメージも削除する場合（完全なクリーンビルド）
   docker images | grep mikata-arm
   docker rmi <IMAGE_ID>
   ```

   その後、VS Codeで `Dev Containers: Rebuild Container` を実行

4. **Docker Desktopのリソース設定を確認**（Windows/macOS）
   - Docker Desktop → 設定 → Resources
   - CPU: 4コア以上推奨
   - メモリ: 8GB以上推奨
   - ディスク: 20GB以上推奨

### Dev Containers拡張機能がインストールできない

**対処法**:

1. VS Codeを最新版に更新
   - `ヘルプ` → `更新の確認`

2. VS Codeの拡張機能キャッシュをクリア
   ```bash
   # VS Codeを終了してから実行
   rm -rf ~/.vscode/extensions
   ```

   その後、VS Codeを起動して拡張機能を再インストール

## セットアップの確認

環境が正しくセットアップされたことを確認するため、サンプルロボット（Panda）でMoveIt2を試します。

### Pandaロボットのデモを起動

コンテナ内のターミナルで以下を実行：

```bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

### 確認ポイント

- ✅ RVizが起動してPandaロボットが表示される
- ✅ MotionPlanningプラグインでインタラクティブマーカーをドラッグしてゴール位置を設定できる
- ✅ **Plan**ボタンで経路計画ができる
- ✅ **Execute**ボタンで計画した経路をシミュレーション実行できる

これらが確認できれば、MoveIt2とGUI表示が正しく動作しています。

**次のステップ**: 環境が正しく動作することを確認したら、[README.md](../README.md)に戻ってMikataArmのシミュレーションを試してください。

## 参考リンク

- [Dev Containers公式ドキュメント](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [ROS 2 Humble公式ドキュメント](https://docs.ros.org/en/humble/)
