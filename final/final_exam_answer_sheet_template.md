# SPR100 Final Test — Answer Sheet

> ⚠️ Replace every `[placeholder]` with your real answer and delete the brackets.

## Student Information
- **Student Name:** Avery Yong
- **Student Number:** 059789115
- **Student Username:** ayong2
- **Security Lab Computer #:** NHK1003-27-A303 (The one in the far left corner, facing from door)

## Submission Checklist
- [x] `final_exam_answer_sheet.md` saved in `SPR100_Labs/final/`
- [ ] `task1/`, `task2/`, `task3/` folders added with required artifacts
- [ ] Final commit pushed with the REQUIRED finalization command

---

## Task 1 — Vault Custodian

| Item | Your Evidence |
| --- | --- |
| Hostname | ubuntu |
| Username used | ayong2 |
| `ls -l vault.log` | -rw-r-----+ 1 ayong2 ayong2 39 Dec 5 16:57 vault.log |
| `stat --format ... vault.log` | `[ayong2/ayong2/-rw-r-----/39]` |
| `getfacl` user line | user:auditor:r-- |
| `getfacl` mask line | mask::r-- |
| `sudo -u auditor cat ...` (first line) | Fri Dec  5 04:57:28 PM UTC 2025
ubuntu |
| `TASK1-TOKEN` | TASK1-TOKEN:2M2N2P26272G2N1E11161A18191A1212162W2J232N2A1E102A2H2F27102P242P2G2N2P101c1Z1b121111211V23242M10282B2G232E102N232M2D12102Q232P2E2N0p2E2H292W2H2R2G272L1E232T2H2G29132W292L2H2P2J1E232T2H2G29132W2F2H26271E112H1715112W2M2B2U271E141A2W23252E1E2P2M272L1B1B2L2R0n2W2P2M272L1B232P262B2N2H2L1B2L0n0n2W292L2H2P2J1B1B2L0n0n2W2F232M2D1B1B2L0n0n2W2H2N2A272L1B1B0n0n0n2W282B2E27212M2A231316171E172518181813252514131A2727111424121818142611131A23241A111112271626271A1725111519121615142416241314111A2417231A151A13141912131727
Keep this token with your other Task 1 observations in the answer sheet. |

Notes (optional, max 2 sentences):  
Ugh I had to setfacl -m g:auditor:r-x /home/ubuntu also to let auditor navigate through the folders

---

## Task 2 — Sentinel Service

- `ls -l watcher.sh`: -rwx------ 1 ayong2 ayong2 168 Dec  5 17:30 watcher.sh
- `final-watch.service` contents:
  ```
[Unit]
Description=SPR100 final watch logger

[Service]
Type=oneshot
ExecStart=/bin/bash -lc './watcher.sh'

# Do not add anything after this line

[Install]
WantedBy=default.target
  ```
- Last two `watchdog.log` lines:
  ```
  [Fill in line -2 here]
  [Fill in line -1 here]
  ```
- `Active:` line from `systemctl --user status final-watch.service`: `[Active: ...]`
- Latest journal entry (single line): `[timestamp unit message]`
- `@reboot` cron line: `[@reboot bash ...]`
- `TASK2-TOKEN`: `[TASK2-TOKEN:...]`

Mitigation reminder after grading (do NOT do during test): `[describe how you will remove hooks later]`

---

## Task 3 — Traffic Examiner

- Capture interface: `ens33`
- TLS ClientHello fields (`frame/ip.dst/SNI/version`):
0.108626910 192.168.194.128 → 23.220.75.245 TLSv1 571 Client Hello
- TLS version interpreted: TLSv1.3
- `io,stat` TLS/HTTP line: 
=============================
| IO Statistics             |
|                           |
| Duration: 14.  6943 secs  |
| Interval:  1 secs         |
|                           |
| Col 1: Frames and bytes   |
|---------------------------|
|          |1               |
| Interval | Frames | Bytes |
|---------------------------|
|  0 <>  1 |     25 |  6653 |
|  1 <>  2 |      1 |    60 |
|  2 <>  3 |      1 |    60 |
|  3 <>  4 |      2 |   130 |
|  4 <>  5 |      2 |   120 |
|  5 <>  6 |      1 |    60 |
|  6 <>  7 |      0 |     0 |
|  7 <>  8 |      0 |     0 |
|  8 <>  9 |      0 |     0 |
|  9 <> 10 |      0 |     0 |
| 10 <> 11 |      0 |     0 |
| 11 <> 12 |      0 |     0 |
| 12 <> 13 |      0 |     0 |
| 13 <> 14 |     10 |   756 |
| 14 <> Dur|      1 |    60 |
=============================
- Host/IP + protocol(s) from capture evidence: 
192.168.194.128 (Me)
23.192.228.80 
DNS to 23.192.228.80 OR example.com
From Me on TCP 60 and 74 to example.com
192.168.194.128 to TCP port 54 for acknowledge 
- `ls -l final_capture.pcapng`: 
	- -rw------- 1 ayong2 ayong2 9676 Dec  5 17:55 final_capture.pcapng
- `TASK3-TOKEN`: 
[Task 3] Initiating HTTPS request...
[Task 3] Traffic generation complete.
TASK3-TOKEN:2M2N2P26272G2N1E11161A18191A1212162W2P2L2E1E2A2N2N2J2M1B1010272S232F2J2E270p252H2F102W272G262J2HB2G2N1E13140p1313110p1315162W242T2N272M1E1612142W2J2L272Q2B272R1E240f1D0Z262H252N2T2J270Y2A2N2F2E1F1D2A2N2F2E0Y2E232G291E0a272G0a1f1D0f
Use tshark/wireshark to inspect the capture and extract the required details.

Optional Notes (max 2 sentences to describe what the python program `task_network.py` does):  
I've made a huge mistake

---

## Task B — Firewall Sentinel (Bonus)

- Domains/IPs blocked (from Task 3 analysis): `[Fill in here]`
- Commands used to add `ufw` rules:
  ```
  [Fill in here]
  ```
- `sudo ufw status numbered` (trimmed output):
  ```
  [Fill in here]
  ```
- Evidence that Task 3 script is blocked:
  ```
  [Error/output snippet]
  ```
- Evidence that other sites still work:
  ```
  [Successful command/output]
  ```

---

## Final Confirmation
- I confirm I followed all rules and performed the work independently. Yes
- Timestamp of final push (`date -u`): `2025-12-05 [YYYY-MM-DDTHH:MM:SSZ]`

**Signature (type your name):** Avery Yong

