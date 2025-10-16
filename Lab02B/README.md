
# Lab02B - Linux Ubuntu VM CPU and Memory Analysis Report

**Student Name:** Avery Yong
**Student ID:** 059789115
**Course Section:** SPR100NBB
**Completion Date:** 2025/09/26
**Lab Duration:** 3 hours, 30 mins

---

## Part 1: Ubuntu VM Setup and Configuration

### 1.1 VM Configuration Summary
- **Hypervisor:** VMware Workstation Pro
- **Version:** 17.6.4
- **CPU Cores:** 2
- **Memory:** 4 GB
- **Storage:** 40 GB
- **Network:** Network Address Translation

### 1.2 VM Installation and Startup Process
- **Ubuntu ISO Source:** \\mydrive\courses\SPR100\Ubuntu-L2\Ubuntu22.0.4.ova
- **Installation Method:** Open a virtual machine and imported onto  
- **Startup Time:** 5 seconds
- **User Account Created:** ubuntu
- **Initial VM State:** Seems fine?

---

## Part 2: Linux System Analysis

### 2.1 CPU Analysis Results

#### System Information Commands
- **Processor Information:** 
processor       : 0  
vendor_id       : GenuineIntel  
cpu family      : 6  
model           : 151  
model name      : 12th Gen Intel(R) Core(TM) i7-12700  
stepping        : 2  
microcode       : 0x37  
cpu MHz         : 2112.004  
cache size      : 25600 KB  
physical id     : 0  
siblings        : 2  
core id         : 0  
cpu cores       : 2  
apicid          : 0  
initial apicid  : 0  
fpu             : yes  
fpu_exception   : yes  
cpuid level     : 32  
wp              : yes  
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves arat umip pku ospke gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear flush_l1d arch_capabilities  
bugs            : spectre_v1 spectre_v2 spec_store_bypass swapgs itlb_multihit eibrs_pbrsb  
bogomips        : 4224.00  
clflush size    : 64  
cache_alignment : 64  
address sizes   : 45 bits physical, 48 bits virtual  
power management:  
processor       : 1  
vendor_id       : GenuineIntel  
cpu family      : 6  
model           : 151  
model name      : 12th Gen Intel(R) Core(TM) i7-12700  
stepping        : 2  
microcode       : 0x37  
cpu MHz         : 2112.004  
cache size      : 25600 KB  
physical id     : 0  
siblings        : 2  
core id         : 1  
cpu cores       : 2  
apicid          : 1  
initial apicid  : 1  
fpu             : yes  
fpu_exception   : yes  
cpuid level     : 32  
wp              : yes  
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves arat umip pku ospke gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear flush_l1d arch_capabilities  
bugs            : spectre_v1 spectre_v2 spec_store_bypass swapgs itlb_multihit eibrs_pbrsb  
bogomips        : 4224.00  
clflush size    : 64  
cache_alignment : 64  
address sizes   : 45 bits physical, 48 bits virtual  
power management:
- **Architecture:** x86_64
- **Number of Cores:** 2
- **CPU Model Name:** model name    : 12th Gen Intel(R) Core(TM) i7-12700
- **CPU Frequency:** cpu MHz    : 2112.000

#### htop CPU Analysis
- **Current CPU Usage:** 0.7%
- **Number of CPU Cores Visible:** 2
- **CPU Utilization Pattern:** Without doing anything, the utilization is very low.
- **Process CPU Usage:** 
-- /usr/bin/vmtools
-- /usr/bin/htop
-- /systemd | /sbin/init
-- /lib/systemd/systemd-journald
-- /sbin/multipathd -d -s

#### Linux Command Outputs
    # Processor Information Command Output:
Architecture:                       x86_64
CPU op-mode(s):                     32-bit, 64-bit
Address sizes:                      45 bits physical, 48 bits virtual
Byte Order:                         Little Endian
CPU(s):                             2
On-line CPU(s) list:                0,1
Vendor ID:                          GenuineIntel
Model name:                         12th Gen Intel(R) Core(TM) i7-12700
CPU family:                         6
Model:                              151
Thread(s) per core:                 1
Core(s) per socket:                 2
Socket(s):                          1
Stepping:                           2
BogoMIPS:                           4224.00
Flags:                              fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves arat umip pku ospke gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear flush_l1d arch_capabilities
Hypervisor vendor:                  VMware
Virtualization type:                full
L1d cache:                          96 KiB (2 instances)
L1i cache:                          64 KiB (2 instances)
L2 cache:                           2.5 MiB (2 instances)
L3 cache:                           25 MiB (1 instance)
NUMA node(s):                       1
NUMA node0 CPU(s):                  0,1
Vulnerability Gather data sampling: Not affected
Vulnerability Itlb multihit:        KVM: Mitigation: VMX unsupported
Vulnerability L1tf:                 Not affected
Vulnerability Mds:                  Not affected
Vulnerability Meltdown:             Not affected
Vulnerability Mmio stale data:      Not affected
Vulnerability Retbleed:             Not affected
Vulnerability Spec store bypass:    Mitigation; Speculative Store Bypass disabled via prctl and seccomp
Vulnerability Spectre v1:           Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:           Mitigation; Enhanced IBRS, IBPB conditional, RSB filling, PBRSB-eIBRS SW sequence
Vulnerability Srbds:                Not affected
Vulnerability Tsx async abort:      Not affected

    # CPU Performance Output:
    %Cpu(s): 0.0 us 0.0 sy, 0.0 ni,100.0 id, 0.0 wa, 0.0 hi, 0.0 si, 0.0 st

### 2.2 Memory Analysis Results

