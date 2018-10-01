#!/usr/bin/env python
import roslib
import rospy
import tf
from geometry_msgs.msg import TransformStamped, Quaternion
from std_msgs.msg import String

'''Deals with seting the locations for erl coordinate frame and target locaiton,
   also returns tiago'location in erl coordinates and target's location relative
   to tiago'''


#set erl_frame coords to be tiago's current location
def frame_change(x):
    (pos,ori) = listener.lookupTransform("/map","/base_footprint",rospy.Time())
    rospy.set_param('erl_pos', pos)
    rospy.set_param('erl_ori', ori)

#sets target location relative to erl_frame
def set_target(target):
    pos = [target.transform.translation.x,
           target.transform.translation.y,
           target.transform.translation.z]
    ori = [float(target.transform.rotation.x),
           float(target.transform.rotation.y),
           float(target.transform.rotation.z),
           float(target.transform.rotation.w)]
    rospy.set_param('target_pos', pos)
    rospy.set_param('target_ori', ori)

#prints the goal's location relative to tiago
def tiago_to_goal(x):
    (pos,ori) = listener.lookupTransform("/base_footprint","/target",rospy.Time())
    rospy.loginfo(pos)
    rospy.loginfo(ori)

#prints tiago's location relative to the erl_frame
def tiago_loc(x):
    (pos,ori) = listener.lookupTransform("/erl_frame","/base_footprint",rospy.Time())
    rospy.loginfo(pos)
    rospy.loginfo(ori)


#create the node
rospy.init_node('transform_mover')

#broadcaster to let ros know where the frames are
br = tf.TransformBroadcaster()

#subscribe to the required topics
rospy.Subscriber("set_erl_frame", String, frame_change)
rospy.Subscriber("set_move_target", TransformStamped, set_target)
rospy.Subscriber("where_is_target", String, tiago_to_goal)
rospy.Subscriber("where_am_i", String, tiago_loc)

#listener allows us to look up Tiago's current location
listener = tf.TransformListener()

#sleep to give everything time to initialize
rospy.sleep(1)

#invoke frame change & set_target so the frames exists when the while loop starts
frame_change('x')
#create a transform of all 0 to set as initial target
targ = TransformStamped()
targ.transform.translation.x = 0
targ.transform.translation.y = 0
targ.transform.translation.z = 0
targ.transform.rotation = Quaternion(0,0,0,1)

set_target(targ)
rospy.sleep(1)

#frames are published at 1Hz
r = rospy.Rate(5)

#continuously publish the frames so that other tf functions can use them
while not rospy.is_shutdown():
    pos = rospy.get_param('erl_pos')
    ori = rospy.get_param('erl_ori')
    br.sendTransform(pos,ori,rospy.Time.now(),"/erl_frame","/map")

    pos = rospy.get_param('target_pos')
    ori = rospy.get_param('target_ori')
    br.sendTransform(pos,ori,rospy.Time.now(),"/target","/erl_frame")
    r.sleep()


#if __name__ == '__main__':
