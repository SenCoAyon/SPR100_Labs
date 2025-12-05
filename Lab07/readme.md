## Lab Activities

0) **Create a workspace and work from there on each VM (especially VM1):**

```bash
mkdir -p ~/SPR100_Labs/Lab07/work
cd ~/SPR100_Labs/Lab07/work
```

- Keep notes and configuration snippets in this folder as you go.

---

### Part 1: Configure UFW Firewall Rules on Ubuntu (VM1) (40 minutes)

Goal: Enable and configure `ufw` on VM1 and test connectivity from VM2.

> **CRITICAL WARNING:**
> 1. **IP Addresses:** The examples below use `192.168.56.x`. You **MUST** replace these with your actual VM IP addresses (check using `ip addr`).
> 2. **Interfaces:** Examples use `eth0`. Your interface might be `ens33` or `ens160`. Check using `ip addr` or `tshark -D` and use the correct name.

#### 1) Define basic rules (Prevent Lockout)

**Crucial Step:** You must define your "allow" rules **before** enabling the firewall. If you enable the firewall first while using SSH, you will be locked out immediately.

On **VM1**, add rules to control SSH (if needed), HTTP, and ICMP:

```bash
# Set default policies first
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (CRITICAL if you are connected remotely!)
sudo ufw allow 22/tcp

# Allow HTTP (for testing later)
sudo ufw allow 80/tcp

# Block telnet (bad practice example)
sudo ufw deny 23/tcp
```

- Think:
  - Why is `deny 23/tcp` considered a best practice? 
	- Telnet is very insecure. If you send anything over telnet and they capture those packets, they can see all the data written in there.

  - What is the difference between `allow 80/tcp` and `allow from 192.168.1.50 to any port 80 proto tcp`?
	- "allow 80/tcp" allows incoming traffic from port 80/tcp, as opposed to "allow from 192.168.1.50 to..." which allows inbound traffic from only 192.168.1.50

#### 2) Enable UFW

Now that you have allowed SSH, it is safe to enable the firewall.

```bash
sudo ufw enable
# Press 'y' to confirm if prompted
```

Inspect the status:

```bash
sudo ufw status numbered
```

- My active rules:
  - Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere
[ 2] 22                         ALLOW IN    Anywhere
[ 3] 80/tcp                     ALLOW IN    Anywhere
[ 4] 23/tcp                     DENY IN     Anywhere
[ 5] 80/tcp                     ALLOW IN    192.168.1.50
[ 6] 22/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 7] 22 (v6)                    ALLOW IN    Anywhere (v6)
[ 8] 80/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 9] 23/tcp (v6)                DENY IN     Anywhere (v6)
	- Oh that's what I was missing when I tried to fix Aamna's ssh. You need to add /tcp.
#### 3) Source-specific rules and best practices

Design some **source-specific** rules on VM1, assuming:

- VM1 (Firewall) IP: e.g., `192.168.56.10` IP set to: .4
- VM2 (Client) IP: e.g., `192.168.56.11` IP set to: .5
	- I guess I'll just make this the OPS105 things since I've already started with them

Examples:

```bash
# Allow HTTP only from VM2
sudo ufw allow from 192.168.58.5 to any port 80 proto tcp

# Block everything from an example “untrusted” IP
sudo ufw deny from 192.168.56.99
```

Best practices to discuss and apply:

- Start from a **default deny** stance and explicitly allow what is needed:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

- Avoid duplicate/conflicting rules; periodically review with:

```bash
sudo ufw status numbered
```
22/tcp			ALLOW		Anywhere
22			ALLOW		Anywhere
80/tcp			ALLOW		Anywhere
23/tcp			DENY		Anywhere
80/tcp			ALLOW		192.168.1.50
22/tcp			ALLOW		192.168.58.5
22/tcp			ALLOW		192.168.58.4
22/tcp (v6)		ALLOW		Anywhere (v6)
22  (v6)		ALLOW		Anywhere (v6)
80/tcp  (v6)		ALLOW		Anywhere (v6)
23/tcp  (v6)		DENY		Anywhere (v6)

- Remove rules you no longer need:

```bash
sudo ufw delete <rule-number>
```

- Record:
  - At least **3–5 rules** you created and why (what risk or requirement each addresses).
	- I previously made ufw allow port 22 when we first needed to send files outside of what I think was Lab 2B, which risk wise would have allowed anything that knew or could guess any of my user passwords to ssh or copy files into my VM with scp
	- I added the three rules given above for allowing port 22/tcp, port 80/tcp and denying port 23/tcp, which allows ssh and scp to the the VM, HTTP use and stopping Telnet, but these are both deprecated and unsecure.
	- Then I added deny port 80 for testing if it stops pings, which it does not, but it allows the use of HTTP, which is not secure since it is in plaintext

