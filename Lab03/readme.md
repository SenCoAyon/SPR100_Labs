# 🔄 Lab03 - Process Management & Scheduling Analysis

**Course:** SsPR100 - Introduction to Computer Systems and Security  
**Lab Number:** Lab03  
**Weight:** 4% of final grade  
**Duration:** 3 hours (this lab lasts two weeks: 2 lab sessions) 
**Due Date:** See Blackboard for due date (11:59 PM before the start of the next lab session)

---

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. **Investigate process creation and lifecycle** using Linux system tools and commands
2. **Analyze process scheduling policies** and understand how the OS manages CPU time
3. **Examine multithreading concepts** through practical Python-based activities
4. **Identify security implications** of process management in Linux systems
5. **Apply process monitoring and analysis** techniques for system administration

---

## 📋 Pre-Lab Requirements

### Required Software
- **Ubuntu VM** from **Lab02B** (Must be completed first)
- **Python 3.x** (should already be installed on Ubuntu VM, if not, please search online how to install it using `apt`.)
- **Git** (for submission)

### Required Knowledge
- **Completion of Lab02B** (Linux Ubuntu VM Analysis) - **MANDATORY**
- Basic understanding of process concepts from lectures
- Familiarity with Linux command line
- Understanding of virtualization concepts from Lab02B

**Important:** 
- This lab builds directly on the Ubuntu VM environment you set up in Lab02B. Make sure Lab02B is completed before starting this lab.
- Whatever you document, please make sure you understand what they mean, don't just copy and paste without learning what they are -- they are going to appear again in your close-book tests and quizzes later. 
- 
---

## 🚀 Lab Activities

### Part 1: Process Creation and Lifecycle Analysis (60 minutes)

#### 1.1 Linux Process Management

**Use the same Ubuntu VM from Lab02B for all activities in this lab.**

1. **Process Information Commands Analysis:**
   
   **For each command below, document what it does and your specific observations:**
   
   ```bash
   # Command 1: Get all running processes
   ps aux
   ```
   - **What this command does:** Shows all processes run from commands
   - **Total process count:** wc is wordcount, printing newline, word and byte counts, but using -l only counts the newline, which co-incidentally is also all the processes, and it looks like it includes the titles
   - **Top 5 CPU users:** 
   1. 0.3 -bash 
   2. 0.3 tmux
   3. 0.3 sudo -i
   4. 0.1 [kworker/u4:1events_unbound]
   5. 0.0 everything else
     - Hint: You need to use the "Sort by" feature in `htop`, please find out how to use it. 
   - **Top 5 memory users:** 
   1. /usr/lib/snapd/snapd
   2. /sbin/multpathd -d -s
   3. /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
   4. /lib/systemd/systemd/systemd-journald
   5. /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
   
   ```bash
   # Command 2: Get process tree structure  
   pstree
   ```
   - **What this command does:** Shows all processes connected to systemd in a tree
   - **Root process observation:** ModemManager ---2*[{ModemManager}]
   - **Tree depth:** pstree in tmux is 6 branches deep
   - **Interesting parent-child relationships:** 
   login -> bash -> tmux:client
   systemd-timesyn -> {systemd-timesyn}
   tmux: server -> bash -> sudo -> sudo -> bash -> pstree
   Since I don't have a lot running, the highest trees are the terminal running tmux, tmux running bash inside with sudo permission and the recently run pstree, and then all the other systemd processes like time synchronization, network
         
   ```bash
   # Command 3: Current user processes
   ps -u $USER 
   ```
   - **What this command does:** Gives a simpler view all the processes that are running
   - **Your process count:** 
      - As regular user: In terms of tty1, only 2, but has 2 pts/0
      - As root: Only 1 tty1, but also has 1 tty2, 1 pts/0, and two 
   - **Resource usage:** Splitting two panes in tmux to cross-reference the two, systemd takes up the most memory, while htop and sometimes tmux would take up the most cpu.
   
   ```bash
   # Command 4: Bash process details
   ps -ef | grep -E "(PID|bash)"
   ```
   - **What this command does:** The pipe symbol allows use of another command in the same line. I personally used the pipe in the beginning of the course when making multiple directories at once (e.g. mkdir code | mkdir images | mkdir documents)

   grep is defined in --help as searching for patterns in each file. We usually use it to look in a file to find an exact phrase in OPS105 like (grep "^FallbackDNS=" /etc/systemd/resolved.conf) to output our "FallbackDNS= 1.1.1.1 8.8.8.8"
   - **Bash instances found:** 3 instances
   - **Bash process details:** 
      - ubuntu, 1548, -bash
      - root, 2020, -bash
      - root, 2050, -bash
   - **Your current bash:** My bash session should be the latest one, since we start as user ubuntu, then I did sudo -i, used tmux, then executed the command.

