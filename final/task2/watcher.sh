#!/usr/bin/env bash
LOG="$HOME/SPR100_Labs/final/task2/watchdog.log"
date >> watchdog.log
hostname >> watchdog.log
echo "bork bork, it looks okay?" >> watchdog.log
exit 0
