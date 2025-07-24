#!/bin/bash
#  Bash script to find the endpoint (URL) that received the most requests, indicating it was likely the target of the attack.
awk -F'"' '{print $2}' logs.txt | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'
