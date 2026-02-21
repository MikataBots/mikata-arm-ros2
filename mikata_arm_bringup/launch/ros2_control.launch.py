from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation time",
        ),
        DeclareLaunchArgument(
            "initial_positions_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("mikata_arm_bringup"), "config", "initial_positions.yaml"]
            ),
            description="Path to initial positions yaml",
        ),
    ]

    use_sim_time = LaunchConfiguration("use_sim_time")
    initial_positions_file = LaunchConfiguration("initial_positions_file")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("mikata_arm_bringup"), "config", "mikata_arm.system.urdf.xacro"]
            ),
            " ",
            "initial_positions_file:=",
            initial_positions_file,
        ]
    )
    robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}

    controller_config = PathJoinSubstitution(
        [FindPackageShare("mikata_arm_bringup"), "config", "ros2_controllers.yaml"]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controller_config, {"use_sim_time": use_sim_time}],
        output="screen",
    )

    return LaunchDescription(declared_arguments + [control_node])