2. **Detailed Process Analysis with `htop`:**
   - Open terminal and type `htop`
   - If not installed: `sudo apt update && sudo apt install htop`
   
   **Step-by-step htop analysis:**
   
   a) **Initial htop Overview (first 2 minutes):**
      - **32 tasks, 32 threads** 
      - 0.7% CPU on core 1, 0.7% on core 2
      - 342M/3.79G Mem, 0K/3.79G
      - Uptime: 0:40:55 
      - **Top 5 processes by CPU usage** 
         - 2178, htop, 0.7%
         - 2160, tmux, 0.7%
         - 599, /usr/bin/vmtoolsd, 0.0-0.7%
         - 1 , /sbin/init, 0.0%
         - 490, /lib/systemd/systemd-journald, 0.0%
 
      - **Top 5 processes by memory usage** 
         - 1131,/usr/lib/snapd/snapd, 1.0
         - 1140,/usr/lib/snapd/snapd, 1.0
         - 1141,/usr/lib/snapd/snapd, 1.0
         - 1142,/usr/lib/snapd/snapd, 1.0
         - 1143,/usr/lib/snapd/snapd, 1.0
   
   b) **Process Tree Analysis (press F5 to enable tree mode):**
      - PID 1 is: /sbin/init, he 
      - For my current process in tmux, the bash shell is PID: 2163 and PPID: 2162, but the /bin/login -p -- -bash is PID: 2020 PPID: 2019
      - The parent process is the current bash I'm working in on tmux
      - **Snap daemon**
      Process /usr/lib/snapd/snapd with PID 1140 is child of /usr/lib/snapd/snapd with PPID 1  
      **Initial login shell**
      Process tmux with PID 2160 is child of -bash with PPID 2019  
      **Time synchronization**
      Process /lib/systemd/systemd-timesyncd with PID 585 is child of /lib/systemd/systemd-timesyncd with PPID 1  
      
   c) **Interactive Testing:**
      - Press **F4** to filter - Gives only commands with -bash in it
      - Press **F3** to search - Lets you find anything with systemd in it and cycle through what matches
      - Press **F6** to sort by memory (MEM%) - Still only 3 /usr/lib/snapd/snapd, but this time I know that the parent is at the top.
      - Press **F6** again to sort by CPU% - htop, /usr/bin/vmtoolsd, sudo -i OR tmux
      - Press **h** for help - Shift+H removes threads from Tasks, this kills the children

      I wish I knew about Shift+n/m/p/t early so I could change it to PID/Memory%/CPU%/Time+ respectively earlier
      - Press **F2** to play with some settings of `htop` - I thought we already needed to know this for the previous lab, I used this to add and remove PPID to the columns
   
   **Document all findings with specific numbers, process names, and PIDs in your report.**

3. **Process Creation Test:**
- Create a simple shell script
   ```bash
   nano test_process.sh
   ```
   
- Add this content to your `test_process.sh` file:

   ```bash
   #!/bin/bash
   echo "Hello from Process $$"
   echo "Parent PID: $PPID"
   sleep 20
   echo "Process $$ finishing"
   ```
- Make executable
   ```bash
   chmod +x test_process.sh
   ```   

