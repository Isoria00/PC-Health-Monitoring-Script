import psutil
import platform
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import subprocess


def get_size(bytes, suffix="B"):
    """Scale bytes to KB, MB, GB, TB"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_cpu_name():
    try:
        result = subprocess.check_output("wmic cpu get name", shell=True).decode().split("\n")[1].strip()
        return result if result else platform.processor()
    except:
        return platform.processor()


def get_gpu_name():
    try:
        result = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode().split("\n")[1].strip()
        return result if result else "Unknown GPU"
    except:
        return "Unknown GPU"


def get_ram_info():
    try:
        total_ram = psutil.virtual_memory().total
        result = subprocess.check_output("wmic memorychip get manufacturer, capacity", shell=True).decode().split("\n")
        manufacturer = "Unknown"
        for line in result:
            if line.strip() and "Manufacturer" not in line:
                manufacturer = line.split()[0]
                break
        return f"{manufacturer} - {get_size(total_ram)}"
    except:
        return f"{get_size(psutil.virtual_memory().total)}"


def get_disk_info():
    try:
        result = subprocess.check_output("wmic diskdrive get model", shell=True).decode().split("\n")[1].strip()
        return result if result else "Unknown Disk"
    except:
        return "Unknown Disk"


class PCHealthMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Health Monitor")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        style = ttk.Style(root)
        style.theme_use("clam")

        self.main_frame = ttk.Frame(root, padding=15)
        self.main_frame.pack(fill="both", expand=True)

        self.create_system_info_section()
        self.create_performance_section()
        self.update_info()

    def create_system_info_section(self):
        sys_frame = ttk.LabelFrame(self.main_frame, text="System Information", padding=10)
        sys_frame.pack(fill="x", pady=5)

        uname = platform.uname()
        self.sys_labels = {
            "System": uname.system,
            "Machine": uname.machine,
            "Processor": get_cpu_name(),
            "GPU": get_gpu_name(),
            "RAM": get_ram_info(),
            "Disk": get_disk_info(),
            "Release": uname.release,
            "Version": uname.version,
            "Node Name": uname.node
        }

        for i, (key, value) in enumerate(self.sys_labels.items()):
            ttk.Label(sys_frame, text=f"{key}:", font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2)
            ttk.Label(sys_frame, text=value, font=("Segoe UI", 10)).grid(row=i, column=1, sticky="w", pady=2)

    def create_performance_section(self):
        perf_frame = ttk.LabelFrame(self.main_frame, text="Performance", padding=10)
        perf_frame.pack(fill="x", pady=5)

        self.cpu_label = ttk.Label(perf_frame, text="CPU Usage:")
        self.cpu_label.grid(row=0, column=0, sticky="w")
        self.cpu_bar = ttk.Progressbar(perf_frame, length=300, maximum=100)
        self.cpu_bar.grid(row=0, column=1, padx=10)

        self.ram_label = ttk.Label(perf_frame, text="RAM Usage:")
        self.ram_label.grid(row=1, column=0, sticky="w")
        self.ram_bar = ttk.Progressbar(perf_frame, length=300, maximum=100)
        self.ram_bar.grid(row=1, column=1, padx=10)

        self.disk_label = ttk.Label(perf_frame, text="Disk Usage:")
        self.disk_label.grid(row=2, column=0, sticky="w")
        self.disk_bar = ttk.Progressbar(perf_frame, length=300, maximum=100)
        self.disk_bar.grid(row=2, column=1, padx=10)

        self.last_updated = ttk.Label(perf_frame, text="")
        self.last_updated.grid(row=3, column=0, columnspan=2, pady=5)

    def colorize_bar(self, bar, value):
        style = ttk.Style()
        if value < 50:
            style.configure("green.Horizontal.TProgressbar", troughcolor='white', background='green')
            bar.configure(style="green.Horizontal.TProgressbar")
        elif value < 80:
            style.configure("yellow.Horizontal.TProgressbar", troughcolor='white', background='orange')
            bar.configure(style="yellow.Horizontal.TProgressbar")
        else:
            style.configure("red.Horizontal.TProgressbar", troughcolor='white', background='red')
            bar.configure(style="red.Horizontal.TProgressbar")

    def update_info(self):
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        self.cpu_bar["value"] = cpu_usage
        self.colorize_bar(self.cpu_bar, cpu_usage)

        self.ram_bar["value"] = ram.percent
        self.colorize_bar(self.ram_bar, ram.percent)

        self.disk_bar["value"] = disk.percent
        self.colorize_bar(self.disk_bar, disk.percent)

        self.last_updated.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

        self.root.after(1000, self.update_info)


def main():
    root = tk.Tk()
    app = PCHealthMonitor(root)
    root.mainloop()


if __name__ == "__main__":
    main()

