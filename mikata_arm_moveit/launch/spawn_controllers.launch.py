from launch import LaunchDescription
from launch_ros.actions import Node

from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder(
        "mikata_arm", package_name="mikata_arm_moveit"
    ).to_moveit_configs()

    controller_names = moveit_config.trajectory_execution.get(
        "moveit_simple_controller_manager", {}
    ).get("controller_names", [])

    # `ros2_control_node` が立ち上がる前に spawner が service call を始めると
    # `list_controllers` が timeout して落ちることがあるため、待ち時間を長めに取る。
    spawner_common_args = [
        "-c",
        "/controller_manager",
        "--controller-manager-timeout",
        "60",
        "--service-call-timeout",
        "30",
    ]

    nodes = []
    for controller in controller_names + ["joint_state_broadcaster"]:
        nodes.append(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[controller, *spawner_common_args],
                output="screen",
            )
        )

    return LaunchDescription(nodes)
