"""
System Control — System Management & Automation
===============================================
Controls volume, system status monitoring, process management,
and system power actions (shutdown, restart, lock).
"""

import os
import sys
import subprocess
import psutil
import pyautogui


def get_system_stats():
    """Retrieve current system CPU, RAM, Disk, and Battery metrics."""
    try:
        cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery()

        battery_info = {
            "percent": battery.percent if battery else "N/A",
            "plugged": battery.power_plugged if battery else False,
        }

        return {
            "cpu_percent": cpu_usage,
            "ram_percent": memory.percent,
            "ram_used_gb": round(memory.used / (1024 ** 3), 2),
            "ram_total_gb": round(memory.total / (1024 ** 3), 2),
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024 ** 3), 2),
            "battery": battery_info,
        }
    except Exception as e:
        print(f"[Error reading system stats] {e}")
        return {
            "cpu_percent": 0,
            "ram_percent": 0,
            "ram_used_gb": 0,
            "ram_total_gb": 0,
            "disk_percent": 0,
            "disk_free_gb": 0,
            "battery": {"percent": "N/A", "plugged": False},
        }


def get_running_processes(limit=15):
    """Retrieve list of top running processes sorted by RAM usage."""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                processes.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "cpu": round(info['cpu_percent'] or 0, 1),
                    "memory": round(info['memory_percent'] or 0, 1),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        processes.sort(key=lambda x: x['memory'], reverse=True)
        return processes[:limit]
    except Exception as e:
        print(f"[Error listing processes] {e}")
        return []


def take_screenshot(filename="screenshot.png"):
    """Capture screen screenshot."""
    try:
        from bujji.config import OUTPUT_DIR
        filepath = OUTPUT_DIR / filename
        shot = pyautogui.screenshot()
        shot.save(filepath)
        return str(filepath)
    except Exception as e:
        print(f"[Screenshot Error] {e}")
        return None


def lock_screen():
    """Lock the workstation."""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.LockWorkStation()


def system_action(action):
    """Trigger system action: shutdown, restart, sleep, lock."""
    action = action.lower()
    if action == "lock":
        lock_screen()
        return "Workstation locked."
    elif action == "shutdown":
        if sys.platform == "win32":
            os.system("shutdown /s /t 10")
            return "System shutting down in 10 seconds."
    elif action == "restart":
        if sys.platform == "win32":
            os.system("shutdown /r /t 10")
            return "System restarting in 10 seconds."
    return "Action not supported on this platform."