- Run and observe process creation
   ```bash
   ./test_process.sh &
   ```
   - Think: what does this `&` mean in the end of the command above? Find out by searching online. (man bash | grep -A 'operator &' explains it but that is not a great explanation for me)
   - Find out what the different is between running the script using `./test_process.sh` and `sh test_process.sh`. 
      - ./ needs execution permission, sh is short for dash, which is the shell command interpreter, which gives a similar man page as "man bash", but just needs to be readable for a file

- Now check the background process before 20 seconds since you ran the last command. 
   ```bash
   ps -ef | grep test_process
   jobs
   ```

   - This gives the PID, PPID, Start time, and the command, as grep cuts down only for the "test_process" pattern, not showing the titles ps -ef would normally show.
---

### Part 2: Process Scheduling and Multithreading (60 minutes)

#### 2.1 Linux Process Scheduling Analysis

1. **Process Priority Management:**
   ```bash
   # Check current process priorities
   ps -eo pid,ppid,ni,comm
   
   # Start a process with different nice values
   nice -n 10 sleep 30 &
   nice -n -5 sleep 30 &
   
   # Check the priority differences
   ps -eo pid,ppid,ni,comm | grep sleep
   
   # Change process priority (`renice` command)
   # First, find a PID from above command
   renice 15 -p [PID_OF_SLEEP_PROCESS]
   ```
   - 129977 PID old priority -5, new priority 15, so this sets the nice value to 15. Doing it again gives old priority 15, new priority 15, so no change.

2. **Python Multithreading Analysis:**
   - Create/copy the python source file: `threading_analysis.py`:
   ```python
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
   ```

3. **Run and Monitor Threading:**
   ```bash
   # Terminal 1 （or Tmux Pane 1): Run the Python script
   python3 threading_analysis.py
   
   # Terminal 2 (or Tmux Pane 2): Monitor with htop while script runs
   htop
   
   # Terminal 3 (or Tmux Pane 3): Monitor specific process
   # Find the PID of python3 process and monitor it
   watch -n 1 "ps -p [PYTHON_PID] -o pid,ppid,pcpu,pmem,comm"
   ```
- If you are using Tmux to split your terminal as in Lab02B, a reference layout of your pane can  look like this, which is more convenient than opening multiple terminals:
   ![Tmux Layout](./thread-tmux.png)
- Using watch has a very limited time frame with the python process quickly finishing. It also takes up a very heavy load on htop, since it uses 4 different threads to use 96.3% of the cpu.


#### 2.2 Advanced Process Monitoring

1. **Process Monitoring Script:**
   - Create or copy the python source file: `process_monitor.py`
   ```python
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
   ```

2. **Install and Run Process Monitor:**
   ```bash
   # Install psutil if not installed
   sudo apt update
   sudo apt install python3-pip
   pip3 install psutil
   
   # Run the monitor
   python3 process_monitor.py
   
   # Let it run for 2-3 minutes while you do other activities
   # Press Ctrl+C to stop the python program
   ```

- Other than tmux having an odd jumbling of characters where it changes the time format from 18:18:36 to 18:18e41 and then and o and d after the time, a lot of processes are always switching hands for using the most CPU processes, changing between the active window processes like tmux, sudo -i, though not bash. The most common to appear was a "kworker/1:1-events", which is for kernel worker threads that do most of the processing for the kernel.
---

### Part 3: Security Implications and Process Analysis (60 minutes)

#### 3.1 Process Security Analysis

1. **Linux Process Security Features:**
   ```bash
   # Check process capabilities
   cat /proc/1238/status | grep Cap
   Is this a bunch of hexcode? 
   - **Cap Inh,CapAmb:** all 0  
   - **CapPrm/Eff/Bnd:** 000001ffffffffff  

   # Check process namespaces
   ls -la /proc/1238/ns/
   These have full permissions for read, write and execution

   # Check process limits
   cat /proc/1238/limits

   
   ```
   Process capabilities, defined as a measureable property of a process to specification. The "Cap"s all represent Inherited, Permitted, Effective, Bounding Set, Ambient. You can use capsh --decode=[result] to find what the caps included are, as it showed me cap_perfmon or cap_syslog

   Process namespaces have some of the things we see in htop, like process id, user and time. Red Hat gave more information on some like mnt -> Mount, where it's like two processes sharing content, but not everything, ipc -> Interprocess communication is very complicated and I don't have enough time before study week to read or understand all this. Cgroup controls how much CPU, RAM and block I/O a process can use, and is important to conceal information.

   Process limits is simple, showing how much resources it can use, like maximum cpu time, file size, processes, and gives soft limit, which is set and can be raised, hard limit is what is the actual limit set by a root user, and the unit of measurement for each maximum.

