# Lab06 - Network Traffic Analysis with tshark (Wireshark CLI)

**Student Name:** Avery Yong
**Student ID:** 059789115
**Course Section:** SPR100NBB
**Date:** 2025-11-20  
**VM Interface Used:** ens33
**tshark Version:** TShark (Wireshark) 3.6.2 (Git v3.6.2 packaged as 3.6.2-2)

Copyright 1998-2022 Gerald Combs <gerald@wireshark.org> and contributors.
License GPLv2+: GNU GPL version 2 or later <https://www.gnu.org/licenses/gpl-2.0.html>
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Compiled (64-bit) using GCC 11.2.0, with libpcap, with POSIX capabilities
(Linux), with libnl 3, with GLib 2.71.2, with zlib 1.2.11, with Lua 5.2.4, with
GnuTLS 3.7.3 and PKCS #11 support, with Gcrypt 1.9.4, with MIT Kerberos, with
MaxMind DB resolver, with nghttp2 1.43.0, with brotli, with LZ4, with Zstandard,
with Snappy, with libxml2 2.9.12, with libsmi 0.4.8.

Running on Linux 5.15.0-161-generic, with Intel(R) Core(TM) i5-3320M CPU @
2.60GHz (with SSE4.2), with 3875 MB of physical memory, with GLib 2.72.4, with
zlib 1.2.11, with libpcap 1.10.1 (with TPACKET_V3), with c-ares 1.18.1, with
GnuTLS 3.7.3, with Gcrypt 1.9.4, with nghttp2 1.43.0, with brotli 1.0.9, with
LZ4 1.9.3, with Zstandard 1.4.8, with libsmi 0.4.8, with LC_TYPE=en_US.UTF-8,
binary plugins supported (0 loaded).

---

## 0) Workspace and Environment

### Workspace Path
```
$ pwd
/home/ubuntu/SPR100_Labs/Lab06
```

### Interfaces and Permissions
```
$ tshark -D
1. ens33
2. ens34
3. any
4. lo (Loopback)
5. bluetooth-monitor
6. nflog
7. nfqueue
8. dbus-system
9. dbus-session
10. ciscodump (Cisco remote capture)
11. dpauxmon (DisplayPort AUX channel monitor capture)
12. randpkt (Random packet generator)
13. sdjournal (systemd Journal Export)
14. sshdump (SSH remote capture)
15. udpdump (UDP Listener remote capture)

$ groups
With "getent groups | tail -3" I get:
fsuser:x:1003:
ayong2:x:1004:ayong2
wireshark:x:119:root,ayong2
```

### Notes
- I accidentally did not allow non-superuser to be able to capture packets, so I added myself as part of the wireshark group with "adduser ayong2 wireshark" instead as root, as the usermod command wouldn't work at first.

- Other questions for personal note:
	- running as root will tell you it "could be dangerous" because it would have permission to everything, which if compromised by malware it could get in through the network traffic
	- newgrp makes a new group but is a more common built-in over addgroup/groupadd
	- pinging google.com while watching loopback shows DNS 99 Standard query and 137 Standard query response 

---

## Part 1: Install and Explore tshark

