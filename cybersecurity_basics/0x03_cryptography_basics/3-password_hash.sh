#!/bin/bash
[ -z "$1" ] && { echo "Usage: $0 <password>"; exit 1; } || echo -n "$1$(openssl rand -hex 8)" | openssl dgst -sha512 > 3_hash.txt
