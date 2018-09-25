#!/bin/bash

if [ $# -lt 1 ]
then
    echo "no map name"
else
    echo "map_name=$1"
    rosservice call /pal_navigation_sm "input: 'LOC'"
    sleep 2
    rosservice call /pal_map_manager/change_map "input: '$1'"
    sleep 2
    rosrun rviz rviz -d ~/workspaces/hearts_erl/src/hearts_navigation/hearts_navigation/config/navigation_public_sim.rviz
fi

echo "$0 complete"


