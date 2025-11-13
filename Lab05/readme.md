# Lab05 - File System Persistence, Hiding, and Detection

**Student Name:** Avery Yong  
**Student ID:** 059789115  
**Course Section:** SPR100NBB  
**Date:** 2025-11-12  

---

## Part 1: Persistence and Concealment

### 1) Hidden Names and Locations (dotfiles)
#### Evidence (outputs/excerpts) and Notes
```
/home/ubuntu:
total 76
drwxr-x---   8 ayong2 ubuntu 4096 Nov 13 19:43 .
drwxr-xr-x   7 root   root   4096 Nov  4 21:07 ..
-rw-------   1 ayong2 ubuntu 6707 Nov 13 20:52 .bash_history
-rw-r--r--   1 ayong2 ubuntu  220 Jan  6  2022 .bash_logout
-rw-r--r--   1 ayong2 ubuntu 3902 Nov 13 19:18 .bashrc
-rw-rw-r--   1 ayong2 ubuntu 2766 Nov  3 17:06 bup.txt
drwx------   3 ayong2 ubuntu 4096 Nov 13 21:21 .cache
drwx------   4 ayong2 ubuntu 4096 Nov 13 19:35 .config
-rw-r--r--   1 ayong2 ubuntu 2458 Nov  3 17:01 file_acl_demo.py
-rw-r--r--   1 ayong2 ubuntu 1490 Nov  3 17:00 fs_inspect.py
-rw-rw-r--   1 ayong2 ubuntu  103 Nov 13 05:37 .gitconfig
-rw-r--r--   1 ayong2 ubuntu  227 Nov 13 19:43 idkharder.txt
-rw-------   1 ayong2 ubuntu   20 Nov 13 18:59 .lesshst
drwxrwxr-x   3 ayong2 ubuntu 4096 Oct  1 16:10 .local
-rw-r--r--   1 ayong2 ubuntu  807 Jan  6  2022 .profile
drwxrwx---+ 11 root   root   4096 Nov 13 05:37 SPR100_Labs
drwxr-xr-x   2 root   root   4096 Nov  3 17:05 SPR100_Midterm
drwx------   2 ayong2 ubuntu 4096 Nov  4 02:40 .ssh
-rw-r--r--   1 ayong2 ubuntu    0 Sep 14  2023 .sudo_as_admin_successful

/home/ubuntu/.cache:
total 12
drwx------ 3 ayong2 ubuntu 4096 Nov 13 21:21 .
drwxr-x--- 8 ayong2 ubuntu 4096 Nov 13 19:43 ..
-rw-r--r-- 1 ayong2 ubuntu    0 Sep 14  2023 motd.legal-displayed
drwxr-xr-x 2 ayong2 ubuntu 4096 Nov 13 21:30 .thumbs

/home/ubuntu/.config:
total 16
drwx------ 4 ayong2 ubuntu 4096 Nov 13 19:35 .
drwxr-x--- 8 ayong2 ubuntu 4096 Nov 13 19:43 ..
drwx------ 2 ayong2 ubuntu 4096 Oct 16 17:54 htop
drwxr-xr-x 3 ayong2 ubuntu 4096 Nov 13 19:35 systemd

/home/ubuntu/SPR100_Labs/Lab05/work:
total 12
drwxr-xr-x 2 ayong2 ubuntu 4096 Nov 13 21:30 .
drwxr-xr-x 4 ayong2 ubuntu 4096 Nov 13 17:26 ..
```
#### Analysis
- The .files become hidden because this is the standard for configuration files, which want to be hidden so people cannot see it and attempt to edit it. Without the 
[Go test if ls -la works as user:temp]
What became hidden and why? Explain how dotfiles affect listings and traversal.

### 2) Extended Attributes (xattrs)
#### Evidence (outputs/excerpts) and Notes
```
getfattr: Removing leading '/' from absolute path names
# file: home/ubuntu/SPR100_Labs/Lab05/.cache/.thumbs/.note
user.tag="hidden:lab05"
```
#### Analysis
- The data is stored in attributes as a kind of metadata, I assume similar to an mp3 files having artist, album, title information. I don't know any other commands to view the extended attributes without using getfattr, so this is mostly invisible to me. If you need this xattr information elsewhere however, it seems it both needs a program called Rsync and for whatever system you're installing it on to also have xattr support.

