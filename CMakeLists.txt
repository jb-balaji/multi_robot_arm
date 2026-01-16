cmake_minimum_required(VERSION 3.5)
project(multi_robot_arm)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(ros_gz_sim REQUIRED)

include_directories(include)
link_directories(
  ${gazebo_dev_LIBRARY_DIRS}
)

set(THIS_PACKAGE_INCLUDE_DEPENDS
  rclcpp
  std_msgs
)

install(DIRECTORY launch config urdf worlds scripts DESTINATION share/${PROJECT_NAME})

# Install Python scripts
install(PROGRAMS
  scripts/ur_pose_goal.py
  scripts/dance_arms.py
  scripts/test_pose_goals.py
  DESTINATION lib/${PROJECT_NAME}
)
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/env-hooks/multi_robot_arm.dsv.in")

ament_package()
