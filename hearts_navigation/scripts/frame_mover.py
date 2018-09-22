#!/usr/bin/env python
import roslib
import rospy
import tf
from std_msgs.msg import String

def frame_change(x):
    (pos,ori) = listener.lookupTransform("/odom","/base_footprint",rospy.Time())
    rospy.set_param('erl_pos', pos)
    rospy.set_param('erl_ori', ori)

if __name__ == '__main__':
    rospy.init_node('transform_mover')
    br = tf.TransformBroadcaster()
    rospy.Subscriber("set_erl_frame", String, frame_change)
    listener = tf.TransformListener()
    rospy.sleep(1)
    frame_change('x')
    r = rospy.Rate(1)    

    while not rospy.is_shutdown():
        pos = rospy.get_param('erl_pos')
        ori = rospy.get_param('erl_ori')
        br.sendTransform(pos,ori,rospy.Time.now(),"/erl_frame","/odom")
        r.sleep()
        
     
