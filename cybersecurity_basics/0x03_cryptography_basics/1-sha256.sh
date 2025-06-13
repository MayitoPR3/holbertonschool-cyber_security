#!/bin/bash
[ -z "$1" ] && { echo "Usage: $0 <password>"; exit 1; } || echo -n "$1" | sha256sum | awk '{print $1}' > 1_hash.txt
