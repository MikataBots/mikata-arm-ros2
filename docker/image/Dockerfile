FROM moveit/moveit2:jazzy-release

ARG ROS_DISTRO=jazzy
ENV ROS_DISTRO=${ROS_DISTRO}
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=1000
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

# ベースイメージにユーザーがなければ作成し、あればそのまま利用する
RUN set -eux; \
    if ! id -u "$USERNAME" >/dev/null 2>&1; then \
      if getent group "$USER_GID" >/dev/null 2>&1; then \
        USER_GROUP="$(getent group "$USER_GID" | cut -d: -f1)"; \
      else \
        groupadd --gid "$USER_GID" "$USERNAME"; \
        USER_GROUP="$USERNAME"; \
      fi; \
      useradd --uid "$USER_UID" --gid "$USER_GROUP" -m "$USERNAME"; \
    fi; \
    mkdir -p /etc/sudoers.d; \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME; \
    chmod 0440 /etc/sudoers.d/$USERNAME; \
    usermod -aG dialout "$USERNAME"; \
    mkdir -p "$WS_DIR"; \
    chown -R "$USERNAME":"$(id -gn "$USERNAME")" "$USER_HOME"

# 依存リポジトリ & rosdep の導入をイメージビルド時に実行
# - setup.bash 内部の相対パス計算を崩さないため、実ワークスペース配下に配置する
RUN mkdir -p ${WS_DIR}/src/mikata-arm-ros2 ${WS_DIR}/src
COPY setup.bash build_depends.repos ${WS_DIR}/src/mikata-arm-ros2/

# rosdep は初回のみ init が必要な場合がある
RUN if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then rosdep init; fi \
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
