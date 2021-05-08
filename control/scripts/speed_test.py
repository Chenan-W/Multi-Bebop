#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/19 下午1:13
# @Author : Chenan_Wang
# @File : speed_test.py
# @Software: CLion

import rospy
import time
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped

now_err_x = 0


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


def callback(msg):
    twist = Twist()

    global now_err_x

    last_err_x = now_err_x
    now_x = msg.pose.position.x
    now_err_x = now_x - 0

    twist.linear.x = 0.02
    twist.linear.y = 0
    twist.linear.z = 0

    speed = 1000 * twist.linear.x

    speed_x = (now_err_x - last_err_x)
    sppp = 10 * (-speed_x)

    if now_x > -900:

        # print 'now_x:', now_x
        print 'x:', msg.pose.position.x, 'y:', msg.pose.position.y
        print 'Set_speed:', speed
        print 'Real_speed:', sppp
        print "bebop send cmd!!!!"
        print '————————————————————————'
    else:
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0

    cmd_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)
    cmd_pub.publish(twist)

    # rate.sleep()


if __name__ == '__main__':

    try:
        rospy.init_node('ctrl_node')
        # now_err_x = 0
        takeoff()
        time.sleep(5)
        print "Go!!!"
        rospy.Subscriber('/vrpn_client_node/bebop/pose', PoseStamped, callback)

        print "wait 3s ..."
        time.sleep(50)
        # cmd()
        land()

    except rospy.ROSInterruptException:
        pass

