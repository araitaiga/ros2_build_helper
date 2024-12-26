#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def get_args():
    # get optional arguments
    # -w: workspace name
    # -p: package name
    # -t: build this package
    # -d: build with Debug option
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workspace", type=str,
                        help="Set workspace name (default: ros2_ws)")
    parser.add_argument("-p", "--package", type=str,
                        help="Set package name (if this and -t option are not set, build entire workspace)")
    parser.add_argument("-t", "--this", action="store_true",
                        help="Build this package (if this and -p option are not set, build entire workspace)")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Build with Debug option")
    return parser.parse_args()


def ros2_build():
    # Save the current Path
    orig_path = os.getcwd()
    # if ROS2_ROOT_WS is not exported, set $HOME to default value
    if not os.environ.get("ROS2_ROOT_WS"):
        os.environ["ROS2_ROOT_WS"] = os.environ["HOME"]

    args = get_args()

    ws_name = args.workspace if args.workspace else "ros2_ws"
    ws_path = os.path.join(os.environ["ROS2_ROOT_WS"], ws_name)

    if args.this:
        current_dir_name = os.path.basename(os.getcwd())
        print(f"Set this package {current_dir_name}")
        args.package = current_dir_name

    # Change directory to workspace
    os.chdir(ws_path)

    print(f"[Build Options: workspace={ws_name}, package={args.package}]")

    # if package_name has value, build only the package
    if not args.package:
        print(f"[Build entire workspace: {ws_name}]")
        # if Debug option is set, build with Debug option
        if args.debug:
            subprocess.run(["colcon", "build", "--symlink-install",
                           "--cmake-args", "-DCMAKE_BUILD_TYPE=Debug"])
        else:
            subprocess.run(["colcon", "build", "--symlink-install",
                           "--cmake-args", "-DCMAKE_BUILD_TYPE=Release"])

    else:
        print(f"[Build package: {args.package}]")
        # subprocess.run(["colcon", "build", "--symlink-install",
        #                 "--packages-up-to", args.package])
        if args.debug:
            subprocess.run(["colcon", "build", "--symlink-install",
                            "--packages-up-to", args.package, "--cmake-args", "-DCMAKE_BUILD_TYPE=Debug"])
        else:
            subprocess.run(["colcon", "build", "--symlink-install",
                            "--packages-up-to", args.package, "--cmake-args", "-DCMAKE_BUILD_TYPE=Release"])

    os.chdir(orig_path)


if __name__ == "__main__":
    ros2_build()
