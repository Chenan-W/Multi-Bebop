#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/12/16 下午10:14
# @Author :Chenan_Wang
# @File : ctrl_node.py.py
# @Software: PyCharm

import rospy
import time
import math
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

aaa = 0


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

    x = msg.pose.position.x
    y = msg.pose.position.y

    x_sim = [1600, 800,   0, -600, -600, -500, -500,    0,  400,  700, 0]
    y_sim = [700,  700, 700,  700,    0, -600, -600, -500, -500, -500, 0]

    global aaa

    kp = 0.0002

    x_t = x_sim[aaa]
    y_t = y_sim[aaa]

    err_x = x - x_t
    err_y = y - y_t

    now_err = math.sqrt(math.pow((x_t-x), 2) + math.pow((y_t-y), 2))

    if -270 < err_x < 270:
        twist.linear.x = 0
    else:
        twist.linear.x = kp * err_x

    if -270 < err_y < 270:
        twist.linear.y = 0
    else:
        twist.linear.y = -kp * err_y

    print 'Point:', aaa

    if now_err < 400:
        aaa = aaa + 1
        twist.linear.x = 0
        twist.linear.y = 0
        # time.sleep(1)
        if aaa >= 16:
            aaa = 16

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

    cmd_pub = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=1)
    cmd_pub.publish(twist)

    print 'x_t =', x_t, '; y_t =', y_t
    print 'x =', x, '; y =', y
    print 'speed_x =', twist.linear.x, '; speed_y =', twist.linear.y
    print 'err_x =', err_x, '; err_y =', err_y
    print 'now_err:', now_err
    print "bebop send cmd!"
    print '----------------------------'


if __name__ == '__main__':

    try:
        rospy.init_node('ctrl_node')
        takeoff()
        time.sleep(5)
        print "Go!!!"
        rospy.Subscriber('/vrpn_client_node/feiji/pose', PoseStamped, callback)

        print "wait 3s ..."
        time.sleep(50)
        land()

    except rospy.ROSInterruptException:
        pass

