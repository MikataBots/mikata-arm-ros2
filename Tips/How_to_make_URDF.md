# How to make URDF

URDFを作成し、MoveItで動作確認するまでの最小手順をまとめる。

## 目的

- CAD由来のメッシュからURDFを作る
- MoveIt Setup AssistantでMoveIt設定パッケージを作る
- RVizで表示・計画ができる状態まで確認する

## 事前準備

- Ubuntu
- ROS 2（利用するディストリビューションに合わせる。例: Humble / Jazzy）
- MoveIt 2
- `xacro`, `robot_state_publisher`, `rviz2`
- メッシュデータ（`.dae` など）

## 成果物の配置方針（一般例）

- `<robot_name>_description/`
  - `urdf/` : ロボット本体のURDF/Xacro
  - `meshes/` : メッシュ
- `<robot_name>_moveit/`
  - `config/` : SRDF、kinematics、joint limits、RViz設定
  - `launch/` : MoveIt用launch
- `<robot_name>_bringup/`
  - `config/` : `ros2_control`、controller設定
  - `launch/` : bringup一式

## 手順

1. 元メッシュを準備する

- リンクごとにメッシュを分割し、原点と向きを確認する
- ファイル名はリンク名と対応させる（例: `Link1.dae`）

2. URDF KitchenでURDF構造を作る

- [URDF_kitchen](https://github.com/Ninagawa123/URDF_kitchen) を利用
- `StlSourcer` で各パーツの中心点・座標軸を調整
- `PartsEditor` でジョイント情報を設定しXML出力
- `Assembler` で全体を組み立ててURDF化
- 参考: [Qiita記事](https://qiita.com/Ninagawa123/items/c4643ca92e57c3a45efb)

3. `description` パッケージに反映する

- 生成URDFをXacro化して `urdf/` に配置
- メッシュ参照を `package://<robot_name>_description/meshes/...` に揃える
- 必要に応じて `collision` と `inertial` を補完する

4. MoveIt Setup Assistantで設定を生成する

- `ros2 launch moveit_setup_assistant setup_assistant.launch.py`
- URDF/Xacroを読み込み、以下を設定
  - planning groups（例: アームとグリッパーを分離）
  - end effector
  - virtual joint
  - self-collision matrix
- `<robot_name>_moveit` を生成または更新

5. `ros2_control` とbringupを整備する

- `<robot_name>_bringup/config/<robot_name>.ros2_control.xacro`
- `<robot_name>_bringup/config/ros2_controllers.yaml`
- `<robot_name>_bringup/config/initial_positions.yaml`（シミュレーション時）
- bringup launchから `robot_state_publisher` / `ros2_control_node` / controllers / MoveIt / RViz を起動する

## 動作確認

1. ビルド

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select <robot_name>_description <robot_name>_moveit <robot_name>_bringup
source install/setup.bash
```

2. 起動

```bash
ros2 launch <robot_name>_bringup bringup.launch.py
```

3. 確認ポイント

- RVizでロボットモデルが表示される
- `move_group` が落ちない
- PlanningグループでPlanが通る

## よくあるハマりどころ

- `joint_limits.yaml` の型不一致
  - `max_velocity`, `max_acceleration` は float で書く（例: `7.0`）
- グリッパーを1チェーンとして扱えない設定
  - planning groupやkinematics設定を見直す
- `collision`/`inertial` が不足し、RVizやプランニングで警告が多発

## 参考

- [URDF_kitchen](https://github.com/Ninagawa123/URDF_kitchen)
- [URDF Kitchen解説(Qiita)](https://qiita.com/Ninagawa123/items/c4643ca92e57c3a45efb)
- [MoveIt Setup Assistant参考1](https://note.com/npaka/n/n09d8693bbb04)
- [MoveIt Setup Assistant参考2](https://zenn.dev/nutechr/articles/d603fa30251ce3)
