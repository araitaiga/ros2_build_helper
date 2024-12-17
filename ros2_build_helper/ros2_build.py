import os
import sys
import argparse
import subprocess
from colorama import init, Fore, Back, Style


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
                        help="Build this package (if this and -p option are not set, build entire workspace)")
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

    init(autoreset=True)  # coloramaの初期化
    # if package_name has value, build only the package
    if not args.package:
        print(f"[Build entire workspace: {ws_name}]")
        subprocess.run(["colcon", "build", "--symlink-install"])

        # # subprocess.runの標準出力をcoloramaで色付け
        # p = subprocess.Popen(["colcon", "build", "--symlink-install"],
        #                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # # もしその行の先頭の文字列が"Starting >>>"という文字列であれば、その行を緑色で表示
        # # "Finished <<<"という文字列であれば、その行を緑色で表示
        # # それ以外の行はそのまま表示. 直前の行に色がついていても, 次の行には影響しないようにする
        # for line in p.stdout:
        #     if line.startswith("Starting >>>"):
        #         print(Fore.GREEN + line, end="", flush=True)
        #     elif line.startswith("Finished <<<"):
        #         print(Fore.GREEN + line, end="", flush=True)
        #     else:
        #         print(line, end="", flush=True)

        # for line in p.stderr:

        #     elif line.startswith("--- stderr:"):
        #         print(Fore.RED + line, end="", flush=True)
        #     else:
        #         print(line, end="", flush=True)

    else:
        print(f"[Build package: {args.package}]")
        subprocess.run(["colcon", "build", "--symlink-install",
                        "--packages-up-to", args.package])

        # p = subprocess.Popen(["colcon", "build", "--symlink-install",
        #                       "--packages-up-to", args.package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # for line in p.stdout:
        #     if line.startswith("Starting >>>"):
        #         print(Fore.GREEN + line, end="", flush=True)
        #     elif line.startswith("Finished <<<"):
        #         print(Fore.GREEN + line, end="", flush=True)
        #     else:
        #         print(line, end="", flush=True)

        # for line in p.stderr:
        #     if line.startswith("--- stderr:"):
        #         print(Fore.RED + line, end="", flush=True)
        #     else:
        #         print(line, end="", flush=True)

    os.chdir(orig_path)


if __name__ == "__main__":
    ros2_build()