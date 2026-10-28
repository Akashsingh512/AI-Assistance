import psutil

class SystemMonitor:
    @staticmethod
    def get_cpu_usage() -> float:
        return psutil.cpu_percent(interval=0.1)

    @staticmethod
    def get_ram_usage() -> dict:
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used
        }

    @staticmethod
    def get_disk_usage(path="/") -> dict:
        disk = psutil.disk_usage(path)
        return {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        }

    @staticmethod
    def get_battery_status() -> dict:
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged
                }
        return {"percent": "N/A", "power_plugged": "N/A"}

    @staticmethod
    def get_running_processes(limit=10) -> list:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        # Sort by CPU usage
        processes = sorted(processes, key=lambda p: p['cpu_percent'] or 0.0, reverse=True)
        return processes[:limit]
