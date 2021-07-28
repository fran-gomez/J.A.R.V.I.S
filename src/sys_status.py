import platform
import psutil

class SystemStatus:
    def __init__(self) -> None:
        pass

    def get_system_stats(self):
        running_since = psutil.boot_time()

        report = f"System running since {running_since}"

        return report
        
    def get_cpu_stats(self):
        cpu_usage = psutil.cpu_percent(percpu=True)

        max_usage = max(cpu_usage)
        min_usage = min(cpu_usage)
        avg = psutil.cpu_percent(percpu=False)
        report = f"Maximum core usage is at {max_usage} percent, minimum at {min_usage}, and avergave at {avg} percent"

        return report
    
    def get_memory_stats(self):
        mem_usage = psutil.virtual_memory()
        swap_usage = psutil.swap_memory()

        report = f"Memory is at {mem_usage.percent} percent, and swap is at {swap_usage.percent}"

        return report
    
    def get_disk_stats(self, partition = '/'):
        disk_usage = psutil.disk_usage(partition)

        report = f"Partition {partition} uses {disk_usage.percent} percent of disk size"

        return report
    
    def get_battery_stats(self):
        battery_level = psutil.sensors_battery()
        
        report = f"Battery is at {battery_level.percent} percent"

        return report
    
    def get_sensors_stats(self):
        if (platform.system() != 'Darwin'):
            sensors = psutil.sensors_temperatures(fahrenheit=False)
            report = f"{sensors}"
        else:
            report = "Sensors not suported on M1 macs"
        
        return report

stats = SystemStatus()
print(stats.get_cpu_stats())
print(stats.get_memory_stats())
print(stats.get_disk_stats('/Library'))
print(stats.get_battery_stats())
print(stats.get_sensors_stats())