2. **Process Isolation Testing:**
   ```bash
   # Create a test user process
   sudo adduser testuser --disabled-password --gecos ""
   ```
- What does `adduser` command do? 
   ```bash
   # Switch to test user and run a process
   sudo -u testuser bash -c 'sleep 60 &'
   ```
- What does this command do?

   ```bash
   # Check process ownership and isolation
   ps -eo pid,user,comm | grep sleep
   
   # Try to access the process from another user (should fail)
   kill [TESTUSER_SLEEP_PID] 
   ```
- If you don't do it within the after "60 seconds, sleep" timer the process dies.
- It immediately kills the command, if you check with the same process ownership command right after doing it

#### 3.2 Process Security Monitoring

1. **Security-Focused Process Analysis:**
   ```bash
   # Monitor processes by security context
   ps -eo pid,user,comm,args | head -20
   
   # Check for suspicious processes
   ps aux | awk '$3 > 50.0 || $4 > 50.0' # High CPU/Memory processes
   
   # Monitor new process creation
   # Run this bash script in one terminal while doing activities in another
   while true; do 
       ps -eo pid,ppid,lstart,comm | tail -5
       sleep 2
   done
   ```
- This script monitors the bottom 5 commands of ps -eo, sorted by lowest number to highest, which is usually the newest commands executed.

2. **Process Permissions and Rights:**
   ```bash
   # Check current user processes
   ps -u $USER -o pid,comm,ni,pri
   
   # Check system processes
   sudo ps -u root -o pid,comm,ni,pri | head -10
   
   # Demonstrate privilege separation
   id  # Show current user ID
   sudo id  # Show root privileges when using sudo
   ```
- The first checks the nice and priority values of all processes for the current user. 
The second gives the top 10 processes of root, starting from PID 1 to higher amounts.  
The third gives user id, group id, the rest are supplementary group IDs. sudo id gives what power you have if you use sudo from a user account.

---

## 📝 Documentation Requirements

### Required Documentation Template

Create a comprehensive lab report using the following template structure:

