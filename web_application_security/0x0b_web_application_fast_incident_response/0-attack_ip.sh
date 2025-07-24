#!/bin/bash

# Extract IP addresses, count them, sort by count, print top result
awk '{print $1}' logs.txt | sort | uniq -c | sort -nr | head -n 1 | awk '{print $2}'
