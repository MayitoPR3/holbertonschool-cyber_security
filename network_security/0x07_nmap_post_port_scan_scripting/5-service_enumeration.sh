#!/bin/bash
nmap -sS -sV -O -A --script banner* ssl-enum-ciphers* default* smb-os-discovery* "$1" -oN service_enumeration_results.txt
