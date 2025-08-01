#!/bin/bash

LOGFILE="dmesg.log"
grep "Linux version" "$LOGFILE"