```markdown
# Lab03 - Process Management & Scheduling Analysis Report

**Student Name:** Avery Yong  
**Student ID:** 059789115
**Course Section:** SPR100-NBB
**Completion Date:** 2025-10-16
**Lab Duration:** 5 hours, over Computing Commons computers and personal

---

## Part 1: Process Creation and Lifecycle Analysis

### 1.1 Linux Process Management Results

#### Process Information Commands Analysis

**Command 1: ps aux Analysis**
- **What this command does:** Shows all processes run from commands
- **Total process count:** wc is wordcount, printing newline, word and byte counts, but using -l only counts the newline, which co-incidentally is also all the processes, and it looks like it includes the titles
- **Top 5 CPU users:** 
   1. 0.3 -bash 
   2. 0.3 tmux
   3. 0.3 sudo -i
   4. 0.1 [kworker/u4:1events_unbound]
   5. 0.0 everything else
   I used htops F6 Sort By feature for the previous lab already to check the top CPU and MEM processes, and read about the nice feature, but too quickly dismissed it as a priority, completely forgetting that priority was right on top of it
- **Top 5 memory users:** 
   1. /usr/lib/snapd/snapd
   2. /sbin/multpathd -d -s
   3. /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
   4. /lib/systemd/systemd/systemd-journald
   5. /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers

**Command 2: pstree Analysis**
- **What this command does:** Shows all processes connected to systemd in a tree
- **Root process observation:** ModemManager ---2*[{ModeManager}]
- **Tree depth:** stree in tmux is 6 branches deep
- **Parent-child relationships:** 
   login -> bash -> tmux:client
   systemd-timesyn -> {systemd-timesyn}
   tmux: server -> bash -> sudo -> sudo -> bash -> pstree
   Since I don't have a lot running, the highest trees are the terminal running tmux, tmux running bash inside with sudo permission and the recently run pstree, and then all the other systemd processes like time synchronization, network

**Command 3: ps -u $USER Analysis**
- **What this command does:** Gives a simpler view all the processes that are running
- **Your process count:** 
      - As regular user: In terms of tty1, only 2, but has 2 pts/0
      - As root: Only 1 tty1, but also has 1 tty2, 1 pts/0, and tw
- **Resource usage:** Splitting two panes in tmux to cross-reference the two, systemd takes up the most memory, while htop and sometimes tmux would take up the most cpu.

**Command 4: ps -ef | grep -E "(PID|bash)" Analysis**
- **What this command does:** The pipe symbol allows use of another command in the same line. I personally used the pipe in the beginning of the course when making multiple directories at once (e.g. mkdir code | mkdir images | mkdir documents)

   grep is defined in --help as searching for patterns in each file. We usually use it to look in a file to find an exact phrase in OPS105 like (grep "^FallbackDNS=" /etc/systemd/resolved.conf) to output our "FallbackDNS= 1.1.1.1 8.8.8.8"
- **Bash instances found:** 3 instances
- **Bash process details:** 
      - ubuntu, 1548, -bash
      - root, 2020, -bash
      - root, 2050, -bash
- **Your current bash:** My bash session should be the latest one, since we start as user ubuntu, then I did sudo -i, used tmux, then executed the command.

#### htop Detailed Analysis Results

**a) Initial htop Overview:**
- **Total Number of Tasks:** - **32 tasks, 32 threads** 
- **CPU Usage per Core:** [List each core's usage percentage, e.g., Core 1: 15.2%, Core 2: 8.7%]
- **Total Memory Usage:** 342M/3.79G Mem 
- **Swap Usage:** 0K/3.79G
- **System Uptime:** - Time recorded: Uptime: 0:40:55 
- **Load Averages:** 0.02 / 0.01 / 0.00
- **Top 5 CPU Processes:** 
         - 2178, htop, 0.7%
         - 2160, tmux, 0.7%
         - 599, /usr/bin/vmtoolsd, 0.0-0.7%
         - 1 , /sbin/init, 0.0%
         - 490, /lib/systemd/systemd-journald, 0.0%
- **Top 5 Memory Processes:** 
   - 1131,/usr/lib/snapd/snapd, 1.0
   - 1140,/usr/lib/snapd/snapd, 1.0
   - 1141,/usr/lib/snapd/snapd, 1.0
   - 1142,/usr/lib/snapd/snapd, 1.0
   - 1143,/usr/lib/snapd/snapd, 1.0

**b) Process Tree Analysis (F5 tree mode):**
- **Init Process:** - PID 1 is: /sbin/init
- **Bash Shell Process:** - For my current process in tmux, the bash shell is PID: 2163 and PPID: 2162, but the /bin/login -p -- -bash is PID: 2020 PPID: 2019
- **Htop Process Parent:** - The parent process is the current bash I'm working in on tmux
- **System Process Relationships:** 
      **Snap daemon**
      Process /usr/lib/snapd/snapd with PID 1140 is child of /usr/lib/snapd/snapd with PPID 1  
      **Initial login shell**
      Process tmux with PID 2160 is child of -bash with PPID 2019  
      **Time synchronization**
      Process /lib/systemd/systemd-timesyncd with PID 585 is child of /lib/systemd/systemd-timesyncd with PPID 1 

**c) Interactive htop Testing Results:**
- **F4 Filter Test:** Gives only commands with -bash in it
- **F3 Search Test:** Lets you find anything with systemd in it and cycle through what matches
- **Top 3 Memory Users:** Still only 3 /usr/lib/snapd/snapd, but this time I know that the parent is at the top.
- **Top 3 CPU Users:** htop, /usr/bin/vmtoolsd, sudo -i OR tmux
- **F2 Settings:** I thought we already needed to know this for the previous lab, I used this to add and remove PPID to the columns, and then again right at the end where I ran out of space to read because my laptop resolution is too small
- **Additional Functions Explored:** 
   Shift+H removes threads from Tasks, this removes the children from sight

   I wish I knew about Shift+n/m/p/t early so I could change it to PID/Memory%/CPU%/Time+ respectively earlier

#### Process Creation Test Results
- **Script Content Created:** Line 1 gives process ID, Line 2 gives parent process ID, Line 3 kills the process after 20 seconds, Line 4 notates the process finishing
- **Script Process ID:** 2964
- **Parent Process:** 2561
- **Background Execution:** man bash | grep -5 'operator &' reads to me that it executes the command in it's own subshell, which then can't be interacted with if you don't press ctrl+c to early quit
- **Script Execution Difference:** - ./ needs execution permission, sh is short for dash, which is the shell command interpreter, which gives a similar man page as "man bash", but just needs to be readable for a file
- **Sleep Duration:** 20 seconds, as per line 3's "sleep 20"
- **Process Lifecycle:** [Describe from creation to termination - explain WHY these things happened]

# Process Creation Command Output:
root         2969    2561  0 00:59pts/0    00:00:00 grep --color=auto test_process

# Jobs Command Output:
root         2972    2561  0 00:59pts/0    00:00:00 grep --color=auto test_process

**Explanation of Findings:** This gives the PID, PPID, Start time, and the command, as grep cuts down only for the specific "test_process" pattern, not showing the titles ps -ef would normally show.

---

## Part 2: Process Scheduling and Multithreading

### 2.1 Linux Process Scheduling Analysis

#### Process Priority Management Results
- **Default Nice Values Observed:** -5 and 10
- **Priority Change Test:** Nice starts with -5 or 10 whichever number is given after -n, and renice does not add to it, but sets it to the given one.

# Priority Management Command Output:
129977 PID old priority -5, new priority 15

#### Python Multithreading Analysis
- **Main Process PID:** 1329
- **Number of Threads Created:** 4 threads, starting from 0 going up
- **Thread Creation Observation:** Other than it going too fast, that it consistently put down a > 90% CPU usage
- **CPU Utilization During Threading:** 96.3
- **Thread Execution Pattern:** 
Created Thread-0
Created Thread-1
Created Thread-2
Created Thread-3
Task Thread-0 started (PID: 1329)
Task Thread-1 started (PID: 1329)
Task Thread-2 started (PID: 1329)
Task Thread-3 started (PID: 1329)
Task Thread-1 completed
Task Thread-0 completed
Task Thread-2 completed
Task Thread-3 completed
All tasks completed
- These executed very quickly, so fast I often could not keep my htop on the right place to observe it. Normally it would complete the threads fully in order, but in the one screenshot I have, it did not. 

### 2.2 Advanced Process Monitoring Results

#### Process Monitor Script Output
- **Monitoring Duration:** 2.5 minutes approximately
- **Activities Performed:** Switched panes on tmux, made too many windows by accident

# Top Process Monitoring Results:
♦Snapshot at 18:18:36
Top 5 CPU -consuming processes:
1. PID:     1, Name: systemd        , CPU: 0.0%, Memory:    0.3%
2. PID:     2, Name: kthreadd       , CPU: 0.0%, Memory:    0.0%
3. PID:     3, Name: rcu_gp         , CPU: 0.0%, Memory:    0.0%
4. PID:     4, Name: rcu_gar_gp     , CPU: 0.0%, Memory:    0.0%
5. PID:     5, Name: slub_flushwq   , CPU: 0.0%, Memory:    0.0%

♦Snapshot at 18:18e41  ,  o     d  ,,
Top 5 CPU -consuming processes:
1. PID:  1238, Name: tmux           , CPU: 0.7%, Memory:    0.1%
2. PID:  1226, Name: sudo           , CPU: 0.0%, Memory:    0.1%
3. PID:     1, Name: kworker/1:1-events, CPU: 0.6%, Memory:    0.0%
4. PID:     4, Name: python3        , CPU: 0.7%, Memory:    0.1%
5. PID:     5, Name: systemd        , CPU: 0.0%, Memory:    0.3%

#### Performance Patterns Observed
- **CPU Usage Trends:** tmux and sudo would come up very often as expected, but there was also kworker/1:1-events, which I found is kernel worker threads that do most of the processing for the kernel. On weaker computers python3 will come up, Seneca computers did not, oddly.
- **Memory Usage Trends:** Stays mostly static as usual, but more often brings processes that actually have more than 0.0%
- **Process Behavior:** Tmux having an odd jumbling of characters where it changes the time format from 18:18:36 to 18:18e41 with an o and d always after when scrolling through

---

## Part 3: Security Implications and Process Analysis

### 3.1 Process Security Analysis Results

#### Linux Process Security Features
- **Process Capabilities:** Process capabilities, defined as a measureable property of a process to specification. The "Cap"s all represent Inherited, Permitted, Effective, Bounding Set, Ambient. You can use capsh --decode=[result] to find what the caps included are, as it showed me cap_perfmon or cap_syslog  
- **Process Namespaces:**  Process namespaces have some of the things we see in htop, like process id, user and time. Red Hat gave more information on some like mnt -> Mount, where it's like two processes sharing content, but not everything, ipc -> Interprocess communication is very complicated and I don't have enough time before study week to read or understand all this. Cgroup controls how much CPU, RAM and block I/O a process can use, and is important to conceal information.  
- **Process Limits:** Process limits is simple, showing how much resources it can use, like maximum cpu time, file size, processes, and gives soft limit, which is set and can be raised, hard limit is what is the actual limit set by a root user, and the unit of measurement for each maximum.  

# Process Security Command Output:
CapInh: 0000000000000000
CapPrm: 000001ffffffffff
CapEff: 000001ffffffffff
CapBnd: 000001ffffffffff
CapAmb: 0000000000000000

total 0
dr-x--x--x 2 root root 0 Oct 16 20:54 .
dr-xr-xr-x 9 root root 0 Oct 16 20:18 ..
lrwxrwxrwx 1 root root 0 Oct 16 20:54 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 ipc -> 'ipc:[4026531839]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 mnt -> 'mnt:[4026531841]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 net -> 'net:[4026531840]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 pid -> 'pid:[4026531836]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 pid_for_children -> 'pid:[4026531836]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 time -> 'time:[4026531834]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 time_for_children -> 'time:[4026531834]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 user -> 'user:[4026531837]'
lrwxrwxrwx 1 root root 0 Oct 16 20:54 uts -> 'uts:[4026531838]'

Limit                     Soft Limit           Hard Limit           Units
Max cpu time              unlimited            unlimited            seconds
Max file size             unlimited            unlimited            bytes
Max data size             unlimited            unlimited            bytes
Max stack size            8388608              unlimited            bytes
Max core file size        0                    unlimited            bytes
Max resident set          unlimited            unlimited            bytes
Max processes             15050                15050                processes
Max open files            1024                 1048576              files
Max locked memory         508006400            508006400            bytes
Max address space         unlimited            unlimited            bytes
Max file locks            unlimited            unlimited            locks
Max pending signals       15050                15050                signals
Max msgqueue size         819200               819200               bytes
Max nice priority         0                    0
Max realtime priority     0                    0
Max realtime timeout      unlimited            unlimited            us

#### Process Isolation Testing
- **Test User Creation:** Works with no issue as root. Ubuntu user it asks for password, then will say Adding user `testuser' ...
Adding new group `testuser' (1001) ...
Adding new user `testuser' (1001) with group `testuser' ...
Creating home directory `/home/testuser' ...
Copying files from `/etc/skel' ...
- **Process Ownership:** It shows testuser as the user, though being in a similar family as the shell in PID
- **Permission Denial Test:** I killed it with no resistance as root, otherwise as ubuntu user it would give me -bash: kill: (3216) - Operation not permitted
- **Isolation Effectiveness:** It isolates them well from regular, non root users, not allowing use and hiding the processes if not shared.

