import psutil
import time
from datetime import datetime

def monitor_processes():
    print(f"🔍 Process Monitor Started at {datetime.now()}")
    print("-" * 60)
    
    try:
        while True:
            print(f"\n📊 Snapshot at {datetime.now().strftime('%H:%M:%S')}")
            print("Top 5 CPU-consuming processes:")
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
            
            for i, proc in enumerate(top_processes, 1):
                print(f"{i}. PID: {proc['pid']:>6}, Name: {proc['name']:<15}, "
                      f"CPU: {proc['cpu_percent']:>5.1f}%, Memory: {proc['memory_percent']:>5.1f}%")
            
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")

if __name__ == "__main__":
    monitor_processes()