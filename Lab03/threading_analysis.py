import threading
import time
import os

def cpu_intensive_task(name, duration):
    """Simulate CPU-intensive work"""
    print(f"Task {name} started (PID: {os.getpid()})")
    start_time = time.time()
    while time.time() - start_time < duration:
        # CPU-intensive calculation
        result = sum(i**2 for i in range(1000))
    print(f"Task {name} completed")

def main():
    print(f"Main process PID: {os.getpid()}")
    
    # Create multiple threads
    threads = []
    for i in range(4):
        thread = threading.Thread(
            target=cpu_intensive_task, 
            args=(f"Thread-{i}", 8)
        )
        threads.append(thread)
        print(f"Created Thread-{i}")
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("All tasks completed")

if __name__ == "__main__":
    main()