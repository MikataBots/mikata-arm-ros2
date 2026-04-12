FROM moveit/moveit2:jazzy-release

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ARG USERNAME=ubuntu
ENV USERNAME=${USERNAME}
ENV USER_HOME=/home/${USERNAME}
ENV WS_DIR=${USER_HOME}/ws_mikata_arm

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
    sudo \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

# 既存の ubuntu ユーザーを devcontainer の実行ユーザーとして利用する
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && usermod -aG dialout $USERNAME

# 依存リポジトリ & rosdep の導入をイメージビルド時に実行
# - setup.bash 内部の相対パス計算を崩さないため、実ワークスペース配下に配置する
RUN mkdir -p ${WS_DIR}/src/mikata-arm-ros2 ${WS_DIR}/src
COPY setup.bash build_depends.repos ${WS_DIR}/src/mikata-arm-ros2/

# rosdep は初回のみ init が必要な場合がある
RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then rosdep init; fi \
    && rosdep update \
    && bash ${WS_DIR}/src/mikata-arm-ros2/setup.bash \
    && chown -R ${USERNAME}:${USERNAME} ${WS_DIR}

# ROS 2の環境設定を.bashrcに追加
USER $USERNAME
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# CycloneDDS を既定のミドルウェアに設定
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
RUN echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc

# ROS2 CLI / colcon のTAB補完 (argcomplete)
RUN echo 'eval "$(register-python-argcomplete ros2)"' >> ~/.bashrc \
    && echo 'eval "$(register-python-argcomplete colcon)"' >> ~/.bashrc

# ワークスペースディレクトリを作成
RUN mkdir -p ${WS_DIR}

# 起動時にワークスペースをビルドしてからコマンドへ移る
COPY docker/image/entrypoint.sh /usr/local/bin/mikata_entrypoint.sh
RUN sudo chmod +x /usr/local/bin/mikata_entrypoint.sh

# デフォルトのシェルを設定
ENV SHELL=/bin/bash
RUN sudo chsh -s /bin/bash $USERNAME


# デフォルトのシェルをbashに設定
ENTRYPOINT ["/usr/local/bin/mikata_entrypoint.sh"]
CMD ["/bin/bash"]
