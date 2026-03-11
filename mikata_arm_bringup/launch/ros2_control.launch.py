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
            "use_fake_hardware",
            default_value="false",
            description="Use fake hardware (simulation mode)",
        ),
        DeclareLaunchArgument(
            "initial_positions_file",
            default_value=PathJoinSubstitution(
                [FindPackageShare("mikata_arm_description"), "config", "initial_positions.yaml"]
            ),
            description="Path to initial positions yaml",
        ),
    ]

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    initial_positions_file = LaunchConfiguration("initial_positions_file")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("mikata_arm_description"), "urdf", "mikata_arm.urdf.xacro"]
            ),
            " ",
            "use_ros2_control:=true",
            " ",
            "use_fake_hardware:=",
            use_fake_hardware,
            " ",
            "initial_positions_file:=",
            initial_positions_file,
        ]
    )
    robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}

    controller_config = PathJoinSubstitution(
        [FindPackageShare("mikata_arm_description"), "config", "ros2_controllers.yaml"]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, controller_config, {"use_sim_time": use_sim_time}],
        output="screen",
    )

    return LaunchDescription(declared_arguments + [control_node])
