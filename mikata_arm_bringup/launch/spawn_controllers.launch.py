from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    spawner_common_args = [
        "-c",
        "/controller_manager",
        "--controller-manager-timeout",
        "60",
        "--service-call-timeout",
        "30",
    ]

    controller_names = ["joint_state_broadcaster", "mikata_arm_controller", "hand_controller"]

    spawners = [
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=[controller, *spawner_common_args],
            output="screen",
        )
        for controller in controller_names
    ]

    # Let ros2_control_node boot first to reduce transient spawner failures.
    delayed_spawners = [TimerAction(period=2.0, actions=[node]) for node in spawners]
    return LaunchDescription(delayed_spawners)
