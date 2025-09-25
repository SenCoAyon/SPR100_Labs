# Lab02A - Windows VM CPU and Memory Analysis Report
**Student Name:** Avery Yong
**Student ID:** 059789115
**Course Section:** SPR100NBB
**Completion Date:** 2025/09/22
**Lab Duration:** 3h30m
---
## Part 1: Virtual Machine Setup and Configuration
### 1.1 VM Configuration Summary
- **Hypervisor Name:** VMware Workstation Pro 
- **Hypervisor Version:** 17
- **CPU Cores:** 2
- **Memory:** 4 GB
- **Storage:** 60 GB
- **Network:** Network Address Translation
### 1.2 VM Import and Startup Process
- **VM File Source:** \\mydrive\courses\SPR100\Win10
- **Import Method:** Added it with "Open a Virtual Machine" on VMWare
- **VM Name:** win10-ayong2
- **Storage Path:** E:\Virtual Machines\Win10
- **Startup Time:** 49 seconds
### 1.3 Initial System Configuration
- **Password Change Process:** Windows key, type in "pass" and click "Change your password", verify current password, changed password, confirm and double check after restarting.
- **Git Installation:** I did the "winget install Git.git" function, confirmed with Y, stalled at 10%, button press continued it, press yes to allow git to install, complete installion.
---
## Part 2: Windows System Analysis
### 2.1 CPU Analysis Results
#### System Information (msinfo32)
- **Processor Name:** 12th Gen Intel(R) Core i7-12700
- **Number of Cores:** 2 Cores
- **Logical Processors:** 2 Logical Processors
#### Task Manager CPU Analysis
- **Current CPU Utilization:** 16%
- **Number of Virtual Processors:** (2 Cores x 2 Logical Processors) = 4
- **CPU Base Speed:** 2.11 GHz
- **CPU Current Speed:** 2.11GHz
- **System Up Time:** 0:38:00
- **CPU Utilization Observations:** With a text edit it would stay low in process use, but watching a youtube video would use a lot of processing power, jumping up from 16% to 39%.
### 2.2 Memory Analysis Results
#### System Information Memory Details
- **Total Physical Memory:** 4.00 GB
- **Available Physical Memory:** 594 MB
- **Total Virtual Memory:** 5.37 GB
- **Available Virtual Memory:** 1.12 GB
- **Virtual Memory Explanation:** Virtual memory means the memory that is used from the hard drive when the RAM does not have enough space, which explains why so little of the physical is available
#### PowerShell Memory Commands Output
**Physical Memory Information:**__GENUS              : 2  
__CLASS              :   Win32_PhysicalMemory  
__SUPERCLASS         : CIM_PhysicalMemory  
__DYNASTY            : CIM_ManagedSystemElement  
__RELPATH            : Win32_PhysicalMemory.Tag="Physical Memory 0"  
__PROPERTY_COUNT     : 36  
__DERIVATION         : {CIM_PhysicalMemory, CIM_Chip, CIM_PhysicalComponent, CIM_PhysicalElement...}  
__SERVER             : DESKTOP-4H9E4CT  
__NAMESPACE          : root\cimv2  
__PATH               : \\DESKTOP-4H9E4CT\root\cimv2:Win32_PhysicalMemory.Tag="Physical Memory 0"  
Attributes           : 0  
BankLabel            : RAM slot #0  
Capacity             : 2147483648  
Caption              : Physical Memory  
ConfiguredClockSpeed : 4800  
ConfiguredVoltage    :  
CreationClassName    : Win32_PhysicalMemory  
DataWidth            : 64  
Description          : Physical Memory  
DeviceLocator        : RAM slot #0  
FormFactor           : 8  
HotSwappable         :  
InstallDate          :  
InterleaveDataDepth  :  
InterleavePosition   :  
Manufacturer         : VMware Virtual RAM  
MaxVoltage           :  
MemoryType           : 2  
MinVoltage           :  
Model                :  
Name                 : Physical Memory  
OtherIdentifyingInfo :  
PartNumber           : VMW-2048MB  
PositionInRow        :  
PoweredOn            :  
Removable            :  
Replaceable          :  
SerialNumber         : 00000001  
SKU                  :  
SMBIOSMemoryType     : 3  
Speed                :  
Status               :  
Tag                  : Physical Memory 0  
TotalWidth           : 64  
TypeDetail           : 128  
Version              :  
PSComputerName       : DESKTOP-4H9E4CT  
- **Document:**   
**__PATH**: \DESKTOP-4H9E4CT\root\cimv2:Win32_PhysicalMemory.Tag="Physical Memory 0"   
**Capacity**: 2147483648