#### 4) Test rules from VM2 (Client VM)

On **VM2**, use `ping`, `curl`, or other tools to verify your rules:

```bash
# Replace IP with VM1's IP
ping -c 4 192.168.58.4

curl -v http://192.168.58.4/        # if you have a web server or simple Python HTTP server
```

**Required Setup:** On VM1, you must run a simple HTTP server for testing to distinguish between "Connection Refused" (Service Down) and "Filtered" (Firewall Blocked).

**Note:** Port 80 is a privileged port, so you need `sudo`.

```bash
cd ~/SPR100_Labs/Lab07/work
sudo python3 -m http.server 80
```

- Test scenarios:
  - From VM2 (allowed IP) to port 80: does it succeed?
  - Change the rule to allow only a **different** IP and see the effect.
  - Try accessing a port that is not allowed.

### Record:
- Which tests **succeeded** and which **failed**, and how that matches your `ufw` rules.
	- curl works when I have "allow 80/tcp" but will instead give "*Trying 192.168.58.4:80" if I give "deny 80/tcp". Then the server gives  "192.168.58.5 - - [03/Dec/2025 17:35:31] "GET / HTTP/1.1" 200 -"
- Any surprising results (e.g., something allowed that you thought was blocked).
	- Not what I'd call surprising after being told in class, but more annoying that it really is important that it goes through the numbered list, otherwise it will ignore later deny rules. I made a deny rule after making the allow 80/tcp rule, but using curl on VM2 will work.

Reflection for Part 1:

- How does `ufw` simplify firewall management compared to raw `iptables`?
	- Has much more plain English commands, so that they make logical sense for how they work; Like when I write allow from 192.168.58.5 to any port 80 proto tcp is borderline a real sentence. As opposed to nftables which has long unintelligible lines like "nft add chain ip nat POSTROUTING '{ type nat hook postrouting priority 100; policy accept }'"
	- Still kind of verbose though
- Why is “default deny incoming, allow outgoing” a common baseline?
	- It is the most secure because it doesn't allow any unknown inbound traffic.
- What could go wrong if you enable `ufw` on a remote server without planning SSH rules?
	- People won't be able to ssh in, because we couldn't get it to work in the first month of class and like I stated before, the port 22 was open when we started, but upon enabling ufw, suddenly our ssh would not work, despite being on the same subnet
---

### Part 2: Use TShark to Observe Packets and Firewall Effects (35 minutes)

Goal: Use `tshark` on VM1 to see which packets arrive and whether your firewall rules are effective.

#### 1) Capture traffic with and without restrictive rules

On **VM1**:

1. Pick the network interface used between VM1 and VM2 (e.g., `eth0`, `ens33`, or similar):

```bash
tshark -D
```
- So this is VM1's ens34 to VM2's ens33
2. Start a short capture **before** adding a new restrictive rule:

```bash
sudo tshark -i eth0 -a duration:15 -w lab07_before_ufw.pcapng  # adjust interface
```
- Why is this not capturing things
3. During those 15 seconds, on **VM2**:

```bash
ping -c 5 192.168.58.4
curl -s -o /dev/null -w "%{http_code}\n" http://192.168.58.4/
```

### Record:
- Whether ping and HTTP succeed.
	- ping works, HTTP does not give a response
- Basic stats from pcapng file:
	- 28 frames


```bash
tshark -r lab07_before_ufw.pcapng -q -z io,stat,1
```
=============================
| IO Statistics             |
|                           |
| Duration: 13. 55916 secs  |
| Interval:  1 secs         |
|                           |
| Col 1: Frames and bytes   |
|---------------------------|
|          |1               |
| Interval | Frames | Bytes |
|---------------------------|
|  0 <>  1 |      1 |    74 |
|  1 <>  2 |      2 |   128 |
|  2 <>  3 |      6 |   516 |
|  3 <>  4 |      2 |   196 |
|  4 <>  5 |      2 |   196 |
|  5 <>  6 |      2 |   196 |
|  6 <>  7 |      6 |   400 |
|  7 <>  8 |      3 |   238 |
|  8 <>  9 |      1 |    74 |
|  9 <> 10 |      0 |     0 |
| 10 <> 11 |      1 |    74 |
| 11 <> 12 |      0 |     0 |
| 12 <> 13 |      0 |     0 |
| 13 <> Dur|      2 |   120 |
=============================

