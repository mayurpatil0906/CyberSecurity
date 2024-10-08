import psutil
import time

# Monitor CPU, Memory, Disk Usage
def monitor_system():
    print("CPU Usage: ", psutil.cpu_percent(interval=1), "%")
    print("Memory Usage: ", psutil.virtual_memory().percent, "%")
    print("Disk Usage: ", psutil.disk_usage('/').percent, "%")
    print("Network Stats: ", psutil.net_io_counters())
    print("------------------------------------------------")

# Function to list all processes
def list_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        print(proc.info)

# Monitoring for suspicious behavior (high CPU usage, abnormal network activity)
def detect_suspicious_process():
    suspicious_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        if proc.info['cpu_percent'] > 80 or proc.info['memory_percent'] > 50:
            suspicious_processes.append(proc.info)
    return suspicious_processes

# Monitor suspicious processes
def monitor_suspicious_activity():
    while True:
        suspicious = detect_suspicious_process()
        if suspicious:
            print("Suspicious Process Detected:")
            for proc in suspicious:
                print(proc)
        time.sleep(5)

    
monitor_suspicious_activity()
# Real-time monitoring
while True:
    monitor_system()
    time.sleep(2)
