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
from std_msgs.msg import String

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
sum_err_x = 0
sum_err_y = 0


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
    global sum_err_x
    global sum_err_y

    x = msg.pose.position.x
    y = msg.pose.position.y
    z = msg.pose.position.z

    last_err_x = now_err_x
    last_err_y = now_err_y
    now_err_x = x - 1300
    now_err_y = y - 500
    sum_err_x += now_err_x
    sum_err_x += now_err_y

    px = 0.0002
    py = 0.0002

    if twist.linear.x > 0:
        kdx = -0.005
    else:
        kdx = 0.005

    if twist.linear.y > 0:
        kdy = 0.005
    else:
        kdy = -0.005

    linear_vel = 0.1

    if -270 < now_err_x < 270:
        twist.linear.x = 0
        # time.sleep(1)
    else:
        # twist.linear.x = px * linear_vel + kdx * (now_err_x - last_err_x) * linear_vel
        # twist.linear.x = px * linear_vel + kdx * (now_err_x - last_err_x)
        twist.linear.x = px * now_err_x

    if -270 < now_err_y < 270:
        twist.linear.y = 0
        # time.sleep(1)
    else:
        # twist.linear.y = -py * linear_vel - kdy * (now_err_y - last_err_y) * linear_vel
        # twist.linear.y = -py * linear_vel - kdy * (now_err_y - last_err_y)
        twist.linear.y = -py * now_err_y - 0.01

    twist.linear.z = 0.0

    if twist.linear.x > 0.08:
        twist.linear.x = 0.08

    if twist.linear.x < -0.08:
        twist.linear.x = -0.08

    if twist.linear.y > 0.08:
        twist.linear.y = 0.08

    if twist.linear.y < -0.08:
        twist.linear.y = -0.08

    twist.angular.x = 0.0
    twist.angular.y = 0.0
    twist.angular.z = 0.0

    print x, y
    print twist.linear.x, twist.linear.y
    print "ok"
    cmd_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=1)
    # rate = rospy.Rate(20)   # 10hz

    cmd_pub.publish(twist)
    print "bebop send cmd!"


if __name__ == '__main__':

    try:
        rospy.init_node('ctrl_node')
        # now_err_x = 0
        # takeoff()
        # time.sleep(5)
        print "Go!!!"
        rospy.Subscriber('/vrpn_client_node/bebop/pose', PoseStamped, callback)

        print "wait 3s ..."
        time.sleep(50)
        # cmd()
        land()

    except rospy.ROSInterruptException:
        pass