### Commands and Outputs
```
$ tshark -v
TShark (Wireshark) 3.6.2 (Git v3.6.2 packaged as 3.6.2-2)

Copyright 1998-2022 Gerald Combs <gerald@wireshark.org> and contributors.
License GPLv2+: GNU GPL version 2 or later <https://www.gnu.org/licenses/gpl-2.0.html>
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Compiled (64-bit) using GCC 11.2.0, with libpcap, with POSIX capabilities
(Linux), with libnl 3, with GLib 2.71.2, with zlib 1.2.11, with Lua 5.2.4, with
GnuTLS 3.7.3 and PKCS #11 support, with Gcrypt 1.9.4, with MIT Kerberos, with
MaxMind DB resolver, with nghttp2 1.43.0, with brotli, with LZ4, with Zstandard,
with Snappy, with libxml2 2.9.12, with libsmi 0.4.8.

Running on Linux 5.15.0-161-generic, with Intel(R) Core(TM) i5-3320M CPU @
2.60GHz (with SSE4.2), with 3875 MB of physical memory, with GLib 2.72.4, with
zlib 1.2.11, with libpcap 1.10.1 (with TPACKET_V3), with c-ares 1.18.1, with
GnuTLS 3.7.3, with Gcrypt 1.9.4, with nghttp2 1.43.0, with brotli 1.0.9, with
LZ4 1.9.3, with Zstandard 1.4.8, with libsmi 0.4.8, with LC_TYPE=en_US.UTF-8,
binary plugins supported (0 loaded).

$ tshark -D
1. ens33
2. ens34
3. any
4. lo (Loopback)
5. bluetooth-monitor
6. nflog
7. nfqueue
8. dbus-system
9. dbus-session
10. ciscodump (Cisco remote capture)
11. dpauxmon (DisplayPort AUX channel monitor capture)
12. randpkt (Random packet generator)
13. sdjournal (systemd Journal Export)
14. sshdump (SSH remote capture)
15. udpdump (UDP Listener remote capture)

# 10-second capture (replace interface name if different)
$ tshark -i eth0 -a duration:10 -w lab06_basic.pcapng
Capturing on 'ens33'
** (tshark:2837) 05:07:37.169174 [Main MESSAGE] -- Capture started.
** (tshark:2837) 05:07:37.169385 [Main MESSAGE] -- File: "lab06_basic.pcapng"
63

$ tshark -r lab06_basic.pcapng -q -z io,stat,1
=============================
| IO Statistics             |
|                           |
| Duration: 7.795424 secs   |
| Interval: 1 secs          |
|                           |
| Col 1: Frames and bytes   |
|---------------------------|
|          |1               |
| Interval | Frames | Bytes |
|---------------------------|
|  0 <> 1  |      6 |   640 |
|  1 <> 2  |      5 |   484 |
|  2 <> 3  |     17 |  1486 |
|  3 <> 4  |      4 |   402 |
|  4 <> 5  |      4 |   402 |
|  5 <> 6  |      4 |   402 |
|  6 <> 7  |      4 |   402 |
|  7 <> Dur|      4 |   402 |
=============================

$ tshark -i any -f "udp port 53" -a duration:8 -w lab06_dns_only.pcapng
Capturing on 'any'
** (tshark:1448) 18:52:55.854389 [Main MESSAGE] -- Capture started.                                                  
 ** (tshark:1448) 18:52:55.854544 [Main MESSAGE] -- File: "lab06_dns_only.pcapng"                                     
26 

$ tshark -r lab06_basic.pcapng -Y "http"
(No output)

$ tshark -r lab06_basic.pcapng \
  -T fields -E header=y -E separator=, \
  -e frame.number -e frame.time_relative -e _ws.col.Protocol \
  -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport \
  > lab06_basic_fields.csv
1,0.000000000,SSH,192.168.92.1,192.168.92.130,58383,22,,
2,0.001064682,SSH,192.168.92.130,192.168.92.1,22,58383,,
3,0.052808978,TCP,192.168.92.1,192.168.92.130,58383,22,,
4,0.662667159,SSH,192.168.92.1,192.168.92.130,58383,22,,
5,0.663840735,SSH,192.168.92.130,192.168.92.1,22,58383,,
```

### Analysis
- [Which interface(s) are active and why?]
	- My interfaces are ens33 for the NAT, ens34 for an internal network that I added because I wanted to try to connect it to my OPS105 gateway to practice, and loopback so that we can test connections without using another machine
- [Explain capture vs display filters in your own words.]
	- A capture filter filters the traffic WHILE capturing
	- A display filter filters traffic ALREADY captured, but it remains on the file
- [How did you distinguish TCP vs UDP in the CSV fields?]
	- Since I decided to SSH onto my VM, I clogged the capture with SSH and TCP.
	- UDP would only come up if I used DNS, as that is the only thing I know that works with UDP that I can use that isn't video games

---

## Part 2: Recognize TCP vs UDP Across Concurrent Activities

### Activities Performed
```
# In separate terminals or sequentially during capture window:
$ ping -c 6 1.1.1.1
$ dig +short senecapolytechnic.ca
$ curl -s -o /dev/null -w "%{http_code}\n" http://example.com
$ dig A www.google.com
```

