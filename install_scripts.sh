#!/bin/bash

echo "Installing ros2_build_helper"
cp ./ros2_build_helper/ros2_build.py ~/.local/bin/ros2_build
chmod +x ~/.local/bin/ros2_build
echo "ros2_build is installed"

cp ./ros2_build_helper/ros2_test.py ~/.local/bin/ros2_test
chmod +x ~/.local/bin/ros2_test
echo "ros2_test is installed"
