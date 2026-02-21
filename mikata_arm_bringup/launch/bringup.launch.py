from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation time",
        ),
        DeclareLaunchArgument(
            "use_rviz",
            default_value="true",
            description="Launch RViz",
        ),
    ]

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_rviz = LaunchConfiguration("use_rviz")

    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("mikata_arm_bringup"), "launch", "rsp.launch.py"])
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    ros2_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("mikata_arm_bringup"), "launch", "ros2_control.launch.py"]
            )
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    spawn_controllers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("mikata_arm_bringup"), "launch", "spawn_controllers.launch.py"]
            )
        )
    )

    move_group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("mikata_arm_moveit"), "launch", "move_group.launch.py"])
        )
    )

    static_tf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("mikata_arm_moveit"), "launch", "static_virtual_joint_tfs.launch.py"]
            )
        )
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare("mikata_arm_moveit"), "launch", "moveit_rviz.launch.py"])
        ),
        condition=IfCondition(use_rviz),
    )

    delayed_moveit = TimerAction(period=3.0, actions=[move_group_launch, static_tf_launch])
    delayed_rviz = TimerAction(period=4.0, actions=[rviz_launch])

    return LaunchDescription(
        declared_arguments
        + [rsp_launch, ros2_control_launch, spawn_controllers_launch, delayed_moveit, delayed_rviz]
    )