### 3) Immutable Bit Demonstration
#### Evidence (before/after)
```
lsattr lockme.txt
--------------e------- lockme.txt
ayong2@ubuntu:~/SPR100_Labs/Lab05$ sudo chattr +i lockme.txt
[sudo] password for ayong2:
ayong2@ubuntu:~/SPR100_Labs/Lab05$ echo x >> lockme.txt || echo "append denied"
-bash: lockme.txt: Operation not permitted
append denied
```
#### Analysis
- Describe behavior before/after immutable. How would you safely reverse it?
	- It breaks my VM if I leave it immutable, gave me "The process cannot access the file because another process has locked a portion of the file." I may have unsafely reversed it by deleting all relevant .lck files in that VM folder on my SSD.

### 4) Shell RC Login Hook
#### Evidence
```
[paste the added ~/.bashrc line(s) and recent lines from hook.log]
echo "[Lab05 demo] User login hook executed: $(date)" >> /home/ubuntu/SPR100_Labs/Lab05/work/hook.log

[Lab05 demo] User login hook executed: Thu Nov 13 07:19:16 PM UTC 2025
[Lab05 demo] User login hook executed: Thu Nov 13 07:19:36 PM UTC 2025
[Lab05 demo] User login hook executed: Thu Nov 13 07:19:50 PM UTC 2025
[Lab05 demo] User login hook executed: Thu Nov 13 07:20:00 PM UTC 2025
```
#### Analysis
- What did you add, when does it run, and what are the risks of RC file changes?
	- In the first week of Linux we were also taught to edit the .bashrc file and make it possible to poweroff by just writing poof as an alias, so that is also there.
What I added was a command to print "[Lab05 demo] User login hook executed:" the current date in UTC, and save it to the hook.log file in my .../Lab05/work folder. The risk of editing the .bashrc file is that it runs scripts upon startup, as well as some other things while the OS is running, like appending to the history file.


### 5) systemd User Service (preferred)
#### Unit File Content (paste your file)
```
~/.config/systemd/user/lab05-demo.service
-----------------------------------------
[Unit]
Description=Lab05 benign demo (user)

[Service]
Type=oneshot
ExecStart=/bin/bash -lc 'echo "[Lab05 demo] systemd user service ran: $(date)" >> ~/SPR100_Labs/Lab05/work/hook.log'

[Install]
WantedBy=default.target
```
#### Verification Evidence
```
- tail of hook.log:
[Lab05 demo] User login hook executed: Thu Nov 13 07:19:50 PM UTC 2025
[Lab05 demo] User login hook executed: Thu Nov 13 07:20:00 PM UTC 2025
[Lab05 demo] systemd user service ran: Thu Nov 13 08:10:21 PM UTC 2025
```
#### Analysis
- How does a user service persist? What confirmed it ran? Why is `--user` important?
	- User services persist as files, sometimes needing to be loaded or mentioned in a file in the main directory. "Created symlink" signals confirmation it was linked, then our hooks.log message " systemd user service ran: $(date)" and journalctl confirmed the Lab05 benign demo it was run and finished. --user denotes our specific configurations to the current user.
### 6) Crontab @reboot (if systemd user unavailable)
#### Evidence
```
@reboot echo "[Lab05 demo] cron @reboot: $(date)" >> /home/ubuntu/SPR100_Labs/Lab05/work/hook.log
```
#### Analysis
- Where are user cron jobs stored on your system? When would this run?
	- Jobs for cron are stored in the hooks.log, which upon reboot, it will run and add the "cron @ reboot" with the current date and time to hooks.log, alongside the .bashrc and lab05-demo.service.

---

## Part 2: Detection and Mitigation