#### 2) Apply a new blocking rule and capture again

On **VM1**, block all incoming traffic from VM2’s IP:

```bash
sudo ufw deny from 192.168.58.5
sudo ufw status numbered
```

Now run another capture:

```bash
sudo tshark -i eth0 -a duration:15 -w lab07_after_ufw.pcapng
```

During this time, on **VM2**:

```bash
ping -c 5 <VM1_IP>
curl -s -o /dev/null -w "%{http_code}\n" http://<VM1_IP>/
```

- Compare:
- Does `ping` still get replies?
	- Yes, as ufw allows ping requests by default, and is not affected by port 80 or 22, since it is ICMP, and not TCP
- Does HTTP still work?
	- Yes, because the order of rules, it will just take the earliest rule, which still has the ufw allow 80/tcp, so it will take the earlier rule first.
[ 1] 22/tcp                     ALLOW IN    Anywhere
[ 2] 80/tcp                     ALLOW IN    Anywhere
[ 3] 23/tcp                     ALLOW IN    Anywhere
[ 4] Anywhere                   DENY IN     192.168.58.5
[ 5] 22/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 6] 80/tcp (v6)                ALLOW IN    Anywhere (v6)
[ 7] 23/tcp (v6)                ALLOW IN    Anywhere (v6)
	- After resetting it, it does not change anything

Use `tshark` display filters to study packets:

```bash
# ICMP packets
tshark -r lab07_after_ufw.pcapng -Y "icmp" -T fields -e frame.number -e ip.src -e ip.dst | head

# HTTP (TCP/80)
tshark -r lab07_after_ufw.pcapng -Y "tcp.port==80" \
  -T fields -e frame.number -e ip.src -e ip.dst -e tcp.flags | head
```

### Think:
- Do you still see ICMP echo *requests* from VM2 but no *replies* from VM1?
	- Yes, but VM1 still replies because ufw denial doesn't affect pinging
- How does this pattern reflect the firewall’s behavior?
	- But there is SYN but there is no ACK, since it's TCP
- What differences do you see in the HTTP traffic before vs after the rule?
	- TCP only receives SYN, but will not return SYN/ACK

#### 3) Export structured fields to CSV

Create a CSV summarizing packets for analysis:

```bash
tshark -r lab07_after_ufw.pcapng \
  -T fields -E header=y -E separator=, \
  -e frame.time_relative -e _ws.col.Protocol \
  -e ip.src -e ip.dst -e icmp.type -e tcp.srcport -e tcp.dstport \
  > lab07_after_ufw_fields.csv
```
frame.time_relative,_ws.col.Protocol,ip.src,ip.dst,icmp.type,tcp.srcport,tcp.dstport
0.000000000,ICMP,192.168.58.5,192.168.58.4,8,,
0.000069940,ICMP,192.168.58.4,192.168.58.5,0,,
1.001632506,ICMP,192.168.58.5,192.168.58.4,8,,
1.001700906,ICMP,192.168.58.4,192.168.58.5,0,,
2.003066932,ICMP,192.168.58.5,192.168.58.4,8,,
2.003134822,ICMP,192.168.58.4,192.168.58.5,0,,
3.030790632,ICMP,192.168.58.5,192.168.58.4,8,,
3.030862890,ICMP,192.168.58.4,192.168.58.5,0,,
3.591365389,TCP,192.168.58.5,192.168.58.4,,51246,80
3.591427816,TCP,192.168.58.4,192.168.58.5,,80,51246
4.032522201,ICMP,192.168.58.5,192.168.58.4,8,,
4.032581601,ICMP,192.168.58.4,192.168.58.5,0,,
4.472020164,DNS,192.168.220.128,192.168.220.1,,,
4.472020560,DNS,192.168.220.128,192.168.220.1,,,
4.472302735,TCP,192.168.220.128,192.168.220.1,,35292,53
5.033741220,ICMP,192.168.58.5,192.168.58.4,8,,
5.033808811,ICMP,192.168.58.4,192.168.58.5,0,,
5.494447319,TCP,192.168.220.128,192.168.220.1,,35292,53
6.034256290,ICMP,192.168.58.5,192.168.58.4,8,,
6.034289862,ICMP,192.168.58.4,192.168.58.5,0,,
7.062468782,ICMP,192.168.58.5,192.168.58.4,8,,
7.062539807,ICMP,192.168.58.4,192.168.58.5,0,,
7.510543300,TCP,192.168.220.128,192.168.220.1,,35292,53
8.086078652,ICMP,192.168.58.5,192.168.58.4,8,,
8.086155321,ICMP,192.168.58.4,192.168.58.5,0,,
9.110611061,ICMP,192.168.58.5,192.168.58.4,8,,
9.110681446,ICMP,192.168.58.4,192.168.58.5,0,,
10.112131336,ICMP,192.168.58.5,192.168.58.4,8,,
10.112200673,ICMP,192.168.58.4,192.168.58.5,0,,
11.112829248,ICMP,192.168.58.5,192.168.58.4,8,,
11.112894886,ICMP,192.168.58.4,192.168.58.5,0,,
11.734395211,TCP,192.168.220.128,192.168.220.1,,35292,53
12.118547081,ICMP,192.168.58.5,192.168.58.4,8,,
12.118609288,ICMP,192.168.58.4,192.168.58.5,0,,
12.758143631,ARP,,,,,
12.758408445,ARP,,,,,
13.119585814,ICMP,192.168.58.5,192.168.58.4,8,,
13.119654608,ICMP,192.168.58.4,192.168.58.5,0,,
13.155321677,ARP,,,,,
13.155703825,ARP,,,,,
13.269917712,ARP,,,,,
13.269941904,ARP,,,,,
14.134778304,ICMP,192.168.58.5,192.168.58.4,8,,
14.134847838,ICMP,192.168.58.4,192.168.58.5,0,,
14.485165974,TCP,192.168.220.128,192.168.220.1,,38322,53
### Open the CSV and identify:
- Which rows show blocked ICMP (e.g., only requests, no replies)?
	- Any row that has TCP is probably only requests, because ICMP was not blocked
