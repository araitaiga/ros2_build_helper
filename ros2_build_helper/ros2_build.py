#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--workspace", type=str, help="Set workspace name (default: ros2_ws)"
    )
    parser.add_argument(
        "-p",
        "--package",
        type=str,
        help="Set package name (if this and -t option are not set, build entire workspace)",
    )
    parser.add_argument(
        "-t",
        "--this",
        action="store_true",
        help="Build this package (if this and -p option are not set, build entire workspace)",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Build with Debug option"
    )
    parser.add_argument(
        "-j", "--jobs", type=int, help="Number of parallel jobs for build"
    )
    return parser.parse_args()


def build_command(package: str | None, debug: bool, jobs: int | None) -> list[str]:
    build_type = "Debug" if debug else "Release"
    cmd = [
        "colcon",
        "build",
        "--symlink-install",
    ]
    if package:
        cmd += ["--packages-up-to", package]
    cmd += [
        "--cmake-args",
        f"-DCMAKE_BUILD_TYPE={build_type}",
        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
    ]
    if jobs:
        cmd += [f"--parallel-workers", str(jobs)]
    return cmd


def ros2_build():
    orig_path = os.getcwd()

    if not os.environ.get("ROS2_ROOT_WS"):
        os.environ["ROS2_ROOT_WS"] = os.environ["HOME"]

    args = get_args()

    ws_name = args.workspace or "ros2_ws"
    ws_path = os.path.join(os.environ["ROS2_ROOT_WS"], ws_name)

    package = args.package
    if args.this:
        package = os.path.basename(os.getcwd())
        print(f"Set this package {package}")

    os.chdir(ws_path)

    if package:
        print(f"[Build package: {package} in {ws_name}]")
    else:
        print(f"[Build entire workspace: {ws_name}]")

    subprocess.run(build_command(package, args.debug, args.jobs))

    os.chdir(orig_path)


if __name__ == "__main__":
    ros2_build()
