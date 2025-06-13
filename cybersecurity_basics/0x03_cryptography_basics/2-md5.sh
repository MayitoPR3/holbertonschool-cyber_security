#!/bin/bash
[ -z "$1" ] && { echo "Usage: $0 <password>"; exit 1; } || echo -n "$1" | md5sum | awk '{print $1}' > 2_hash.txt