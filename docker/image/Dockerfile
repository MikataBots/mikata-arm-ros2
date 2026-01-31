FROM moveit/moveit2:humble-release

# 基本的な開発ツールのインストール
RUN apt-get update && apt-get install -y \
    bash-completion \
    git \
    vim \
    wget \
    curl \
    gdb \
    && rm -rf /var/lib/apt/lists/*

# 開発用ユーザー (ros) の作成
# セキュリティとファイルのパーミッション問題を避けるため、非rootユーザーを作成します
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ROS 2の環境設定を.bashrcに追加
USER $USERNAME
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# ワークスペースディレクトリを作成
RUN mkdir -p /home/ros/ws_mikata_arm

# デフォルトのシェルを設定
ENV SHELL=/bin/bash
RUN sudo chsh -s /bin/bash $USERNAME

# 自作ロボットに必要な追加パッケージがあればここに記述します
# RUN sudo apt-get update && sudo apt-get install -y ros-humble-xacro ...

# デフォルトのシェルをbashに設定
CMD ["/bin/bash"]