### 1) Enumerate Hidden Files
#### Evidence
```
[paste relevant `ls -la` / `find` excerpts that show hidden file paths]
drwxr-xr-x 2 ayong2 ubuntu 4096 Nov 13 19:19 .
drwxr-xr-x 4 ayong2 ubuntu 4096 Nov 13 17:26 ..
-rw-r--r-- 1 ayong2 ubuntu  627 Nov 13 20:53 hook.log

/home/ubuntu/.bash_logout
/home/ubuntu/.sudo_as_admin_successful
/home/ubuntu/.lesshst
/home/ubuntu/.profile
/home/ubuntu/.bashrc
/home/ubuntu/.gitconfig
/home/ubuntu/.bash_history

```
#### Analysis
- These look suspicious? .bash_history just shows commands that have been written, gitconfig is just git configurations set by "git config" commands, .bash_logout clears the screen to increase privacy. I suppose ~/.profile and sudo_as_admin_succussful is a little suspicious but only because profile can change my private bin or includes .bashrc if I'm using bash. 

### 2) Inspect Metadata, ACLs, and xattrs
#### Evidence
```
stat: cannot statx '/home/ubuntu/.cache/.thumbs/.note': No such file or directory

getfacl: .note: No such file or directory
getfacl not available

getfattr: /home/ubuntu/.cache/.thumbs/.note: No such file or directory
no xattrs

The .note does not exist here, since it is in the ~/SPR100_Labs/Lab05/notes/.cache/.thumbs/ directory.

However the file in /home/ubuntu/SPR100_Labs/Lab05/notes/.cache/.thumbs/ returns:
stat:
  File: .note
  Size: 25              Blocks: 8          IO Block: 4096   regular file
Device: 802h/2050d      Inode: 1835295     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/  ayong2)   Gid: ( 1000/  ubuntu)
Access: 2025-11-13 21:30:07.074540237 +0000
Modify: 2025-11-13 21:30:07.074540237 +0000
Change: 2025-11-13 21:36:15.802933953 +0000
 Birth: 2025-11-13 21:30:07.074540237 +0000

acl:
# file: .note
# owner: ayong2
# group: ubuntu
user::rw-
group::r--
other::r--

xattr:
# file: .note
user.tag="hidden:lab05"

```
#### Analysis
- What did the metadata and ACL/xattrs reveal about access and labels?
	- That permissions are minimal, only allowing reading to everyone, and writing to only the creator. xattrs does not show user.tag="hidden:lab05" without -d, as it will show only user.tag.

### 3) Detect Startup Hooks
#### Evidence
```
120:echo "[Lab05 demo] User login hook executed: $(date)" >> /home/ubuntu/SPR100_Labs/Lab05/work/hook.log

lab05-demo.service                               enabled   enabled

systemctl --user status lab05-demo.service --no-pager || true

○ lab05-demo.service - Lab05 benign demo (user)
     Loaded: loaded (/home/ubuntu/.config/systemd/user/lab05-demo.service; enabled; vendor preset: enabled)
     Active: inactive (dead) since Thu 2025-11-13 20:53:22 UTC; 1h 8min ago
    Process: 925 ExecStart=/bin/bash -lc echo "[Lab05 demo] systemd user service ran: $(date)" >> ~/SPR100_Labs/Lab05/work/hook.log (code=exited, status=0/SUCCESS)
   Main PID: 925 (code=exited, status=0/SUCCESS)
        CPU: 32ms

Nov 13 20:53:22 ubuntu systemd[918]: Starting Lab05 benign demo (user)...
Nov 13 20:53:22 ubuntu systemd[918]: Finished Lab05 benign demo (user).

1  @reboot echo "[Lab05 demo] cron @reboot: $(date)" >> /home/ubuntu/SPR100_Labs/Lab05/work/hook.log

These are all working and not running the echo command messages

```
#### Analysis
- Which mechanisms were active? How would you prioritize investigation?

