FROM moveit/moveit2:humble-release

ARG ROS_DISTRO=humble
ENV ROS_DISTRO=${ROS_DISTRO}

# 基本的な開発ツールのインストール
RUN apt-get update && apt-get install -y \
    bash-completion \
    git \
    vim \
    wget \
    curl \
    gdb \
    python3-colcon-common-extensions \
    python3-argcomplete \
    python3-vcstool \
    python3-rosdep \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
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

# 依存リポジトリ & rosdep の導入をイメージビルド時に実行
# - setup.bash 内部の相対パス計算を崩さないため、実ワークスペース配下に配置する
RUN mkdir -p /home/ros/ws_mikata_arm/src/mikata-arm-ros2 /home/ros/ws_mikata_arm/src
COPY setup.bash build_depends.repos /home/ros/ws_mikata_arm/src/mikata-arm-ros2/

# rosdep は初回のみ init が必要な場合がある
RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then rosdep init; fi \
    && rosdep update \
    && bash /home/ros/ws_mikata_arm/src/mikata-arm-ros2/setup.bash \
    && chown -R ${USERNAME}:${USERNAME} /home/ros/ws_mikata_arm

# ROS 2の環境設定を.bashrcに追加
USER $USERNAME
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# CycloneDDS を既定のミドルウェアに設定
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
RUN echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc

# ROS2 CLI / colcon のTAB補完 (argcomplete)
RUN echo 'eval "$(register-python-argcomplete3 ros2)"' >> ~/.bashrc \
    && echo 'eval "$(register-python-argcomplete3 colcon)"' >> ~/.bashrc

# ワークスペースディレクトリを作成
RUN mkdir -p /home/ros/ws_mikata_arm

# 起動時にワークスペースをビルドしてからコマンドへ移る
COPY docker/image/entrypoint.sh /usr/local/bin/mikata_entrypoint.sh
RUN sudo chmod +x /usr/local/bin/mikata_entrypoint.sh

# デフォルトのシェルを設定
ENV SHELL=/bin/bash
RUN sudo chsh -s /bin/bash $USERNAME


# デフォルトのシェルをbashに設定
ENTRYPOINT ["/usr/local/bin/mikata_entrypoint.sh"]
CMD ["/bin/bash"]
