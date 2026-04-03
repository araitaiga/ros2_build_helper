#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

from colorama import Fore, init

init(autoreset=True)

FAILURE_PREFIXES = (
    "  <<< failure message",
    "    Code style divergence in file",
    "    [  FAILED  ]",
)

PROGRESS_PREFIXES = (
    "Starting >>>",
    "Finished <<<",
)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--workspace", type=str, help="Set workspace name (default: ros2_ws)"
    )
    parser.add_argument(
        "-p",
        "--package",
        type=str,
        help="Set package name (if this and -t option are not set, test entire workspace)",
    )
    parser.add_argument(
        "-t",
        "--this",
        action="store_true",
        help="Test this package (if this and -p option are not set, test entire workspace)",
    )
    parser.add_argument(
        "--show-result-verbose",
        action="store_true",
        help="Show the result of the test",
    )
    parser.add_argument(
        "--console-direct",
        action="store_true",
        help="Use console_direct event handler for colcon test",
    )
    parser.add_argument(
        "-j", "--jobs", type=int, help="Number of parallel jobs for test"
    )
    parser.add_argument(
        "--delete", action="store_true", help="Delete all test result files"
    )
    return parser.parse_args()


def run_with_color(cmd: list[str], color_rules: dict[str, str]) -> None:
    """コマンドを実行し、プレフィックスに応じて色付きで出力する。

    color_rules: {"stdout" | "stderr": 出力ストリーム名} に対し、
    各行のプレフィックスに応じた色を適用する。
    """
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    for line in popen.stdout:
        color = color_rules.get(
            next((p for p in color_rules if line.startswith(p)), None)
        )
        if color:
            print(color + line, end="", flush=True)
        else:
            print(line, end="", flush=True)

    for line in popen.stderr:
        color = color_rules.get(
            next((p for p in color_rules if line.startswith(p)), None)
        )
        if color:
            print(color + line, end="", flush=True)
        else:
            print(line, end="", flush=True)

    popen.wait()


def ros2_test():
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

    if args.delete:
        print("Deleting all test result files...")
        subprocess.run(["colcon", "test-result", "--all", "--delete"])
        os.chdir(orig_path)
        sys.exit(0)

    if args.show_result_verbose:
        print("Show the result of the test (verbose)")
        rules = {p: Fore.RED for p in FAILURE_PREFIXES}
        run_with_color(["colcon", "test-result", "--all", "--verbose"], rules)
        os.chdir(orig_path)
        sys.exit(0)

    cmd = ["colcon", "test"]
    if package:
        cmd += ["--packages-up-to", package]
        print(f"[Test package: {package} in {ws_name}]")
    else:
        print(f"[Test entire workspace: {ws_name}]")

    if args.jobs:
        cmd += ["--parallel-workers", str(args.jobs)]
    if args.console_direct:
        cmd += ["--event-handler", "console_direct+"]

    rules = {**{p: Fore.GREEN for p in PROGRESS_PREFIXES}, "--- stderr:": Fore.RED}
    run_with_color(cmd, rules)

    os.chdir(orig_path)


if __name__ == "__main__":
    ros2_test()