**Available Memory Information:**  
Timestamp 2025-09-25 11:28:43 AM

CounterSamples \\desktop-4h9e4ct\memory\available mbytes : 483
- **Available Memory:** 483
### 2.3 System Performance Monitoring Results
#### Performance Monitor Data Collector Set
- **Data Collector Set Name:** Lab02A_Performance_Monitoring
- **Sample Interval:** 5 seconds
- **Duration:** 2 minutes
- **Counters Monitored:**
- Processor: % Processor Time
- Memory: Available MBytes
- Physical Disk: % Disk Time
- **Log Location:** C:\Users\Student\Documents
#### Performance Data Summary
- **CPU Usage Range:** 15% - 100%
- **Memory Available Range:** 52 - 360 MB
- **Disk Usage Range:** 0% - 21%
- **Performance Patterns Observed:** Noticeable spikes when opening youtube and other programs.
#### Resource Monitor Observations
- **Peak CPU Usage:** 96%
- **Peak Memory Usage:** 1112 KB/sec and 39% Highest active time
- **Resource Usage During Activities:** Opened youtube on Firefox and Chrome which spiked the usage for about 3 seconds, then returned to nominal levels.
#### Performance Monitor Data Collector Graph
[image]
- **How You Extracted:** Put picture into Seneca OneDrive.
---
## Analysis and Conclusions
### Key Findings
1. **VM Configuration:** Horrible, seneca computing common computers broke in the middle of working on the Lab and lost 30 minutes of work. Windows10 is hard to run on laptops or any weaker computers. Also very difficult to open on deprecated hypervisors. Configuring the system was simple enough though, installing git.
2. **CPU Performance:** The computing commons has a way better processor than my home PC. Mine has 6 cores, while the commons have 12.
3. **Memory Management:** Virtual memory is what the hard drive or SSD utilizes with pagefile.sys, while physical memory is how much the host has in hardware. Removing use of pagefile.sys may have broken my computer.
4. **Performance Monitoring:** When opening any computer applications, it will spike the usage for a moment, but regulate very quickly. Memory on the other hand will be in use while the programs are running. Also that it is much faster to find it on start than using "windows + r, perfmon"

### Technical Insights
- **System Architecture Understanding:** I'm not sure I learned anything about memory hierarchy, but I know now CPU cores and logical processors can be managed to be used specifically for the VM.
- **Virtualization Concepts:** That sometimes if you do not allocate enough it will not run the machine properly, if at all.
- **Performance Monitoring Tools:** That there are way too many monitoring parameters.
- **PowerShell Commands:** Gives much simpler information, but harder to remember the commands.
### Challenges and Solutions
- **VM Setup Challenges:** Way too many. Current home computers available are unable to run, main PC is broken, so I only have a Windows 7 PC with a lot of processing power, but VirtualBox v5 is not capable of running anything, not even ubuntu.
- **Performance Monitoring Issues:** Had an enormous recording gap when attempting to run on a laptop.
- **File Transfer Challenges:** Seneca OneDrive.
- **Solutions Applied:** Seneca computer commons to have a sufficiently strong computer. SSD solves most of the install issues, usually.
- **Lessons Learned:** Pray to IT God that the computer I'm working on does not suddenly die, and use notepad with constant saving instead of vscode.dev OR just straight put it onto the github
### Understanding Questions
- **Virtual Memory Concept:** Modern applications take up way too much memory, so using HDD or SSD space to compensate for RAM space can keep your computer running smoothly. 
- **VM Resource Allocation:** Sometimes it completely disables usage of computer if you haven't given it enough. Of course, more resources is better, but 
- **Performance Monitoring Value:** Monitoring resources can give a hint to if there is a bitcoin miner in your system, or to give clues if resources are not properly allocated.
---
**Report Completion Time:** Likely 6 hours spread over 3 days
**Confidence Level:** 8?