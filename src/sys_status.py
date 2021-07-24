import math
import platform
import psutil

class SystemStatus:
    def __init__(self) -> None:
        pass

    def get_system_stats(self):
        running_since = psutil.boot_time()
        
    def get_cpu_stats(self):
        cpu_usage = psutil.cpu_percent(percpu=True)

        max = math.max(cpu_usage)
        min = math.min(cpu_usage)
        avg = psutil.cpu_percent(percpu=False)
        report = f"Maximum cpu usage is at {max} percent, minimum at {min}, and avergave at {avg}"

        return report
    
    def get_memory_stats(self):
        mem_usage = psutil.virtual_memory()
        swap_usage = psutil.swap_memory()
        print(mem_usage)
    
    def get_disk_stats(self, partition):
        disk_usage = psutil.disk_usage(partition)
    
    def get_battery_stats(self):
        battery_level = psutil.sensors_battery()
        print(battery_level.percent)
    
    def get_sensors_stats(self):
        if (platform.system() != 'Darwin'):
            sensors = psutil.sensors_temperatures(fahrenheit=False)
            print(sensors)
        else:
            print('Not supported on M1 macs')