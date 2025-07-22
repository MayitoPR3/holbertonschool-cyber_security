#!/usr/bin/python3
import sys
import os


def main():
    if len(sys.argv) != 4:
        print("Usage: read_write_heap.py pid search_string replace_string")
        sys.exit(1)

    pid = sys.argv[1]
    search_string = sys.argv[2]
    replace_string = sys.argv[3]

    if len(replace_string) > len(search_string):
        print("Error: replace_string must not be longer than search_string")
        sys.exit(1)

    maps_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    try:
        with open(maps_path, "r") as maps_file:
            heap_found = False
            for line in maps_file:
                if "[heap]" in line:
                    heap_found = True
                    addresses = line.split(" ")[0]
                    start_addr, end_addr = [int(addr, 16) for addr in addresses.split("-")]
                    break
            if not heap_found:
                print("Error: heap segment not found")
                sys.exit(1)
    except FileNotFoundError:
        print("Error: process does not exist")
        sys.exit(1)
    except PermissionError:
        print("Error: permission denied")
        sys.exit(1)
    except Exception:
        print("Error: cannot read memory map")
        sys.exit(1)

    try:
        with open(mem_path, "rb+") as mem_file:
            mem_file.seek(start_addr)
            heap_data = mem_file.read(end_addr - start_addr)

            index = heap_data.find(search_string.encode())
            if index == -1:
                print("Error: search_string not found in heap")
                sys.exit(1)

            mem_file.seek(start_addr + index)
            padded = replace_string.encode().ljust(len(search_string), b'\x00')
            mem_file.write(padded)
    except PermissionError:
        print("Error: permission denied")
        sys.exit(1)
    except Exception:
        print("Error: cannot access memory file")
        sys.exit(1)


if __name__ == "__main__":
    main()