#### System Information Memory Details
- **Total Physical Memory:** 3.8 Gigabytes
- **Available Physical Memory:** 3.2 Gigabytes
- **Memory Usage Pattern:** These are much larger in use than CPU, but do not change without closing programs or tasks.
- **Buffer and Cache Information:** 
--MemTotal:     3969535 kB
--MemFree:      3343364 kB
--MemAvailable: 3435059 kB

#### Linux Memory Commands Output
    # Memory Information:
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       291Mi       3.2Gi       1.0Mi       324Mi       3.3Gi
Swap:          3.8Gi          0B       3.8Gi

    # Memory Performance:
MemTotal:        3969532 kB
MemFree:         3337628 kB
MemAvailable:    3432220 kB

### 2.3 System Performance Monitoring Results

#### Performance Monitoring Script
- **Monitoring Duration:** [2 minutes]
- **Sample Interval:** [5 seconds]
- **CPU Usage Range:** 0.0% - 3.1%
- **Memory Usage Range:** 7.5% - 7.6%
- **Performance Patterns Observed:** While left completely idle, memory usage does not change. If I switch to a different text terminal with Alt+RightArrow and open htop, it changed the memory usage by 0.1%

#### htop Resource Monitor Observations
- **Peak CPU Usage:** 8.0%
- **Peak Memory Usage:** 0.9%
- **Resource Usage During Activities:** I decided to install ninvaders to have something that might take up more CPU. Originally the peak usage was around 1.3%, but eventually struck a max of 8.0% when I was actively playing ninvaders.

---

## Part 3: Security and Virtualization Analysis

### 3.1 Linux Security Features Status
- **AppArmor Status:** apparmor module is loaded
- **UFW Firewall Status:** Status: inactive
- **UFW Rules Summary:** 
-- There are no rules set, nor do I know how to set them yet.
-- Defaults are:
---deny (incoming)
---allow (outgoing)
---disabled (routed)
- **System Updates Status:** Since I did sudo apt update and sudo apt upgrade, ufw is at version 0.36.1. Copyright states it is from 2008-2021, so I would hazard a guess it is deprecated. After a quick google search, it is not, but it is meant for people who don't know how to set firewalls up.

### 3.2 VM Isolation Test Results

#### File System Isolation
- **Test File Created:** test.txt in /home/ubuntu/
- **Host System Check:** No
- **Isolation Effectiveness:** The kernel is isolated from the host OS, and all the files that are in the VM 

#### Process Isolation
- **VM Processes Observed:**
-- -bash
-- python3
-- systemd
- **Host Processes Visible:** Nothing from Windows
- **Isolation Observations:** Process separation from the host is important, so it doesn't interfere or have any chance of intruding on the memory for host processes.

### 3.3 Performance Observation Results

#### CPU Performance Comparison
- **VM CPU Usage:** 0.7% at idle on htop
- **Host CPU Usage:** 23% on average on resmon.exe
- **Performance Differences:** Big difference is my familiarity with Linux versus my familiarity with Windows, where I have much more of "my basics" open with Windows, having  multiple tabs of a web browser open, music, and Android VM for games. For Linux, I don't know what to open for daily use, other than internet browser tabs for reading up on documentation, or the currently limited knowledge of bash scripting.

#### Memory Performance Test
- **Applications Opened:** (Ninvaders, bc, Nano, Vim) in 4 panes of the same window on tmux
- **Initial Memory Usage:** 192MB/3.82GB
- **Final Memory Usage:** 184MB/3.82GB
- **Memory Behavior Observations:** It actually only went up to 193MB upon opening Ninvaders and the "bc" calculator, but then I opened vimtutor and it became 188MB, then finally opening nano it dipped to 184MB. Upon closing them all however, they stayed at 184MB, until I reopened htop, and it returned to 196MB. 

---

## Analysis and Conclusions

### Key Findings
1. **CPU Performance:** Other than the lab computers are pretty strong, Linux minimal runs like lightning in comparison to Windows. It also appears to use much less resources, but I should not be surprised when without a graphical user interface.
2. **Memory Performance:** Seems like more of the lower level programs take up a little bit more memory than Windows, but they may be more efficient if the system runs faster.
3. **Virtualization Overhead:** Does not destroy my laptop in comparison to Windows 10, uses a fraction of CPU and memory.
4. **Security Features:** Separated from the host application memory, so there is no unauthorized use between the two.

### Technical Insights
- **Linux System Understanding:** CPU and memory usage is much lower, has lower spikes in use and idle time.
- **Virtualization Concepts:** That the VM kernel is what is separated from the host, managed by the hypervisor.
- **Performance Monitoring:** They are a bit more simple and modern, as the usage is mainly measured in megabytes to gigabytes, appear to be made for monitoring larger work processes.

### Challenges and Solutions
- **Challenges Faced:** Suddenly had an init error, saying that it was missing or not in the expected place, causing a kernel panic error.  Also did not know what I was doing with the uncomplicated firewall or hisham's top.
- **Solutions Applied:** Made a new ubuntu vm the next day. Tried to understand what the init error was, but I did not have time to fix this issue before this lab was due. I may try to fix it when I can manage school workload better.  I looked up the man file for ufw, along with some google searching of more information of ufw and htop, to find information on the names and usage.
- **Lessons Learned:** Just always have a clean snapshot, iso or ova file, in case I break the vm somehow. 

---

**Report Completion Time:** 4h  
**Confidence Level:** 6/10
**Questions for Instructor:** Why'd we use minimal instead of with GUI? Performance and resources with GUI look similar to windows, but opening Firefox completely uses both CPUs.