- Which rows show allowed TCP/80 traffic?
	- Rows 9, 10 are the only ones that have accepted port 80 traffic, as shown from the 80 represented in the destination port column, all others are port 53

Reflection for Part 2:

- How can `tshark` demonstrate that a firewall rule is working, *even if you only see one side* of the conversation?
	- It's hard to see from the frames it records, as I got a lower amount of traffic upon adding a deny rule. Instead, reading and having a display filter with the packet captures can show what traffic is being correctly filtered out.
- Why is it useful to export to CSV for later analysis (e.g., with spreadsheets or scripts)?
	- Just to get the relevant information with specific columns that you may wish to look for a specific pattern or to check behaviour of something on the network, (e.g To check if my firewall rules are in the right order)
- What patterns (e.g., missing replies, RSTs) might indicate blocked or refused connections?
	- No TCP [ACK] to follow a previous TCP [SYN] 
	- Or a TCP [SYN] with a TCP [RST ACK] to notify the sender that the connection is closed
---

### Part 3: Using AI to Design Complex Firewall Rule Sets (35 minutes)

Goal: Learn how to describe requirements clearly to an AI assistant so it can propose a safe, coherent `ufw` rule set.

> **Important:** In the *real* final and midterm, AI assistants may be **disallowed**. This part is about learning **how** to communicate with AI *when allowed* in real-world work, not during closed-book assessments.

#### 1) Principles of good AI prompts for firewall rules

To get reliable code from AI, it is helpful to follow "Prompt Engineering" best practices. A widely cited framework involves defining:
1. **Persona** (Who is the AI acting as?)
2. **Context** (What is the environment?)
3. **Task** (What exactly needs to be done?)
4. **Constraints** (What must NOT happen? What limits exist?)
5. **Format** (How should the output look?)

