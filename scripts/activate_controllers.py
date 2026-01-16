#!/usr/bin/env python3
"""
Utility script to check and activate controllers for all arms.
Usage: python3 activate_controllers.py
"""

import subprocess
import sys
from typing import Dict


def _run(cmd, timeout=10):
    """Run subprocess and return result."""
    return subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=timeout)


def _controllers_state(arm_name: str) -> Dict[str, str]:
    """Return controller -> state for an arm."""
    res = _run([
        "ros2", "control", "list_controllers",
        "-c", f"/{arm_name}/controller_manager",
    ])
    state = {}
    for line in res.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            ctrl, status = parts[0], parts[1]
            state[ctrl] = status
    return state


def check_all_controllers():
    """Check and report all arm controllers."""
    print("\n=== Checking controller states ===")
    arms = ["arm1", "arm2", "arm3", "arm4"]
    inactive_controllers = {}

    for arm in arms:
        print(f"\n{arm}:")
        state = _controllers_state(arm)
        needed = ["joint_state_broadcaster", "arm_controller"]
        for ctrl in needed:
            st = state.get(ctrl, "missing")
            status = "✓" if st == "active" else "✗"
            print(f"  {status} {ctrl}: {st}")
            if st != "active":
                if arm not in inactive_controllers:
                    inactive_controllers[arm] = []
                inactive_controllers[arm].append(ctrl)

    return inactive_controllers


def activate_inactive_controllers(inactive_controllers: Dict[str, list]):
    """Activate all inactive controllers."""
    if not inactive_controllers:
        print("\n✓ All controllers already active!")
        return

    print("\n=== Activating inactive controllers ===")
    for arm, ctrls in inactive_controllers.items():
        print(f"\nActivating {arm}: {', '.join(ctrls)}")
        
        # Try to load missing ones
        for ctrl in ctrls:
            res = _run([
                "ros2", "control", "load_controller", "--set-state", "active",
                ctrl, "-c", f"/{arm}/controller_manager",
            ])
            if res.returncode != 0:
                print(f"  ⚠ Could not load {ctrl}: {res.stderr[:100]}")
        
        # Attempt to activate both
        res = _run([
            "ros2", "control", "switch_controllers",
            "--activate", "arm_controller", "joint_state_broadcaster",
            "-c", f"/{arm}/controller_manager",
        ])
        if res.returncode == 0:
            print(f"  ✓ Activated controllers for {arm}")
        else:
            print(f"  ✗ Failed to activate: {res.stderr[:100]}")

    # Final check
    print("\n=== Final controller states ===")
    check_all_controllers()


def main():
    print("Checking and activating controllers for all arms...")
    inactive = check_all_controllers()
    if inactive:
        activate_inactive_controllers(inactive)
    print("\n✓ Controller activation complete!")


if __name__ == "__main__":
    main()
