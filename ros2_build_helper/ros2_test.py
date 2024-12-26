#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

use_colorama = True
if use_colorama:
    from colorama import Back, Fore, Style, init
    init(autoreset=True)  # coloramaの初期化


def get_args():
    # get optional arguments
    # -w: workspace name
    # -p: package name
    # -t: build this package
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workspace", type=str,
                        help="Set workspace name (default: ros2_ws)")
    parser.add_argument("-p", "--package", type=str,
                        help="Set package name (if this and -t option are not set, build entire workspace)")
    parser.add_argument("-t", "--this", action="store_true",
                        help="Test this package (if this and -p option are not set, build entire workspace)")
    parser.add_argument("--show-result", action="store_true",
                        help="Show the result of the build")
    parser.add_argument("--show-result-verbose", action="store_true",
                        help="Show the result of the build")

    return parser.parse_args()


def ros2_test():
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

    if args.show_result_verbose:
        # Change directory to workspace
        os.chdir(ws_path)
        print(f"Show the result of the build (verbose)")
        # subprocess.run(["colcon", "test-result", "--all", "--verbose"])
        if use_colorama:
            popen = subprocess.Popen(["colcon", "test-result", "--all", "--verbose"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # 先頭が"   <<< failure message"という文字列のとき, その行を赤色で表示
            # それ以外の行はそのまま表示
            for line in popen.stdout:
                if line.startswith("  <<< failure message"):
                    print(Fore.RED + line, end="", flush=True)
                elif line.startswith("    Code style divergence in file"):
                    print(Fore.RED + line, end="", flush=True)
                elif line.startswith("    [  FAILED  ]"):
                    print(Fore.RED + line, end="", flush=True)
                else:
                    print(line, end="", flush=True)

            for line in popen.stderr:
                print(line, end="", flush=True)
        else:
            subprocess.run(["colcon", "test-result", "--all", "--verbose"])

        os.chdir(orig_path)
        exit(0)

    if args.show_result:
        print(f"Show the result of the build")
        # Change directory to workspace
        os.chdir(ws_path)
        # colcon test-result --all
        subprocess.run(["colcon", "test-result", "--all"])
        os.chdir(orig_path)
        exit(0)

    # Change directory to workspace
    os.chdir(ws_path)

    print(f"[Test Options: workspace={ws_name}, package={args.package}]")

    if use_colorama:
        popen = None

    # if package_name has value, build only the package
    if not args.package:
        print(f"[Test entire workspace: {ws_name}]")
        if use_colorama:
            # subprocess.runの標準出力をcoloramaで色付け
            popen = subprocess.Popen(["colcon", "test"],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            subprocess.run(["colcon", "test"])

    else:
        print(f"[Test package: {args.package}]")
        if use_colorama:
            popen = subprocess.Popen(["colcon", "test",
                                      "--packages-up-to", args.package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            subprocess.run(["colcon", "test",
                            "--packages-up-to", args.package])

    if use_colorama:
        # もしその行の先頭の文字列が"Starting >>>"という文字列であれば、その行を緑色で表示
        # "Finished <<<"という文字列であれば、その行を緑色で表示
        # それ以外の行はそのまま表示. 直前の行に色がついていても, 次の行には影響しないようにする
        for line in popen.stdout:
            if line.startswith("Starting >>>"):
                print(Fore.GREEN + line, end="", flush=True)
            elif line.startswith("Finished <<<"):
                print(Fore.GREEN + line, end="", flush=True)
            else:
                print(line, end="", flush=True)

        for line in popen.stderr:
            if line.startswith("--- stderr:"):
                print(Fore.RED + line, end="", flush=True)
            else:
                print(line, end="", flush=True)

    os.chdir(orig_path)


if __name__ == "__main__":
    ros2_test()