*Reference: [OpenAI Prompt Engineering Guide - Tactics](https://platform.openai.com/docs/guides/prompt-engineering/tactics)*

**Example "Rigorous" Prompt:**

> **Persona:** Act as a Senior Linux System Administrator.
> 
> **Context:** I am configuring a firewall on an Ubuntu 22.04 server using `ufw` (Uncomplicated Firewall). My server IP is `192.168.56.10`. The client IP is `192.168.56.11`.
> 
> **Task:** Generate the exact `ufw` commands to configure the firewall to meet these requirements:
> - Default policy: Deny all incoming, allow all outgoing.
> - SSH (Port 22/tcp): Allow ONLY from the client IP (`192.168.56.11`).
> - HTTP (Port 80/tcp) and HTTPS (Port 443/tcp): Allow from ANY IP.
> - Block all other incoming traffic.
> 
> **Constraints:**
> - Do NOT use raw `iptables` commands; use only `ufw`.
> - Include comments explaining each rule.
> - Ensure the commands do not flush existing SSH connections if run in sequence.
> 
> **Format:** Provide the commands in a single bash script block.

- Think:
  - Why is it safer to specify "Do NOT use raw iptables"?
  - How does adding the "Context" (IP addresses) prevent the AI from giving you generic `0.0.0.0/0` rules that might be too permissive?

#### 2) Translate AI suggestions into a safe test plan

Even if AI gives you a rule set, you must:

- **Review** each rule line by line.
- Ensure you **do not remove your own access** (e.g., SSH).
- Apply rules step by step, testing between steps.

Practice task (on paper / in your README, not by actually using AI in the lab):

1. Write a detailed prompt for the following scenario using the **Persona/Context/Task/Constraints/Format** structure:
   - **Context:** VM1 (Server) and VM2 (Client) are on the same subnet.
   - **Task:** Configure VM1 to:
     - Allow SSH on port 22 (only from VM2).
     - Allow HTTP on port 8080 (from the whole subnet).
     - Allow DNS server on port 53/udp (from subnet `192.168.56.0/24` only).
   - **Constraints:** Default deny incoming, allow outgoing; log all denied packets.
2. In your own words, draft what you **expect** the AI’s response to include:
- Example `ufw` commands.
	- This will need: 
        	- sudo ufw allow from 192.168.56.11 to any port 22 proto tcp
		- sudo ufw allow from 192.168.56.0/24 to any 
        	- sudo ufw allow from 192.168.56.0/24 to any port 53/udp
- Any logging or rate-limiting rules.
	- After reading the man ufw page on logging, I would assume they would put on medium level for blocking all INVALID packets and those that don't match the defined policy
3. (Optional, outside test conditions) Later, you can try this prompt with an AI and compare the results to your expectations.

#### 3) Design your own complex rule set

For your **final task** in this lab, design a more complex rule set **yourself**, as if you were the AI:

Scenario:

- You are protecting a small internal application server (VM1) with IP `192.168.56.10`.
- Requirements:
  - SSH (22/tcp) only from `192.168.56.11` (admin VM2).
  - HTTP (80/tcp) only from `192.168.56.0/24`.
  - Block all access from IP `192.168.56.50`.
  - Allow DNS queries (53/udp) from local subnet, but **rate-limit** repeated attempts from any single host.
  - Default: deny incoming, allow outgoing, log denied traffic.

Tasks:

1. In your README, write the **prompt** you    would give an AI for this scenario.
2. Then, **without** using AI, write the actual `ufw` commands you would expect to see.
3. Optionally, implement and test a subset of these rules on VM1 and verify with:
   - `sudo ufw status numbered`
   - `ping`, `curl`, `dig` from VM2
   - `tshark` captures similar to Part 2

Reflection for Part 3:

- How does writing a good AI prompt force you to think clearly about requirements?
	- By making me not trust AI to do the job I want it to, so that I personally look at the goals that I need to achieve and understanding the tools that I can use to achieve it.
- What are the risks of blindly copy-pasting firewall rules from any assistant (human or AI)?
	- Sometimes AI will make up random information that does not exist
	- Sometimes AI will draw information from a source that is too specific to work in certain situations
	- If you trust another classmate, they may sabotage you for whatever reason, whether to learn to do it yourself, because they didn't do it fully correctly, or because they want you to learn a lesson. I have sabotaged some classmates by doing it for them for my own practice, but some have had to drop out of a course because they did not know how to replicate it.
- How can you combine AI assistance with your own `tshark` and testing skills to safely deploy rules?
	- 
---

## 🧪 Deliverables

Submit a `README.md` in `Labs/Lab07/` that includes:

- Commands you ran on VM1 and VM2 (trim outputs to the most relevant lines).
- Text snippets showing:
  - `ufw status numbered` before and after your rules.
  - `tshark` output / CSV excerpts demonstrating allowed vs blocked traffic.
- Clear explanations (in your own words) of:
  - Your final `ufw` rule set and what each major rule does.
  - How you verified rule behavior using VM2 and `tshark`.
  - One example of a good AI prompt for firewall rules, plus your analysis of why it is good.

### Files to Save in `~/SPR100_Labs/Lab07/work/` (Suggested Names)

- `lab07_before_ufw.pcapng`
- `lab07_after_ufw.pcapng`
- `lab07_after_ufw_fields.csv`
- Any additional captures or scripts you created for testing

> Keep files reasonably small (short capture durations) so your repository stays under size limits.

---

## 📤 Submission Instructions

Follow the same submission flow as previous labs and the Labs root guidelines:

1. Place your lab `README.md` and any artifacts in `Labs/Lab07/`
2. Commit and push before the deadline

Suggested commit message:  
“Complete Lab07 – UFW Firewall and Packet Analysis”

---


