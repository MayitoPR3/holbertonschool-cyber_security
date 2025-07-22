#!/usr/bin/python3
import sys
import os


def usage():
    print("Usage: read_write_heap.py pid search_string replace_string")
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

    maps_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    # 1. Check that process and maps file exist
    if not os.path.exists(maps_path):
        print("Error: process does not exist")
        sys.exit(1)

    # 2. Find heap segment
    try:
        with open(maps_path, 'r') as maps:
            for line in maps:
                if "[heap]" in line:
                    addr = line.split()[0]
                    start, end = [int(x, 16) for x in addr.split("-")]
                    break
            else:
                print("Error: heap segment not found")
                sys.exit(1)
    except Exception:
        print("Error: cannot read memory map")
        sys.exit(1)

    # 3. Open memory and search
    try:
        with open(mem_path, 'rb+') as mem:
            mem.seek(start)
            heap = mem.read(end - start)

            index = heap.find(search)
            if index == -1:
                print("Error: search_string not found in heap")
                sys.exit(1)

            mem.seek(start + index)
            mem.write(replace.ljust(len(search), b'\x00'))
    except PermissionError:
        print("Error: permission denied")
        sys.exit(1)
    except Exception:
        print("Error: cannot access memory file")
        sys.exit(1)


if __name__ == "__main__":
    main()
