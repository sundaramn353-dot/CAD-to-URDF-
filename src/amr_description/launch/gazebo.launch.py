import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable

from launch_ros.actions import Node


def generate_launch_description():

    pkg_share = get_package_share_directory(
        'amr_description'
    )

    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.path.dirname(pkg_share)
     )
    

    urdf_file = os.path.join(
        pkg_share,
        'urdf',
        'amr.urdf'
    )

    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description
            }
        ]
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_amr',
            '-topic', 'robot_description',
            '-z', '0.2'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        robot_state_publisher,
        spawn_robot,
        bridge
    ])
