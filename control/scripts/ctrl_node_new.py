#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/16 下午10:14
# @Author :Chenan_Wang
# @File : ctrl_node.py.py
# @Software: PyCharm

import rospy
import time
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped

# linear_vel = 0.05
# angular_vel = 0.0
#
# twist = Twist()
#
# twist.linear.x = linear_vel
# twist.linear.y = 0.0
# twist.linear.z = 0.0
#
# twist.angular.x = 0.0
# twist.angular.y = 0.0
# twist.angular.z = angular_vel

#
# def __init__(self):
#     self.now_err_x = 0
#     self.last_err_x = 0
#     self.sum_err_x = 0

now_err_x = 0
now_err_y = 0


def takeoff():
    takeoff_pub = rospy.Publisher('/bebop/takeoff', Empty, queue_size=10)
    rate = rospy.Rate(1)   # 10hz
    i = 0
    while 1:
        print "wait 3s ..."
        time.sleep(2)
        takeoff_pub.publish(Empty())
        print "bebop takeoff!"
        i += 1
        if i == 1:
            break


def land():
    land_pub = rospy.Publisher('/bebop/land', Empty, queue_size=10)
    rate = rospy.Rate(20)   # 10hz
    i = 0
    while 1:
        time.sleep(3.5)
        land_pub.publish(Empty())
        print "bebop land!"
        i += 1
        if i == 1:
            break


def cmd():
    cmd_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(20)   # 10hz
    while not rospy.is_shutdown():
        # cmd_pub.publish(twist)
        print "bebop send cmd!"
        rate.sleep()

# def callback(self, data):


def callback(msg):
    twist = Twist()

    global now_err_x
    global now_err_y
    kdx = 0.01
    kdy = 0.01

    x = msg.pose.position.x
    y = msg.pose.position.y
    z = msg.pose.position.z

    # kp_x = 0.001
    # ki_x = 0.001
    # kd_x = 0.001
    #
    last_err_x = now_err_x
    last_err_y = now_err_y
    now_err_x = x - 0
    now_err_y = y - 0
    # sum_err_x += now_err_x

    err_x = x - 1800
    err_y = y - 1000
    px = 0.0015 * err_x
    py = 0.0015 * err_y

    linear_vel = 0.1
    #
    # if twist.linear.x > 0.06:
    #     twist.linear.x = 0.06
    #
    # if twist.linear.x < -0.06:
    #     twist.linear.x = -0.06
    #
    # if twist.linear.y > 0.06:
    #     twist.linear.y = 0.06
    #
    # if twist.linear.y < -0.06:
    #     twist.linear.y = -0.06
    #
    # twist.angular.x = 0.0
    # twist.angular.y = 0.0
    # twist.angular.z = 0.0

    cmd_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        if -270 < err_x < 270:
            twist.linear.x = 0
        else:
            twist.linear.x = px * linear_vel + kdx * (now_err_x - last_err_x) * linear_vel

        if -270 < err_y < 270:
            twist.linear.y = 0
        else:
            twist.linear.y = -py * linear_vel - kdx * (now_err_y - last_err_y) * linear_vel

        twist.linear.z = 0.0
        cmd_pub.publish(twist)
        print x, y
        print twist.linear.x, twist.linear.y
        print "bebop send cmd!"
        rate.sleep()


if __name__ == '__main__':

    rospy.init_node('ctrl_node')
    # takeoff()
    # time.sleep(5)
    print "Go!!!"
    rospy.Subscriber('/vrpn_client_node/feiji/pose', PoseStamped, callback)

    print "wait 3s ..."
    time.sleep(50)
    # cmd()
    land()

