#!/usr/bin/env python3
"""System information gathering skill."""

import argparse
import json
import os
import platform
import shutil


def get_os_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "hostname": platform.node(),
        "python": platform.python_version(),
    }


def get_cpu_info():
    cpu_count = os.cpu_count() or 0
    info = {
        "processor": platform.processor() or "unknown",
        "cores": cpu_count,
    }

    # Try to get load average (Unix only)
    try:
        load = os.getloadavg()
        info["load_avg_1m"] = round(load[0], 2)
        info["load_avg_5m"] = round(load[1], 2)
        info["load_avg_15m"] = round(load[2], 2)
    except (OSError, AttributeError):
        pass

    return info


def get_memory_info():
    """Get memory info using /proc/meminfo on Linux or vm_stat on macOS."""
    info = {}

    if platform.system() == "Linux":
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        info["total_kb"] = int(line.split()[1])
                    elif line.startswith("MemAvailable:"):
                        info["available_kb"] = int(line.split()[1])
                    elif line.startswith("MemFree:"):
                        info["free_kb"] = int(line.split()[1])

            if "total_kb" in info:
                total_gb = info["total_kb"] / 1024 / 1024
                info["total_gb"] = round(total_gb, 1)
            if "available_kb" in info and "total_kb" in info:
                used = info["total_kb"] - info["available_kb"]
                info["used_percent"] = round(used / info["total_kb"] * 100, 1)
        except FileNotFoundError:
            info["error"] = "/proc/meminfo not available"
    elif platform.system() == "Darwin":
        try:
            import subprocess
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, check=True
            )
            total_bytes = int(result.stdout.strip())
            info["total_gb"] = round(total_bytes / 1024 / 1024 / 1024, 1)
        except (subprocess.CalledProcessError, ValueError):
            pass

    return info


def get_disk_info():
    usage = shutil.disk_usage("/")
    return {
        "total_gb": round(usage.total / 1024 / 1024 / 1024, 1),
        "used_gb": round(usage.used / 1024 / 1024 / 1024, 1),
        "free_gb": round(usage.free / 1024 / 1024 / 1024, 1),
        "used_percent": round(usage.used / usage.total * 100, 1),
    }


def get_network_info():
    """Basic network info from hostname."""
    import socket
    info = {"hostname": socket.gethostname()}
    try:
        info["ip"] = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        info["ip"] = "unknown"
    return info


SECTIONS = {
    "os": ("Operating System", get_os_info),
    "cpu": ("CPU", get_cpu_info),
    "memory": ("Memory", get_memory_info),
    "disk": ("Disk", get_disk_info),
    "network": ("Network", get_network_info),
}


def format_section(title, data):
    lines = [f"## {title}", ""]
    for key, value in data.items():
        label = key.replace("_", " ").title()
        lines.append(f"- **{label}**: {value}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Gather system information")
    parser.add_argument(
        "--section",
        choices=list(SECTIONS.keys()) + ["all"],
        default="all",
        help="Which section to display",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    args = parser.parse_args()

    sections = list(SECTIONS.keys()) if args.section == "all" else [args.section]
    result = {}

    for section in sections:
        title, fn = SECTIONS[section]
        result[section] = fn()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("# System Information\n")
        for section in sections:
            title, _ = SECTIONS[section]
            print(format_section(title, result[section]))


if __name__ == "__main__":
    main()
