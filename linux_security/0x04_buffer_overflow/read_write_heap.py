#!/usr/bin/env python3

import sys
import os

def usage():
    print("Usage: read_write_heap.py pid search_string replace_string")
    exit(1)

def main():
    if len(sys.argv) != 4:
        usage()

    pid = sys.argv[1]
    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    if len(replace_str) > len(search_str):
        print("Error: replace_string must not be longer than search_string")
        exit(1)

    try:
        pid_int = int(pid)
    except ValueError:
        print("Error: PID must be an integer")
        exit(1)
    
    try:
        maps_path = f"/proc/{pid}/maps"
        mem_path = f"/proc/{pid}/mem"

        with open(maps_path, 'r') as maps_file:
            heap_region = None
            for line in maps_file:
                if '[heap]' in line:
                    heap_region = line
                    break
            
            if not heap_region:
                print("Error: Heap region not found")
                exit(1)

            addr = heap_region.split(' ')[0]
            start_str, end_str = addr.split('-')
            start = int(start_str, 16)
            end = int(end_str, 16)
            print(f"[+] Heap starts at {hex(start)} and ends at {hex(end)}")

        with open(mem_path, 'rb+') as mem_file:
            mem_file.seek(start)
            heap_data = mem_file.read(end - start)

            index = heap_data.find(search_str.encode())
            if index == -1:
                print(f"[-] '{search_str}' not found in heap")
                exit(1)
            print(f"[+] Found '{search_str}' at offset {hex(start + index)}")

            mem_file.seek(start + index)
            new_data = replace_str.encode() + b'\x00' * (len(search_str) - len(replace_str))
            mem_file.write(new_data)
            print(f"[+] Replaced with '{replace_str}'")

    except FileNotFoundError:
        print("Error: Process does not exist")
        exit(1)

    except PermissionError:
        print("Error: Permission denied. Try running as root.")
        exit(1)

if __name__ == "__main__":
    main()
# This script reads and writes to the heap of a process given its PID.
# It searches for a specific string in the heap and replaces it with another string.    