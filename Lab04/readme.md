# Lab04 - File System Security & Access Control

**Student Name:** Avery Yong
**Student ID:** 059789115
**Course Section:** SPR100NBB
**Date:** 2025-11-03

---

## Part 1: File Metadata and Permissions

### Commands and Outputs
```
$ ls -la
total 20
drwxr-xr-x 3 root root 4096 Nov  3 16:54 .
drwxr-xr-x 3 root root 4096 Nov  3 16:52 ..
-rw-r--r-- 1 root root   11 Nov  3 16:53 notes.txt
drwxr-x--- 3 root root 4096 Nov  3 16:54 projects
-rw------- 1 root root   46 Nov  3 16:53 secret.txt

$ stat secret.txt
File: /home/ubuntu/SPR100_Labs/Lab04/work/secret.txt
Size: 46        	Blocks: 8          IO Block: 4096   regular file
Device: 802h/2050d	Inode: 1835055     Links: 1
Access: (0600/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2025-11-03 16:53:31.322188508 +0000
Modify: 2025-11-03 16:53:22.298298457 +0000
Change: 2025-11-04 20:20:18.475235284 +0000
Birth: 2025-11-03 16:53:14.086402108 +0000

```

### Analysis
- Ownership is to root, since I made the file as root rather than making it as my account.
  - Modes are represented by the rwx for read, write and execute permissions, represented by 4,2,1 in their binary positions, which in the case of secret, since I made it as root, they are represented by 644, where secret.txt is able to be read and written by root, but read by other groups and anyone else. 
  - Doing the chmod a day later made it clear that it changed the "change" timestamp a day after I first created the file, but modifying it is unchanged since that would be editing file contents instead with nano or vim.

- If you cannot execute using the directory, you cannot travel through it, as I tried going into my ubuntu folder without root power as a temporary user and it denied permission even if it was in the SPR100_Labs with global execution permission, since all /home files come as 750 to not allow anything that isn't user or in whatever group that's relevant execute.
I unintentionally did the 4th step by making a temp account to usermod my name to my senecaID, and did the above.
Doing the actual 4th step I don't know how to login to that account, but the command tries to execute as "fsuser", and read out the text of secret.txt, but similarly gives "Permission denied", and then I don't know why we're printing "denied" after it. I assume for history checking reasons?

---

## Part 2: POSIX ACLs — Finer-Grained Access

### Commands and Outputs
```
$ getfacl secret.txt

# file: secret.txt
# owner: root
# group: root
user::rw-
group::---
other::---

$ setfacl -m u:fsuser:r-- secret.txt && getfacl secret.txt

# file: secret.txt
# owner: root
# group: root
user::rw-
user:fsuser:r--
group::---
mask::r--
other::---
```

### Analysis
- The man page says "Denotes maximum access rights granted by the 3 other types"... but that did not make any sense to me written like that. I read ask ubuntu and AI and to put it simply, the mask is a filter that may reduce the permissions for a specific group, and does not grant any. Like if a user has only r--, but the mask has rwx, it will not grant rwx, simply allow r as provided. 
However, the mask does not affect other because the mask only affects the user and groups, because it appears to be by design that it should not affect users that don't fall under the other:: umbrella.
- Why did fsuser read succeed and write fail?
We gave fsuser only read permissions, and since the mask also allows only read permissions, those are the only things possible. 
---

## Part 3: Extended Attributes and Encryption

### Commands and Outputs
```
$ setfattr -n user.note -v "tag:confidential" 

notes.txt && getfattr -d notes.txt
# file: notes.txt
user.note="tag:confidential"

$ zip -r secure_bundle.zip projects && \
  openssl enc -aes-256-cbc -salt -in secure_bundle.zip -out secure_bundle.zip.enc

adding: projects/ (stored 0%)
adding: projects/teamA/ (stored 0%)
adding: projects/teamA/idk.txt (stored 0%)
enter AES-256-CBC encryption password:
Verifying - enter AES-256-CBC encryption password:
*** WARNING : deprecated key derivation used.
Using -iter or -pbkdf2 would be better.
```

### Analysis
- I guess you could hide malicious code in the extended attributes since you can do the same in xml files and mp3 metadata. If it isn't detected or easily readable then it may be a hidden vector for attack
Security considerations of xattrs (visibility, backup, portability).
- The .enc file was stored in the same directory. If this is the same type of encryption of cryptocurrency, then when you don't know the key, this is lost forever, like that one person who died and made people lose millions.

---

## Reflection
1. When would ACLs be preferred over group changes or multiple groups?
- Of course when you need fine grained permission handling so that you can more easily set restrictions for specific groups without having to worry about if a user in that group has the permissions when they weren't supposed to
2. How does the ACL mask affect effective permissions?
- The ACL mask affects permissions by reducing how much groups or specified users can use. If a user has rwx, but the mask has only r--, then the user can only read for that file
3. Why is execute (x) on directories required for traversal?
- If you cannot execute directories, you will not be able to enter the directory, and the other files inside will inherit that. Though if it has read you can still use ls to look inside, though it will still say permission denied for any files shown for some reason. ls -la will also let you see what is inside, but not the permissions. Using nano will also not be possible, even if you know the file path.
4. What operational risks do extended attributes and ad‑hoc encryption introduce?
- If extended attributes have malicious code in it, it may not get checked during startup or in standard checks. The ad-hoc encryption we used from openssl is deprecated, so it should not be used, because this lacks built-in authentication, so the integrity is questionable.
