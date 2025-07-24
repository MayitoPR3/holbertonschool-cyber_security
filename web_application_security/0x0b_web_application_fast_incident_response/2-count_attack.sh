#!/bin/bash

# Identify the IP address with the most requests (assumed to be the attacker).
attacker_ip=$(awk '{print $1}' logs.txt | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}')

# Count the total number of requests made by that IP address.
grep -c "^$attacker_ip" logs.txt
