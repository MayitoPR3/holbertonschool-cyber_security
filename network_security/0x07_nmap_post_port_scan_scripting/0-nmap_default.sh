#!/bin/bash
TARGET="$1"
sudo nmap -sC -sV "$TARGET"
