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


def land():
    land1_pub = rospy.Publisher('/bebop/land', Empty, queue_size=10)
    land2_pub = rospy.Publisher('/bebop2/land', Empty, queue_size=10)
    i = 0
    while 1:
        time.sleep(1)
        land1_pub.publish(Empty())
        print "bebop_1 land!"
        land2_pub.publish(Empty())
        print "bebop_2 land!"
        i += 1
        if i == 1:
            break


if __name__ == '__main__':

    try:
        rospy.init_node('land_node')
        land()
        time.sleep(5)

    except rospy.ROSInterruptException:
        pass

