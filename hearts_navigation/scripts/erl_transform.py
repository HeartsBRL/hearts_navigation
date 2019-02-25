#!/usr/bin/env python
import sys
import roslib
import rospy
import tf

rospy.init_node('erl_transformer')
lis = tf.TransformListener()
# r = rospy.Rate(1)

rospy.sleep(1)
(trans,rot) = lis.lookupTransform('map', 'base_footprint', rospy.Time(0))
ori = tf.transformations.euler_from_quaternion(rot)

#stuff = [trans[0],trans[1],ori[2]]
#print(stuff)

myargv = rospy.myargv(argv=sys.argv)

print('\"' + str(myargv[1]) + '\"' + ': {')
print('\t\t\"x\" : ' + str(trans[0]) + ',')
print('\t\t\"y\" : ' + str(trans[1]) + ',')
print('\t\t\"theta\" : ' + str(ori[2]))
print('\t},')
#pub = rospy.publisher('mydata.txt', String, queue_size=10)
#rospy.init_node('node_name')
#r = rospy.Rate(10)
#while not rospy.is_shutdown();
#    pub.publish('x= ' + str(trans[0])
#    'y= ' + str(trans[1]),
#    'rot= ' + str(ori[2]))
