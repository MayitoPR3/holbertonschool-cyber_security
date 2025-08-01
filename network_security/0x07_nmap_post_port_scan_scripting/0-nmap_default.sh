#!/bin/bash

# Check if target is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <target-host>"
    exit 1
fi

TARGET="$1"

echo "[+] Running Nmap default script scan on: $TARGET"

# Run nmap with default scripts (-sC), service/version detection (-sV), and show reason (-reason)
sudo nmap -sC -sV "$TARGET"