### Capture and Protocol Identification
```
$ tshark -i eth0 -a duration:20 -w lab06_multi.pcapng
Capturing on 'ens33'
** (tshark:2013) 20:13:13:733647 [Main MESSAGE] -- Capture started.
** (tshark:2013) 20:13:13:733677 [Main MESSAGE] -- File: "lab06_multi.pcapng"

# ICMP
$ tshark -r lab06_multi.pcapng -Y "icmp" -T fields -e frame.number -e ip.src -e ip.dst | head
22      192.168.208.128 1.1.1.1
23      1.1.1.1 192.168.208.128
24      192.168.208.128 1.1.1.1
25      1.1.1.1 192.168.208.128
26      192.168.208.128 1.1.1.1
27      1.1.1.1 192.168.208.128
28      192.168.208.128 1.1.1.1
29      1.1.1.1 192.168.208.128
30      192.168.208.128 1.1.1.1
31      1.1.1.1 192.168.208.128
# DNS
$ tshark -r lab06_multi.pcapng -Y "dns" -T fields -e frame.number -e ip.src -e ip.dst -e dns.qry.name | head
1       192.168.208.128 192.168.208.2   example.com
2       192.168.208.128 192.168.208.2   example.com
5       192.168.208.2   192.168.208.128 example.com
6       192.168.208.2   192.168.208.128 example.com
18      192.168.208.128 192.168.208.2   senecapolytechnic.ca
19      192.168.208.2   192.168.208.128 senecapolytechnic.ca

# HTTP (if present)
$ tshark -r lab06_multi.pcapng -Y "http" -T fields -e frame.number -e ip.src -e ip.dst -e http.request.method -e http.host | head
10      192.168.208.128 23.215.0.136    GET     example.com
12      23.215.0.136    192.168.208.128
```

### Stats and Conversations
```
$ tshark -r lab06_multi.pcapng -q -z io,stat,1,"COUNT(tcp) TCP","COUNT(udp) UDP","COUNT(icmp) ICMP","COUNT(dns) DNS"
============================================
| IO Statistics                            |
|                                          |
| Duration: 11.231565 secs                 |
| Interval:  1 secs                        |
|                                          |
| Col 1: COUNT(tcp) tcp                    |
|     2: COUNT(udp) udp                    |
|     3: COUNT(icmp) icmp                  |
|     4: COUNT(dns) dns                    |
|------------------------------------------|
|          |1      |2      |3      |4      |
| Interval | COUNT | COUNT | COUNT | COUNT |
|------------------------------------------|
|  0 <>  1 |    11 |     4 |     0 |     4 |
|  1 <>  2 |     0 |     0 |     0 |     0 |
|  2 <>  3 |     0 |     0 |     0 |     0 |
|  3 <>  4 |     0 |     0 |     0 |     0 |
|  4 <>  5 |     0 |     2 |     0 |     2 |
|  5 <>  6 |     0 |     0 |     0 |     0 |
|  6 <>  7 |     0 |     0 |     2 |     0 |
|  7 <>  8 |     0 |     0 |     2 |     0 |
|  8 <>  9 |     0 |     0 |     2 |     0 |
|  9 <> 10 |     0 |     0 |     2 |     0 |
| 10 <> 11 |     0 |     0 |     2 |     0 |
| 11 <> Dur|     0 |     0 |     2 |     0 |
============================================ 
Why'd the count drop 2

$ tshark -r lab06_multi.pcapng -q -z conv,tcp -z conv,udp

afp,srt
     ancp,tree
     ansi_a,bsmap
     ansi_a,dtap
     ansi_map
     asap,stat
     bacapp_instanceid,tree
     bacapp_ip,tree
     bacapp_objectid,tree
     bacapp_service,tree
     calcappprotocol,stat
     camel,counter
     camel,srt
```

### Exported Dataset
```
$ tshark -r lab06_multi.pcapng \
  -T fields -E header=y -E separator=, \
  -e frame.time_relative -e _ws.col.Protocol -e ip.src -e ip.dst \
  -e tcp.flags -e tcp.len -e udp.length -e dns.qry.name \
  > lab06_part2.csv

0.000000000,DNS,192.168.208.128,192.168.208.2,,,48,example.com
0.000158422,DNS,192.168.208.128,192.168.208.2,,,48,example.com
0.014416557,ARP,,,,,,
0.014427915,ARP,,,,,,
0.014602382,DNS,192.168.208.2,192.168.208.128,,,216,example.com
0.014602599,DNS,192.168.208.2,192.168.208.128,,,144,example.com
0.015148355,TCP,192.168.208.128,23.215.0.136,0x0002,0,,
0.042364661,TCP,23.215.0.136,192.168.208.128,0x0012,0,,
0.042405406,TCP,192.168.208.128,23.215.0.136,0x0010,0,,
0.042463049,HTTP,192.168.208.128,23.215.0.136,0x0018,75,,
```

