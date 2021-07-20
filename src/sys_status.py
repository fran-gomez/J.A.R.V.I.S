import psutil

class SystemStatus:
    def __init__(self) -> None:
        pass

    def get_system_stats(self):
        cpu_usage = psutil.cpu_percent(percpu=True)
        mem_usage = psutil.virtual_memory()
        swap_usage = psutil.swap_memory()
        disk_usage = psutil.disk_usage()
        running_since = psutil.boot_time()
        battery_level = psutil.sensors_battery()
        # sensors = psutil.sensors_temperatures(fahrenheit=False)

        print(cpu_usage)
        print(battery_level.percent)
        # print(sensors)

sys = SystemStatus()
sys.get_system_stats()