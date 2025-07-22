#!/usr/bin/env python3
"""
read_write_heap.py

This script searches for a string in the heap of a running process and
replaces it with another string of the same length or less.

Usage:
    sudo ./read_write_heap.py <pid> <search_string> <replace_string>

Note:
    - You must run this as root to access /proc/<pid>/mem.
    - The replacement string must not be longer than the original.
"""

import sys
import os

def usage():
    print("Usage: read_write_heap.py <pid> <search_string> <replace_string>")
    sys.exit(1)

def check_permissions():
    if os.geteuid() != 0:
        print("[!] Error: You must run this script as root.")
        sys.exit(1)

def find_heap(pid):
    """
    Locate the heap segment of the given process from /proc/<pid>/maps.
    """
    try:
        with open(f'/proc/{pid}/maps', 'r') as maps_file:
            for line in maps_file:
                if '[heap]' in line:
                    addr_range = line.split()[0]
                    start_str, end_str = addr_range.split('-')
                    start = int(start_str, 16)
                    end = int(end_str, 16)
                    print(f"[*] Heap found: {hex(start)} - {hex(end)}")
                    return start, end
        print("[!] Heap not found.")
        sys.exit(1)
    except FileNotFoundError:
        print("[!] Process not found.")
        sys.exit(1)

def read_heap(pid, start, end):
    """
    Read the heap memory of the process.
    """
    try:
        with open(f'/proc/{pid}/mem', 'rb') as mem_file:
            mem_file.seek(start)
            return mem_file.read(end - start)
    except PermissionError:
        print("[!] Permission denied when reading memory.")
        sys.exit(1)

def write_heap(pid, address, data):
    """
    Write the modified data into the heap memory of the process.
    """
    try:
        with open(f'/proc/{pid}/mem', 'rb+') as mem_file:
            mem_file.seek(address)
            mem_file.write(data)
    except PermissionError:
        print("[!] Permission denied when writing to memory.")
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        usage()

    check_permissions()

    pid = sys.argv[1]
    search = sys.argv[2].encode()
    replace_raw = sys.argv[3].encode()

    if len(replace_raw) > len(search):
        print("[!] Error: replace_string must not be longer than search_string.")
        sys.exit(1)

    replace = replace_raw.ljust(len(search), b'\x00')  # Pad with null bytes

    start, end = find_heap(pid)
    heap_data = read_heap(pid, start, end)

    count = 0
    offset = 0

    while True:
        index = heap_data.find(search, offset)
        if index == -1:
            break
        abs_address = start + index
        print(f"[+] Found occurrence at {hex(abs_address)} - replacing...")
        write_heap(pid, abs_address, replace)
        count += 1
        offset = index + len(search)

    if count == 0:
        print(f"[!] '{sys.argv[2]}' not found in heap.")
        sys.exit(1)
    else:
        print(f"[✓] Done. Replaced {count} occurrence(s).")

if __name__ == "__main__":
    main()
