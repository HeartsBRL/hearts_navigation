#!/usr/bin/env python
import roslib
import rospy
import tf
from std_msgs.msg import String

'''Simple script to place a fixed TF frame called erl_frame on the ground at
    Tiago's current location and orientation. Used for setting the origin of
    the competition coordinate frame'''

#The frame coords are updated whenever anything is published to the 
#"set_erl_frame" topic
def frame_change(x):
    (pos,ori) = listener.lookupTransform("/odom","/base_footprint",rospy.Time())
    rospy.set_param('erl_pos', pos)
    rospy.set_param('erl_ori', ori)

#create the node
rospy.init_node('transform_mover')
#broadcaster to let ros know where the frame is
br = tf.TransformBroadcaster()
#subscribe to the required topic
rospy.Subscriber("set_erl_frame", String, frame_change)
#listener allows us to look up Tiago's current location
listener = tf.TransformListener()
#sleep to give everything time to initialize
rospy.sleep(1)
#invoke the frame changer so the frame exists when the while loop starts
frame_change('x')
#frame is published at 1Hz
r = rospy.Rate(1)    

#continuously publish the frame so that other tf functions will work
while not rospy.is_shutdown():
    pos = rospy.get_param('erl_pos')
    ori = rospy.get_param('erl_ori')
    br.sendTransform(pos,ori,rospy.Time.now(),"/erl_frame","/odom")
    r.sleep()

#if __name__ == '__main__':    
