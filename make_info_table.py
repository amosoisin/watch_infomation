from datetime import datetime
import time
import sys
import psutil
import csv
import os


OUTPUT_FILE = "data/infomation.csv"

if (not os.path.exists(OUTPUT_FILE)):
    index = [
        "time",
        "cpu_percent_1",
        "cpu_percent_2",
        "cpu_percent_3",
        "cpu_percent_4",
        "memory_used",
        "memory_free",
        "memory_percent",
        "disk_used",
        "disk_free",
        "disk_percent",
        "cpu_temp",
    ]
    with open(OUTPUT_FILE, "a") as f:
        writer = csv.writer(f)
        writer.writerow(index)

while True:
    try:
        now_ts = int(datetime.now().timestamp())
        cpu_percent = psutil.cpu_percent(percpu=True)
        cpu_temp = psutil.sensors_temperatures()['cpu-thermal'][0]
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(path="/")

        info = [
            now_ts,
            cpu_percent[0],
            cpu_percent[1],
            cpu_percent[2],
            cpu_percent[3],
            memory.used,
            memory.available,
            memory.percent,
            disk.used,
            disk.free,
            disk.percent,
            cpu_temp.current
        ]

        with open(OUTPUT_FILE, "a") as f:
            writer = csv.writer(f)
            writer.writerow(info)

        time.sleep(1)
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt")
        sys.exit()
