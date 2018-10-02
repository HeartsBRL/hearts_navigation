#!/usr/bin/env python


import roslib
import rospy
import tf

rospy.init_node('erl_transformer')
lis = tf.TransformListener()
r = rospy.Rate(1)

r.sleep()
(trans,rot) = lis.lookupTransform('erl_frame', 'base_footprint', rospy.Time(0))
ori = tf.transformations.euler_from_quaternion(rot)

stuff = [trans[0],trans[1],ori[2]]
print(stuff)