### 3.2 Process Security Monitoring Results

#### Security-Focused Analysis
- **High Resource Processes:** None if I wasn't running thread_analysis.py
- **Process Creation Monitoring:** All of the ones shown in this lab, with ps, sleep, and kworker/1:1
- **Privilege Separation:** A regular user is not allowed to interfere with other user's processes, but sudo/root has the power to do absolutely anything. root kills processes without obstacle.

# Security Monitoring Output:
"ps -u $USER -o pid,comm,ni,pri" checks the nice and priority values of all processes for the current user. 
"sudo ps -u root -o pid,comm,ni,pri | head -10" gives the top 10 processes of root, starting from PID 1 to higher amounts.  
"id" gives user id, group id, the rest are supplementary group IDs. "sudo id" gives what power you have if you use sudo from a user account.

---

## Analysis and Conclusions

### Key Findings
1. **Process Management:** Processes that aren't kernel and system running processes get created and die as soon as they are not needed, making for less platform for attack.
2. **Scheduling Behavior:** nice is how much CPU an app hogs per user, priority is how much CPU time it takes on the whole system
3. **Multithreading Impact:** Heavy CPU usage, so much so that it can exceed 100% of the output
4. **Security Features:** Reduce permissions and provisions so that it people won't mess with your processes, and especially so malfactors can't see if they gain access to certain users

