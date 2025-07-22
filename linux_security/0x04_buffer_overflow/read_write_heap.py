#!/usr/bin/python3
"""
read_write_heap.py

Searches and replaces a string in the heap of a running process.
"""

import sys


def find_heap(pid):
    """
    Locate the start and end addresses of the heap in /proc/<pid>/maps.
    Args:
        pid (str): Process ID
    Returns:
        tuple: (start, end) addresses of the heap
    """
    try:
        with open(f'/proc/{pid}/maps', 'r') as f:
            for line in f:
                if '[heap]' in line:
                    addr = line.split(' ')[0]
                    start, end = [int(x, 16) for x in addr.split('-')]
                    return start, end
    except Exception:
        pass
    print("Error: Could not find heap segment")
    sys.exit(1)


def read_heap(pid, start, end):
    """
    Read heap memory from /proc/<pid>/mem.
    Args:
        pid (str): Process ID
        start (int): Start address
        end (int): End address
    Returns:
        bytes: content of the heap
    """
    try:
        with open(f'/proc/{pid}/mem', 'rb') as mem:
            mem.seek(start)
            return mem.read(end - start)
    except Exception:
        print("Error: Cannot read heap memory")
        sys.exit(1)


def write_heap(pid, addr, data):
    """
    Write bytes to a memory address in /proc/<pid>/mem.
    Args:
        pid (str): Process ID
        addr (int): Address to write to
        data (bytes): Bytes to write
    """
    try:
        with open(f'/proc/{pid}/mem', 'rb+') as mem:
            mem.seek(addr)
            mem.write(data)
    except Exception:
        print("Error: Cannot write to heap memory")
        sys.exit(1)


def main():
    """
    Main function to validate args, locate and replace heap string.
    """
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv[1]
    search_str = sys.argv[2]
    replace_str = sys.argv[3]

    if len(replace_str) > len(search_str):
        print("Error: replace_string must not be longer than search_string")
        sys.exit(1)

    search_bytes = search_str.encode()
    replace_bytes = replace_str.encode().ljust(len(search_bytes), b'\x00')

    start, end = find_heap(pid)
    heap = read_heap(pid, start, end)

    idx = heap.find(search_bytes)
    if idx == -1:
        print("Error: search_string not found in heap")
        sys.exit(1)

    write_heap(pid, start + idx, replace_bytes)


if __name__ == "__main__":
    main()
#!/usr/bin/python3
import sys
import os

def usage():
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)

def main():
    if len(sys.argv) != 4:
        usage()

    pid = sys.argv[1]
    search = sys.argv[2]
    replace = sys.argv[3]

    if len(replace) > len(search):
        print("Error: replace_string must not be longer than search_string")
        sys.exit(1)

    maps_file = f"/proc/{pid}/maps"
    mem_file = f"/proc/{pid}/mem"

    if not os.path.exists(maps_file):
        print("Error: process does not exist")
        sys.exit(1)

    try:
        with open(maps_file, "r") as f:
            heap_start = None
            heap_end = None
            for line in f:
                if "[heap]" in line:
                    addr = line.split()[0]
                    heap_start, heap_end = [int(x, 16) for x in addr.split("-")]
                    break
            if heap_start is None:
                print("Error: heap segment not found")
                sys.exit(1)
    except PermissionError:
        print("Error: permission denied")
        sys.exit(1)
    except Exception:
        print("Error: cannot read memory map")
        sys.exit(1)

    try:
        with open(mem_file, "rb+") as mem:
            mem.seek(heap_start)
            heap_data = mem.read(heap_end - heap_start)
            index = heap_data.find(search.encode())
            if index == -1:
                print("Error: search_string not found in heap")
                sys.exit(1)
            mem.seek(heap_start + index)
            mem.write(replace.encode().ljust(len(search), b'\x00'))
    except PermissionError:
        print("Error: permission denied")
        sys.exit(1)
    except Exception:
        print("Error: cannot access memory file")
        sys.exit(1)

if __name__ == "__main__":
    main()
