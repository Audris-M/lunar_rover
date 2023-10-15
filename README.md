# lunar_rover

For code running, clone the repo, probably run catki clean and catkin build build.

for code running (start roscore):
1. python3 reader_for_imu_data.py
2. in another terminal : python3 visualization_code.py
3. rosbag play --loop neutral_position_imu.bag (this had the IMU stable so gives better understanding of whats going on)
4. rviz (in rviz change fixed frame to base_link , add markers choose topic /imu_marker , add axes and choose topic orientation frame)
