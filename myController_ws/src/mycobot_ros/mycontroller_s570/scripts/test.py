#!/usr/bin/env python

"""
This package need `pymycobot`.
This file for test the API if right.

Just can run in Linux.
"""
from exoskeleton_api import Exoskeleton, ExoskeletonSocket
import rospy
from math import pi
import time
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import rosnode
import os
import subprocess

os.system("sudo chmod 777 /dev/ttyACM*")

obj = Exoskeleton(port="/dev/ttyACM0")

def shutdown_ros_node(node_name):
    try:
        subprocess.run(['rosnode', 'kill', node_name])
        print(f"Node {node_name} has been shutdown.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# 初始化ROS节点
rospy.init_node("fr3_joint_state_publisher")
shutdown_ros_node('joint_state_publisher_gui')
#rospy.loginfo("已成功杀死节点")
# 创建发布者
pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
# 设置发布频率
rate = rospy.Rate(100) # 100Hz
# 消息实例
joint_state = JointState()
# 发布消息
while not rospy.is_shutdown():
    joint_state.header = Header()
    # 填充消息内容，例如关节名称、位置、速度和力
    joint_state.header.stamp = rospy.Time.now()
    joint_state.name = [
    'j1',
    'j2',
    'j3',
    'j4',
    'j5',
    'j6']
    l_angle = obj.get_arm_data(1)
    l_angle = l_angle[:7]
    l_angle = [int(x) for x in l_angle]
    r_angle = obj.get_arm_data(2)
    r_angle = r_angle[:7]
    r_angle = [int(y) for y in r_angle]
    
  
    rad_l_angle = [a/180*pi for a in l_angle]
    
    joint_state.position = [0.0] * 6  # Initialize with 6 elements
    
    #only use r_angle and converse joints angle 
    
    #FR 1 = EX 2
    joint_state.position[0] = -r_angle[1] - 70
    #FR 2 = EX 1
    joint_state.position[1] =  r_angle[0] -170
    #FR 3 = EX 4
    joint_state.position[2] = -r_angle[3] - 45
    #FR 4 = EX 6
    joint_state.position[3] =  r_angle[5] - 50
    #FR 5 = EX 5 
    joint_state.position[4] =  r_angle[4] + 90
    #FR 6 = EX 7
    joint_state.position[5] = -r_angle[6]
    
    # convert to position 
    joint_state.position = [a/180*pi for a in joint_state.position]

    joint_state.effort = []
    joint_state.velocity = []
    # 发布消息
    pub.publish(joint_state)
    rospy.loginfo('消息成功发布')
    
    for i in range(6):
        print(f"j{i+1}: {joint_state.position[i]/pi*180}")

    # 等待，允许其他节点处理
    rate.sleep()

