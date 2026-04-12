#!/bin/bash
# Bashヒストリーによく使うコマンドを追加するスクリプト

HISTORY_FILE=~/.bash_history
HISTORY_VOLUME=~/.bash_history_volume
WS_DIR="${WS_DIR:-$HOME/ws_mikata_arm}"
REPO_DIR="$WS_DIR/src/mikata-arm-ros2"

# ボリュームマウントされたヒストリーディレクトリが存在する場合
if [ -d "$HISTORY_VOLUME" ]; then
    PERSISTENT_HISTORY="$HISTORY_VOLUME/bash_history"

    # 永続化されたヒストリーがある場合は読み込む
    if [ -f "$PERSISTENT_HISTORY" ]; then
        cp "$PERSISTENT_HISTORY" "$HISTORY_FILE"
    else
        # 初回の場合は空ファイルを作成
        touch "$PERSISTENT_HISTORY"
        touch "$HISTORY_FILE"
    fi
else
    # ボリュームがない場合は通常のヒストリーファイルを使用
    touch "$HISTORY_FILE"
fi

# よく使うコマンドのリスト
commands=(
    "source $WS_DIR/install/setup.bash"
    "rm -rf build/* install/* log/*"
    "bash $REPO_DIR/scripts/rebuild_colcon.sh"
    "ros2 launch mikata_arm_bringup bringup.launch.py"
    "ros2 launch moveit_resources_panda_moveit_config demo.launch.py"
    "ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=true"
    "ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false"
    "ros2 launch mikata_arm_bringup bringup.launch.py use_fake_hardware:=false usb_port:=/dev/ttyACM0"
    "lsusb"
    "ls -l /dev/ttyUSB* /dev/ttyACM*"
    "colcon build --symlink-install"
    "colcon test"
    "ros2 topic list"
    "ros2 node list"
)

# コマンドをヒストリーに追加（既に存在する場合はスキップ）
for cmd in "${commands[@]}"; do
    if ! grep -Fxq "$cmd" "$HISTORY_FILE"; then
        echo "$cmd" >> "$HISTORY_FILE"
    fi
done

# 永続化ボリュームが存在する場合、ヒストリーを保存
if [ -d "$HISTORY_VOLUME" ]; then
    cp "$HISTORY_FILE" "$PERSISTENT_HISTORY"

    # .bashrcにヒストリー自動保存の設定を追加（初回のみ）
    BASHRC=~/.bashrc
    if ! grep -q "PROMPT_COMMAND.*history -a" "$BASHRC"; then
        cat >> "$BASHRC" << 'EOF'

# Bash history persistence for dev container
if [ -d ~/.bash_history_volume ]; then
    export HISTFILE=~/.bash_history
    export HISTSIZE=10000
    export HISTFILESIZE=20000
    # Save history after every command
    export PROMPT_COMMAND="history -a; if [ -f ~/.bash_history_volume/bash_history ]; then cp ~/.bash_history ~/.bash_history_volume/bash_history; fi; $PROMPT_COMMAND"
fi
EOF
    fi
fi

echo "✓ Bash history setup complete with common commands"
