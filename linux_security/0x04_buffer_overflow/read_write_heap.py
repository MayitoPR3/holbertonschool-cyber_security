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
