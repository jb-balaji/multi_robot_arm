# Enabling Multi-Robot ARM in Gazebo for ROS2
This git repository presents an ROS2 package that demonstrates the simultaneous spawning of multiple robotic arms in a Gazebo simulation. Historically, such an application is difficult to come by within the ROS2 community, leaving a knowledge gap for developers looking to implement multi-arm robotic systems. The work outlined here not only fills this void but also offers a practical guide for beginners and interested parties looking to replicate similar multi-robot simulations in Gazebo.

The UR5 robotic arm, a versatile and widely-used model in robotics, serves as the core of this demonstration. By focusing on this particular model, the tutorial ensures a broad relevance to a multitude of potential robotic applications.

![image](https://github.com/arshadlab/multi_robot_arm/assets/85929438/4e052e79-65c7-4fe5-b73a-871b76b9f01e)
![image](https://github.com/arshadlab/multi_robot_arm/assets/85929438/3189c420-33c1-424c-aaa4-0cc2b8cc868c)

## Demo: Gazebo Harmonic Simulation
Check out the demo video showcasing multi-robot arm simulation with Gazebo Harmonic:

![Gazebo Harmonic Demo](./run.mp4)

## What's New

### ROS2 Jazzy & Gazebo Harmonic Support
We've added full support for **ROS2 Jazzy** and **Gazebo Harmonic**, the latest stable distributions in the ROS2 ecosystem. This brings several benefits:

- **Enhanced Physics Simulation**: Gazebo Harmonic provides improved physics accuracy and performance
- **Improved Compatibility**: Full integration with modern ROS2 tooling and libraries
- **Better Performance**: Optimized for the latest hardware and software stacks
- **ROS-Gazebo Bridge**: Native support via `ros-gz` for seamless ROS2-Gazebo integration

### Launch Files
- **`gazebo_arm.launch.py`**: For ROS2 Humble + Gazebo 11 (legacy)
- **`gazebo_harmonic_arm.launch.py`**: For ROS2 Jazzy + Gazebo Harmonic (recommended)

## Python MoveIt2 Bindings
The present version of this tutorial employs a fork of pymoveit2, a Python library developed to facilitate interaction with MoveIt2. This has been an effective approach and served the purpose well.

However, in recent times, MoveIt2 has introduced native Python bindings in its codebase. These bindings enable direct interaction with MoveIt2 via Python, eliminating the need for additional libraries like pymoveit2. This advancement simplifies the setup process, reduces dependency issues, and potentially enhances performance and stability.

As part of ongoing improvements and in the spirit of keeping up with these updates, future versions of this tutorial may transition to using the Python bindings provided directly by MoveIt2. This would replace the current reliance on the pymoveit2 fork, streamlining the implementation process and ensuring compatibility with future developments in MoveIt2. Consequently, this change will not only refine the tutorial but also make it more adaptable and robust for future use-cases.

## Setup

### Supported Configurations
The package is verified and tested with the following configurations:

| ROS2 Version | Gazebo Version | Launch File | Status |
|---|---|---|---|
| Humble | 11 | `gazebo_arm.launch.py` | ✓ Tested |
| Jazzy | Harmonic | `gazebo_harmonic_arm.launch.py` | ✓ Tested |

### Dependencies

**For ROS2 Humble + Gazebo 11:**
- ROS2 Humble
- moveit2
- pymoveit2
- Gazebo 11

**For ROS2 Jazzy + Gazebo Harmonic:**
- ROS2 Jazzy
- moveit2
- pymoveit2
- Gazebo Harmonic
- ros-gz (ROS-Gazebo bridge)

## Clone and Build

### For ROS2 Humble
```bash
source /opt/ros/humble/setup.bash
mkdir -p robot_ws/src
cd robot_ws/src
git clone https://github.com/arshadlab/multi_robot_arm.git
git clone https://github.com/arshadlab/pymoveit2.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

### For ROS2 Jazzy
```bash
source /opt/ros/jazzy/setup.bash
mkdir -p robot_ws/src
cd robot_ws/src
git clone https://github.com/arshadlab/multi_robot_arm.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
sudo apt install ros-jazzy-pymoveit2
colcon build --symlink-install
```

**Note:** For ROS2 Jazzy, pymoveit2 is available as an apt package, so cloning from git is not required.

## Launch

### Option 1: ROS2 Humble with Gazebo 11
#### Console A (Launch Gazebo)
```bash
source ./install/setup.bash
ros2 launch multi_robot_arm gazebo_arm.launch.py
```

### Option 2: ROS2 Jazzy with Gazebo Harmonic (Recommended)
#### Console A (Launch Gazebo Harmonic)
```bash
source ./install/setup.bash
ros2 launch multi_robot_arm gazebo_harmonic_arm.launch.py
```

### Triggering ARM Movement
#### Console B (Trigger ARM movement)

ARM1 movement to position [0.5, 0.4, 0.2] using kinematic path planner:
```bash
source ./install/setup.bash
cd ./src/pymoveit2/examples
python ex_pose_goal.py --ros-args -r __ns:=/arm1 -p position:=[0.5,0.4,0.2]
```

ARM4 movement to position [0.5, 0.4, 0.2] using cartesian path planner:
```bash
source ./install/setup.bash
cd ./src/pymoveit2/examples
python ex_pose_goal.py --ros-args -r __ns:=/arm4 -p position:=[0.5,0.4,0.2] -p cartesian:=True
```

**Note:** The `__ns:=/namespace` parameter directs commands to a specific instance of robot. Position coordinates are given relative to arm position.

## Acknowledgement
pymoveit2 → https://github.com/AndrejOrsula/pymoveit2
