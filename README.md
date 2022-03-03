# RTAB MAP on Jetson nano: 

The idea behind this approach is that RTABmap and realsense sdk both of them use opencv. If it is possible to optimize opencv with cuda then we can use GPU on the jetson nano board to improve performance of the algorithm. RTABMAP also use PLC which can also be CUDA optimized however that is future works for this project.

In order to acieve this, we need to achieve following goals, which are explained in detail in this document:

* Building Opencv with CUDA on source
* Building Realsense SDK on source (this was tested on the platform which is described in the **hardware**.


## Requirements 

**Hardware**

* Jetson Nano 4gb RAM version
* Intel D435i 
* Can be tethered with 5V and 2.5A power supply (NOTE: this process wants nano to function at maximum power)
* For non-tethered use nano can be either powered with 5V power supply on A1 or with opencr and a battery (refer [nano developer kit](https://developer.download.nvidia.com/assets/embedded/secure/jetson/Nano/docs/NV_Jetson_Nano_Developer_Kit_User_Guide.pdf?LIDWJlZlifSKHCoJzaC7hF_i5enaLjpvzu3YFtgY3k1X6Qlm-8BuaqS0HdLyT4vowJQd_4g9C-cwjvmNfVDFZlP18_jpgAUb1jDHhk-7KrcLBbi3vOB_yIWK6VLNvONSOLWhIOSQ2K89cruhE3RDPJ3PN13dughcO3uOmb-HGkno-NGGASWBK064pTOp9ytylU0&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczpcL1wvd3d3Lmdvb2dsZS5jb21cLyJ9) and [waffle 3 assembly](https://emanual.robotis.com/docs/en/platform/turtlebot3/hardware_setup/) connect 5v & ground on nano to DV5v and out of opencr) 
* Fan

**Software**

* tegra210 OS (latest till building this project [follow this link](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) to download latest os for nano.
* jetpack 4.6


## Building opencv on source with CUDA flag

I have tried OpenCV 4.5.1 for this project. However, you can test other versions as well. Please refer to [Q engineering blog](https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html) which I have followed for this purpose. 

But before that you need some tools to monitor GPU usage on nano. I have used [JTOP](https://github.com/rbonghi/jetson_stats) for this purpose. 

### JTOP

Install pip on jetson nano 

```
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
$ rm get-pip.py
```

Now install jtop using pip 

```
$ sudo -H pip install -U jetson-stats
```

To see if it is install just type ``` jtop ``` and hit run.

Now, you can start building opencv. But before that ensure that you have lots of Disk space (atleast 13gb of empty space). It is higly recomended that you should not have anything 
in your jetson nano before following this guide.

### Enlarge memory swap

You can do these either in traditional way or using jtop 

#### traditional way

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install nano
$ sudo apt-get install dphys-swapfile
$ sudo nano /sbin/dphys-swapfile
# CONF_MAXSWAP=6074
# reboot afterwards
$ sudo reboot.
```

Trust me, the nano was suffering with swap size of 4096 hence, use 6074 just to be safe.

#### jtop way

In page 4 MEM:

* Select s to Enable extra swap
* Press + Increase the swap size and increase upto 6 gb. 
* ``` sudo reboot ```

Type ``` free -m ``` to see if it was sucesful.

#### install dependencies

```
$ sudo ldconfig
# third-party libraries
$ sudo apt-get install build-essential cmake git unzip pkg-config zlib1g-dev
$ sudo apt-get install libjpeg-dev libjpeg8-dev libjpeg-turbo8-dev
$ sudo apt-get install libpng-dev libtiff-dev libglew-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev
$ sudo apt-get install libgtk2.0-dev libgtk-3-dev libcanberra-gtk*
$ sudo apt-get install python-dev python-numpy python-pip
$ sudo apt-get install python3-dev python3-numpy python3-pip
$ sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev
$ sudo apt-get install libtbb2 libtbb-dev libdc1394-22-dev libxine2-dev
$ sudo apt-get install gstreamer1.0-tools libgstreamer-plugins-base1.0-dev
$ sudo apt-get install libgstreamer-plugins-good1.0-dev
$ sudo apt-get install libv4l-dev v4l-utils v4l2ucp qv4l2
$ sudo apt-get install libtesseract-dev libxine2-dev libpostproc-dev
$ sudo apt-get install libavresample-dev libvorbis-dev
$ sudo apt-get install libfaac-dev libmp3lame-dev libtheora-dev
$ sudo apt-get install libopencore-amrnb-dev libopencore-amrwb-dev
$ sudo apt-get install libopenblas-dev libatlas-base-dev libblas-dev
$ sudo apt-get install liblapack-dev liblapacke-dev libeigen3-dev gfortran
$ sudo apt-get install libhdf5-dev libprotobuf-dev protobuf-compiler
$ sudo apt-get install libgoogle-glog-dev libgflags-dev
```

#### Install opencv source file

```
$ cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.1.zip
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.1.zip
# unpack
$ unzip opencv.zip
$ unzip opencv_contrib.zip
# some administration to make live easier later on
$ mv opencv-4.5.1 opencv
$ mv opencv_contrib-4.5.1 opencv_contrib
# clean up the zip files
$ rm opencv.zip
$ rm opencv_contrib.zip
```

make a build directory

```
$ cd ~/opencv
$ mkdir build
$ cd build
```
#### Build and make

Till now you have just installed important dependencies for opencv, now at this step the real trouble begins

Before that you have to specify where the nvcc is located. You have to do this by making some change in the bashrc file:

```
$ sudo nano ~/.bashrc
# Copy below stuff into bashrc file
export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda/lib64\
                         ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
# after exiting from nano source the bash file
$ source ~/.bashrc
```

cmake step 

```
$cd ~/opencv/build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
-D WITH_OPENCL=OFF \
-D WITH_CUDA=ON \
-D CUDA_ARCH_BIN=5.3 \
-D CUDA_ARCH_PTX="" \
-D WITH_CUDNN=ON \
-D WITH_CUBLAS=ON \
-D ENABLE_FAST_MATH=ON \
-D CUDA_FAST_MATH=ON \
-D OPENCV_DNN_CUDA=ON \
-D ENABLE_NEON=ON \
-D WITH_QT=OFF \
-D WITH_OPENMP=ON \
-D BUILD_TIFF=ON \
-D WITH_FFMPEG=ON \
-D WITH_GSTREAMER=ON \
-D WITH_TBB=ON \
-D BUILD_TBB=ON \
-D BUILD_TESTS=OFF \
-D WITH_EIGEN=ON \
-D WITH_V4L=ON \
-D WITH_LIBV4L=ON \
-D OPENCV_ENABLE_NONFREE=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D BUILD_opencv_python3=TRUE \
-D OPENCV_GENERATE_PKGCONFIG=ON \
-D BUILD_EXAMPLES=OFF ..
```
before moving to the next step it is higly recomended that you put the fan at maximum speed (you can do it using jtop) and open system monitor (app in jetson nano to see cpu 
utilization and memory use) and jtop. It is highly possible that system might freeze but be patient. This is the step where you should monitor the system heavily. It may take
upto one hour(not less than one hour might take more than thi) for this step.

```
$ make -j4
```
#### Final touch

If it was succesful without any error then you should feel lucky! This step still make me anxious. Now you can remove the old opencv

```
$ sudo rm -r /usr/include/opencv4/opencv2
$ sudo make install
$ sudo ldconfig
# cleaning (frees 300 MB)
$ make clean
$ sudo apt-get update
```

Now check if it is properly installed:

```
$ python3
$ import cv2
$ exit()
```

If it was sucesful then Hurray!!! and also check jtop info section, now it should show something like " opencv cuda compiled:YES ".

If you do not intend to use opencv with C/C++ and if you want to use opencv for anyother purposes except for described in this document you should definetly read **cleaning**
section of [QEngineering](https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html) blog before performing the below step:

```
$ sudo rm -rf ~/opencv
$ sudo rm -rf ~/opencv_contrib
```
## Building Realsense SDK from source 

Refer to [Official GitHub repo](https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md) for further refernce for building it from source on jetson 
nano. We are building using Native backend for realsense sdk because it is recomended in the official documentation. If you want to use multiple camera then you should try RSUSB 
backend. As per official documentation and to best of my knowledge this was not tested on Jetson nano before. However, I think it is possible on latest version of jetpack which is used in this project. Due to this reason, It takes a lot of computational power to do so. One of the other reason that we increased the swap size to such extend was to make sure the system won't crash while this process as well. 

Before that you should verify that it has atleast 2.5Gb of free space and also ensure that other usb devices are not connected (except for essentials like wifi, mouse and keyboard).

Download the source file from GitHub

```
$ cd ~
$ git clone https://github.com/IntelRealSense/librealsense.git
# Navigate to librealsense directory that was just created
$ cd librealsense/scripts
# now run the patch-realsense-ubuntu-L4T.sh  file
$ ./patch-realsense-ubuntu-L4T.sh  
```

Install missing dependencies and make build directory

```
$ sudo apt-get install git libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev -y
./scripts/setup_udev_rules.sh  
$ mkdir build 
$ cd build  
```

Now again, before this step just open the monitoring tools that you used the last section:

```
$ cmake .. -DBUILD_EXAMPLES=true -DCMAKE_BUILD_TYPE=release -DFORCE_RSUSB_BACKEND=false -DBUILD_WITH_CUDA=true 
$ make -j4 
$ sudo make install
```
As you can see the cuda flag is already on and due to the change in the source file you should not get any error. However, if you get any error regarding Cuda/nvcc not found i would suggest try different methods provided in [cuda community](https://forums.developer.nvidia.com/t/cuda-nvcc-not-found/118068).

If you are lucky and your system didn't crashed then try connecting the camera and running realsense sdk with ``` realsense-viewer```.

If you open ```jtop``` then you will observe that as GPU usage increases load on cpu decreases, which suggest that it is using GPU properly. 

## ROS 

If you have completed above steps then congrats! You have completed the hardest parts. Now you only need to install ROS and simple stuffs for this thing to function.

### Install ROS Melodic

Due to Ubuntu version of Nano you can only use Melodic on Nano. But thats not bad. For installing Melodic on Nano you can refer to [Stereo lab's](https://www.stereolabs.com/blog/ros-and-nvidia-jetson-nano/) guide for reference. 

Seting Up the keys:

```
$ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
$ sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
$ sudo apt update
```

Now install ROS Melodic

```
$ sudo apt install ros-melodic-desktop
```

make some changes in the bashrc and source it

```
$ echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc 
$ source ~/.bashrc
```
Install rosdep

```
$ sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
$ sudo rosdep init 
$ rosdep update
```

to check if it is installed properly, run ```roscore```.

Next step is to build catkin ws:

```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/
$ catkin_make
$ source devel/setup.bash
```
### ROS wrapper for Realsense SDK

The first thing you should do after installing ROS is to build a ros wrapper for Realsense SDK you can find the official document [here](https://github.com/IntelRealSense/realsense-ros).

Change your directory to catkin:

```
$ cd ~/catkin_ws/src/
$ git clone https://github.com/IntelRealSense/realsense-ros.git
$ cd realsense-ros/
$ git checkout `git tag | sort -V | grep -P "^2.\d+\.\d+" | tail -1`
cd ..
```

Don't forget to install ddynamic_reconfigure and other dependent package as mentioned in the [official github](https://github.com/IntelRealSense/realsense-ros) repository otherwise you will get error while catkin_make step.

```
$ sudo apt-get install ros-melodic-ddynamic_reconfigure
```

The real fun begans now (catkin make step):

```
$ cd ~/catkin_ws
$ catkin_make clean
$ catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
$ catkin_make install
```

Make changes in the bashrc file and souce it:

```
$ echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
$ source ~/.bashrc
```
You can check if everything is installed properly by using this command:

```
roslaunch realsense2_camera rs_camera.launch
```
open ```rviz``` and change fixed frame to camera link and chose any topic (first try using /camera/color/image_raw topic) and see if it works fine. 

If it works then congrats! Honestly, you have done most of the work.

### Install RTABmap

I have just installed rtabmap using binary file because i don't see any reason to install RTABMAP from source. Everything that can use GPU is already CUDA optimized. But i would recomend giving it a try.

```
$ sudo apt-get install ros-melodic-rtabmap-ros
```

You can also download an additional file for showing gpu optimization which you can find [here](https://github.com/jetsonhacks/gpuGraphTX). 

## Usage

For the purpose of this project, I have modified [hand held mapping](http://wiki.ros.org/rtabmap_ros/Tutorials/HandHeldMapping) tutorial. 

**NOTE**

Do not use RTABMAP viewer in jetson nano, use RVIZ instead.

There are 3 packages that you need to run for using RTABMAP in the following order:

* Realsense ROS wrapper
* IMU filter madgwick
* RTABMAP

### Install IMU madwick filter:

```
$ sudo apt-get install ros-melodic-imu-filter-madgwick
```

Run the following commands in different terminals

```
$ roslaunch realsense2_camera rs_camera.launch \
    align_depth:=true \
    unite_imu_method:="linear_interpolation" \
    enable_gyro:=true \
     enable_accel:=true

$ rosrun imu_filter_madgwick imu_filter_node \
    _use_mag:=false \
    _publish_tf:=false \
    _world_frame:="enu" \
    /imu/data_raw:=/camera/imu \
    /imu/data:=/rtabmap/imu

 $ roslaunch rtabmap_ros rtabmap.launch \
    rtabmap_args:="--delete_db_on_start --Optimizer/GravitySigma 0.3" \
    depth_topic:=/camera/aligned_depth_to_color/image_raw \
    rgb_topic:=/camera/color/image_raw \
    camera_info_topic:=/camera/color/camera_info \
    approx_sync:=false \
    wait_imu_to_init:=true \
    imu_topic:=/rtabmap/imu  rtabmapviz:=false  rviz:=true
```
Once the rviz is on select Map cloud and map graph. In the map cloud download map to load all the points in the rviz. It would show some error initially but after sometime it should load. 

If you want to not start mapping with fresh map remove ``` rtabmap_args:="--delete_db_on_start --Optimizer/GravitySigma 0.3" ```
## Performance

### FPS on RVIZ 
The frame rate usually fluctuates between 19 and 26 and best it can get upto is 30 
![Screenshot from 2022-02-09 17-12-48](https://user-images.githubusercontent.com/50763982/153254181-3aea52a3-00ff-4d66-9903-8ed422c98ad4.png)
![Screenshot from 2022-02-09 17-13-13](https://user-images.githubusercontent.com/50763982/153254193-1a1f8318-372a-4b1c-968a-eb2450a584a7.png)
![Screenshot from 2022-02-09 17-13-48](https://user-images.githubusercontent.com/50763982/153254198-31bfd1dd-a818-4a16-b116-7736e9161776.png)
![Screenshot from 2022-02-09 17-13-57](https://user-images.githubusercontent.com/50763982/153254202-6f684f35-8e13-41b2-a839-870890fd1267.png)
![Screenshot from 2022-02-09 17-14-04](https://user-images.githubusercontent.com/50763982/153254207-acfb789a-c69d-494c-937b-b4cda4b51a39.png)


However, this are screenshots and it is highly possible that this might have affected the frame rate, hence i have also taken some pictures from mobile which suggest that frame rate actually range between 26 and 30 (the frame rate reduces when the camera is moving and improves when camera is stationary). 

![WhatsApp Image 2022-02-09 at 17 24 45 (2)](https://user-images.githubusercontent.com/50763982/153255968-09a365f3-4502-4649-b500-9fd764688fe4.jpeg)
![WhatsApp Image 2022-02-09 at 17 24 45 (1)](https://user-images.githubusercontent.com/50763982/153256130-ae73258f-c2f6-486b-b885-498516c64437.jpeg)

### GPU and CPU performance 

GPU and CPU of jetson nano was monitored during this mapping to get this results. [jtop](https://github.com/rbonghi/jetson_stats.git) was used to monitor this results. 



https://user-images.githubusercontent.com/50763982/153261807-df0d8e17-2bf6-43e7-95d9-dcdb13e31dc6.mp4



https://user-images.githubusercontent.com/50763982/153261818-c895b328-a9f2-4d08-929c-b52ebf2af39c.mp4

In both of the cases the camera was moved and kept stationary to analyse behaviour of the system in dynamic as well as stationary state.

To specify the results, CPU was almost 100% optimized through out the run (all the 4 cores) and there are fluctuations in GPU usage. 
For this project, we are using cuda optimized opencv4 which comes with jetpack 4.5. RTAB MAP and realsense sdk ROS wrapper which are two of the most image processing focused packages in this whole system. They utilize this version of opencv to process information. This is one of the reason we are getting better reasons as compared to pi. Furthermore, this also explains fluctuations in GPU usage.

### Future objective analysis

This system can be tested on a turtlebot waffle with robot on chair controller, with jtop active. 

The same can be done on A1
