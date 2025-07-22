#!/usr/bin/env python3
import sys
import os

def usage():
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)

def find_heap_region(pid):
    try:
        with open(f"/proc/{pid}/maps", 'r') as f:
            for line in f:
                if '[heap]' in line:
                    addr = line.split(' ')[0]
                    start, end = [int(x, 16) for x in addr.split('-')]
                    return start, end
    except Exception:
        pass
    print("Error: could not find heap segment")
    sys.exit(1)

def read_heap(pid, start, end):
    try:
        with open(f"/proc/{pid}/mem", 'rb') as mem:
            mem.seek(start)
            return mem.read(end - start)
    except Exception:
        print("Error: could not read process memory")
        sys.exit(1)

def write_heap(pid, address, data):
    try:
        with open(f"/proc/{pid}/mem", 'rb+') as mem:
            mem.seek(address)
            mem.write(data)
    except Exception:
        print("Error: could not write to process memory")
        sys.exit(1)

def main():
    if len(sys.argv) != 4:
        usage()

    try:
        pid = int(sys.argv[1])
    except ValueError:
        usage()

    search = sys.argv[2].encode()
    replace = sys.argv[3].encode()

    if len(replace) > len(search):
        print("Error: replace_string must not be longer than search_string")
        sys.exit(1)

    start, end = find_heap_region(pid)
    heap = read_heap(pid, start, end)

    index = heap.find(search)
    if index == -1:
        print(f"Error: '{sys.argv[2]}' not found in heap")
        sys.exit(1)

    addr = start + index
    replace = replace.ljust(len(search), b'\x00')
    write_heap(pid, addr, replace)

if __name__ == "__main__":
    main()