### 4) Live Monitoring with inotifywait
#### Evidence
```
/home/ubuntu/SPR100_Labs/Lab05/work/ CREATE hooks.log
/home/ubuntu/SPR100_Labs/Lab05/work/ MODIFY hooks.log
/home/ubuntu/SPR100_Labs/Lab05/work/ MODIFY hook.log
/home/ubuntu/SPR100_Labs/Lab05/work/ DELETE hooks.log
/home/ubuntu/SPR100_Labs/Lab05/work/ CREATE .testing.swp
/home/ubuntu/SPR100_Labs/Lab05/work/ MODIFY .testing.swp
/home/ubuntu/SPR100_Labs/Lab05/work/ DELETE .testing.swp
/home/ubuntu/SPR100_Labs/Lab05/work/ CREATE .testing.swp
/home/ubuntu/SPR100_Labs/Lab05/work/ MODIFY .testing.swp
/home/ubuntu/SPR100_Labs/Lab05/work/ CREATE testing
/home/ubuntu/SPR100_Labs/Lab05/work/ MODIFY testing
/home/ubuntu/SPR100_Labs/Lab05/work/ DELETE .testing.swp
```
#### Analysis
- What events occurred and what did they indicate?
	- I accidentally mispelled hook.log by doing echo "I'm in" > hooks.log, and that both created and modified hooks.log. When I realized my mistake I did the same thing but modified the hook.log file isntead, then ran "rm hooks.log" to get rid of it. I then did nano testing, which created and modified the "testing.swp" file in nano, added content, pressed Ctrl+O, Enter and exited, which created the actual "testing" file, then modified it with the content I added. Upon exiting it then deleted the testing.swp file because it is a temporary "swap" file that saves changes I've made, but haven't saved. I now hope I never have to make a text editing program or software.

### 5) Mitigation Steps (Before/After Evidence)
#### Evidence
```

ayong2@ubuntu:~/.cache/.thumbs$ sudo chattr -i lockme.txt 2>/dev/null || true
[sudo] password for ayong2:
ayong2@ubuntu:~/.cache/.thumbs$ grep -n 'Lab05 demo' ~/.bashrc || echo "(bashrc hook removed)"
(bashrc hook removed)
ayong2@ubuntu:~/.cache/.thumbs$ systemctl --user list-unit-files --type=service | grep -i lab05 || echo "(service removed)"
lab05-demo.service                               disabled  enabled
ayong2@ubuntu:~/.cache/.thumbs$ crontab -l 2>/dev/null | grep -i '@reboot' || echo "(no @reboot)"
(no @reboot)
ayong2@ubuntu:~/.cache/.thumbs$ getfattr -d note.txt 2>/dev/null || echo "(no xattrs)"
(no xattrs)
[paste before/after snippets proving each cleanup: RC hook removed, unit disabled/removed, @reboot removed, xattrs cleared]
```
#### Analysis
- For each mechanism you created, explain how you detected it and how you removed it safely.
	- For some of these I can confirm. In .bashrc, which I can easily do by changing back to my home directory and doing nano .bashrc, then scrolling to the bottom to confirm the line we added is gone. I can confirm 
---

## Reflection
1. Where should defenders look first for user‑level persistence on Linux?
- Usually on their direct /home/[user] directory
2. What are strengths/limits of ACLs and xattrs for concealment and for defense?
- ACLs are great for filtering out any defined or undefined groups from having access to files, directories. 

- I'm honestly very unsure what xattrs is doing, as this seems like only metadata that can hold information which may or not be relevant if it gets moved to a system that doesn't support it. I read one article during Lab 4 where it was stated to be possible to abuse xattrs on macOS to hide data, as it would not be checked in many cases, but then this would be more of a "security by obscurity" thing, which is more of a defender issue to make a check for it.

3. Why is execute (`x`) on directories relevant for detection (traversal)?
- Execution on directories allows whoever has that permission to run the file to enter it. Otherwise it will give Permission denied.
4. What operational risks should you consider before deleting suspicious files (e.g., immutable, ownership, backups)?
- If the file seems suspicious, it may be better to save it as another file on linux, like doing mv [filename] [filename.sus] so that it won't run anything, but if it is an important file, the contents and details should remain.

---

## Appendix (Optional)
- Extra logs, screenshots, or notes that support your answers.


