# RTAB MAP on Jetson nano: 

## Requirements 

**Hardware**

* Jetson Nano 4gb RAM version
* Intel D435i 
* Can be tethered with 5V and 2.5A power supply (NOTE: this process wants nano to function at maximum power)
* For non-tethered use nano can be either powered with 5V power supply on A1 or with opencr and a battery (refer [nano developer kit](https://developer.download.nvidia.com/assets/embedded/secure/jetson/Nano/docs/NV_Jetson_Nano_Developer_Kit_User_Guide.pdf?LIDWJlZlifSKHCoJzaC7hF_i5enaLjpvzu3YFtgY3k1X6Qlm-8BuaqS0HdLyT4vowJQd_4g9C-cwjvmNfVDFZlP18_jpgAUb1jDHhk-7KrcLBbi3vOB_yIWK6VLNvONSOLWhIOSQ2K89cruhE3RDPJ3PN13dughcO3uOmb-HGkno-NGGASWBK064pTOp9ytylU0&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczpcL1wvd3d3Lmdvb2dsZS5jb21cLyJ9) and [waffle 3 assembly](https://emanual.robotis.com/docs/en/platform/turtlebot3/hardware_setup/) connect 5v & ground on nano to DV5v and out of opencr) 
* Fan

**Software**

For this system we are using Melodic however, it will also works on Noetic

* tegra210 OS (latest till building this project [follow this link](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit) to download latest os for nano.
* jetpack 4.6
* ROS Melodic (Installed using [this link](https://www.stereolabs.com/blog/ros-and-nvidia-jetson-nano/) and taking reference from [official installation guide](http://wiki.ros.org/melodic/Installation/Ubuntu)

**NOTE: during installation of any of the software, if it is asked to install opencv just find opencv4 in jetson nano and change path to the same. Also refer to [this](https://github.com/ros-perception/vision_opencv/issues/345) repository** 

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
