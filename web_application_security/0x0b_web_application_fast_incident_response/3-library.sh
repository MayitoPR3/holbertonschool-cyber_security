#!/bin/bash

attacker_ip=$(awk '{print $1}' logs.txt | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}')

# Filter the log for requests made by the attacker.
awk -v ip="$attacker_ip" -F'"' '$1 ~ ip {print $6}' logs.txt | sort | uniq -c | sort -nr | head -n 1 | awk '{$1=""; print $0}' | sed 's/^ *//'