### Analysis
- [Which activities produced ICMP vs UDP vs TCP?]
	- ICMP was made from pinging 1.1.1.1, though that appeared later in my file
	- UDP should be from pinging senecapolytechnic.ca and DNS resolving the name with ARP
	- TCP from pinging example.com
- [How did you determine client vs server roles from ports/IPs?]
	- The client (ens33) was 192.168.208.128 when pinging will send out a request to 1.1.1.1, or when it pinged 192.168.208.2 the DNS server to resolve the name of example.com.
- [What did the io,stat counts and conversations reveal about traffic patterns?]
	- Other than it may have dropped some packets on the analysis, I found that TCP and ICMP is fairly loud, takes up a lot of traffic from making SYN ACK, or if you have an SSH connection, it will make a lot of traffic on both TCP and SSH itself.
---

## Part 3: Security-Focused Analysis (Scan Pattern and TLS Metadata)

### SYN Pattern on Loopback
```
# Generate localhost connection attempts
$ for p in 22 80 443 8000 8080 53; do (echo > /dev/tcp/127.0.0.1/$p) >/dev/null 2>&1 || true; done

# Capture and analyze
$ tshark -i lo -a duration:10 -w lab06_security_lo.pcapng
$ tshark -r lab06_security_lo.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" \
  -T fields -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport | sort -n | head -20
0.000000000     127.0.0.1       127.0.0.1       22
0.000747467     127.0.0.1       127.0.0.1       80
0.001383835     127.0.0.1       127.0.0.1       443
0.001944529     127.0.0.1       127.0.0.1       8000
0.002497920     127.0.0.1       127.0.0.1       8080
0.003043228     127.0.0.1       127.0.0.1       53
```

### TLS Metadata (SNI/Version)
```
$ curl -s https://example.com >/dev/null
$ tshark -i any -a duration:8 -w lab06_tls.pcapng
$ tshark -r lab06_tls.pcapng -Y "tls.handshake.extensions_server_name" \
  -T fields -e frame.time_relative -e ip.dst -e tls.handshake.extensions_server_name -e tls.record.version | head
0.831692288     23.215.0.136    example.com     0x0301```

### Analysis
- [Explain why SYN without ACK can indicate scanning.]
	- SYN will check if the port is listening, but has no interest or intention to establish a connection, so it may just be checking what ports are open which could be suspicious, or it could just be poor connection and the ACK is just not getting received.
- [What SNI hostnames and TLS versions did you observe, and what do they imply?]
	- Example.com when we curled the http version of it, and it appears it would not switch to the secure https. 
---

## Reflection
1. [What is the difference between capture filters (-f) and display filters (-Y)? Provide one scenario for each.]
- Capture filters is what you are filtering WHILE capturing, like only capturing DNS traffic
- Display filters is what you are filtering AFTER making the capture file, like capturing DNS, ICMP, TCP, but only viewing DNS with display filters.
2. [How can you reliably identify TCP vs UDP traffic using tshark output or fields?]
- For the traffic that I found, I could only see the difference in the name and that the DNS was in the same network when looking at the source and the destination.
3. [What can TLS metadata (e.g., SNI, version) reveal even when payloads are encrypted?]
- It can reveal the speed of the connection, so you could potentially guess if it's wifi or wired.
- Reveals the ip destination and hostname, so if you can do DNS poisoning you could try to masquerade as a bank or something of monetary value and gain access to that if they send information to the wrong destination.
- If the version is out of date, maybe there is a vulnerability that can be exploited to gain access to a victim's system.
4. [What ethical and legal boundaries must you respect when capturing network traffic?]
- It is illegal to port scan and capture network traffic of networks you do not own. I can't imagine Rogers was happy that one student was checking their system so brazenly. Ethically, you can also steal data unencrypted packets, so if somehow bank information is sent over an insecure connection, one could gain access to a victim's bank information.

---

## Artifacts Checklist (Required Filenames)

Please ensure these files are saved in `~/SPR100_Labs/Lab06/work/` with EXACT names:
- [ ] lab06_basic.pcapng
- [ ] lab06_dns_only.pcapng
- [ ] lab06_basic_fields.csv
- [ ] lab06_multi.pcapng
- [ ] lab06_part2.csv
- [ ] lab06_security_lo.pcapng
- [ ] lab06_tls.pcapng

---

## Troubleshooting Notes (Optional)
- [Document any issues (permissions, interfaces) and how you resolved them.]


