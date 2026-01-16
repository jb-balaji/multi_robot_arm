#!/usr/bin/env python3
"""
Continuous dancing motion for all arms - cycles through poses A->B->C->D until Ctrl+C
Author: Jb
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time
import signal
import sys


class WavingArmsNode(Node):
    def __init__(self):
        super().__init__('waving_arms')
        
        # Create publishers for all 4 arms
        self.arm_publishers = {}
        for i in range(1, 5):
            topic = f'/arm{i}/arm_controller/joint_trajectory'
            self.arm_publishers[f'arm{i}'] = self.create_publisher(JointTrajectory, topic, 10)
        
        # Joint names that work with the controllers
        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint', 
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        # Define poses - cycling through A -> B -> C -> D
        # [shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3]
        self.pose_A = [0.8, -0.8, 1.0, -1.5, -1.5, 0.0]     # Base right, arm reaching
        self.pose_B = [-0.8, -1.3, 1.8, -0.8, 1.5, 0.0]    # Base left, arm high
        self.pose_C = [0.0, -0.5, 0.3, -2.0, 0.0, 1.0]     # Center, arm forward with wrist twist
        self.pose_D = [0.5, -1.8, 2.2, -0.5, -0.5, -1.0]   # Base right, dramatic pose with wrist
        
        self.poses = [self.pose_A, self.pose_B, self.pose_C, self.pose_D]
        self.pose_names = ['A', 'B', 'C', 'D']
        self.current_pose_index = 0
        self.running = True
        self.get_logger().info('Dance motion ready. Press Ctrl+C to stop.')
    
    def send_pose_to_all_arms(self, positions):
        # Send to all arms simultaneously
        for arm_name, publisher in self.arm_publishers.items():
            msg = JointTrajectory()
            msg.joint_names = self.joint_names
            
            point = JointTrajectoryPoint()
            point.positions = positions
            point.velocities = [0.0] * len(positions)
            point.time_from_start = Duration(sec=3)
            msg.points = [point]
            
            publisher.publish(msg)
    
    def wave_continuously(self):
        """Main dancing loop with continuous motion through all poses"""
        self.get_logger().info('Starting dance sequence...')
        
        # Initialize all arms to pose A first
        self.send_pose_to_all_arms(self.pose_A)
        time.sleep(6)
        
        while self.running:
            try:
                # Move to next pose in sequence
                self.current_pose_index = (self.current_pose_index + 1) % 4
                next_positions = self.poses[self.current_pose_index]
                
                # Send to all arms
                for publisher in self.arm_publishers.values():
                    if not self.running:
                        break
                    
                    msg = JointTrajectory()
                    msg.joint_names = self.joint_names
                    
                    point = JointTrajectoryPoint()
                    point.positions = next_positions
                    point.velocities = [0.0] * len(next_positions)
                    point.time_from_start = Duration(sec=2)
                    msg.points = [point]
                    
                    publisher.publish(msg)
                    time.sleep(0.1)
                
                time.sleep(1.0)
                
            except KeyboardInterrupt:
                break
        
        self.get_logger().info('Returning to home position...')
        home_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for publisher in self.arm_publishers.values():
            msg = JointTrajectory()
            msg.joint_names = self.joint_names
            
            point = JointTrajectoryPoint()
            point.positions = home_position
            point.velocities = [0.0] * len(home_position)
            point.time_from_start = Duration(sec=3)
            msg.points = [point]
            
            publisher.publish(msg)
        time.sleep(4)
    
    def shutdown(self):
        """Clean shutdown"""
        self.running = False


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\nStopping...')
    global node
    node.shutdown()


def main():
    global node
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    rclpy.init()
    node = WavingArmsNode()
    
    # Wait for publishers to be ready
    time.sleep(1)
    try:
        # Start the dance motion
        node.wave_continuously()
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