### Technical Insights
- **Process Lifecycle Understanding:** Pretty efficient on minimal servers, doesn't heat up a computer, htop takes up a bit more than Windows, but doesn't take as much as time goes on
- **Scheduling Concepts:** nice sort of does mean how polite it is, the more it has, but it is user specified.
- **Multithreading Benefits:** Python can become very inefficient very quickly
- **Security Considerations:** sudo/root power is a little problematic

### Challenges and Solutions
- **Challenges Faced:** The passage of time and allowing the ubuntu installation to accept files from outside
- **Solutions Applied:** Google, with stackexchange, askubuntu and AI
- **Linux-Specific Learning:** A lot of these ps commands like ps -ef, ps -eo pid,user,comm as a snapshot version of htop so I don't have to watch htop constantly

### Understanding Questions
- **Process vs Thread:** Processes are usually the program or "eldest" parent over threads
- **Nice Values Impact:** The higher the nice value, the less CPU space it will take, the lower, the more it will take.
- **Security Isolation:** It will not allow interference by killing other user processes.

---

**Report Completion Time:** 6 hours  
**Confidence Level:** 7/10
**Questions for Instructor:** Should I get more used to being a regular user rather than having root power? Often for Mark's OPS105 class we speed up the process with sudo -i first, but it seems like we should remove super user access for reducing capability.
```




---

## 🔗 Additional Resources

### Linux Process Management Documentation
- [Linux Process Management](https://man7.org/linux/man-pages/man2/fork.2.html)
- [ps Command Manual](https://man7.org/linux/man-pages/man1/ps.1.html)
- [htop Documentation](https://htop.dev/)

### Python Threading Resources
- [Python Threading](https://docs.python.org/3/library/threading.html)
- [psutil Documentation](https://psutil.readthedocs.io/)

### Security Resources
- [Linux Security Features](https://www.kernel.org/doc/Documentation/security/)
- [Process Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)

---

## 📤 Submission Instructions

Please refer to the [readme.md](../readme.md) file of the Labs root directory for detailed submission instructions.

### What to Submit
1. **Complete Lab03 folder** with all required files
2. **README.md** with comprehensive documentation using the provided template
3. **Python scripts** (threading_analysis.py, process_monitor.py)

### Submission Process
1. Navigate to your lab folder:
   ```bash
   cd [YOUR_LAB_FOLDER]/SPR100_Labs/
   mkdir -p Lab03
   cd Lab03
   ```

2. Copy your lab report to the `Lab03` folder and then add all files:
   ```bash
   git add .
   ```

3. Commit with descriptive message:
   ```bash
   git commit -am "Complete Lab03 - Process Management & Scheduling Analysis"
   ```

4. Push to GitHub:
   ```bash
   git push
   ```

---