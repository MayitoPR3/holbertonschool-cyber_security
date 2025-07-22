#!/usr/bin/python3
import sys


def usage():
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)


def main():
    if len(sys.argv) != 4:
        usage()

    pid = sys.argv[1]
    search = sys.argv[2].encode()
    replace = sys.argv[3].encode()

    if len(replace) > len(search):
        print("Error: replace_string must not be longer than search_string")
        sys.exit(1)

    try:
        with open(f"/proc/{pid}/maps") as maps:
            for line in maps:
                if "[heap]" in line:
                    addr = line.split()[0]
                    start, end = [int(x, 16) for x in addr.split("-")]
                    break
            else:
                print("Error: heap segment not found")
                sys.exit(1)
    except Exception:
        print("Error: cannot open maps file")
        sys.exit(1)

    try:
        with open(f"/proc/{pid}/mem", "rb+") as mem:
            mem.seek(start)
            heap = mem.read(end - start)
            index = heap.find(search)

            if index == -1:
                print("Error: search_string not found in heap")
                sys.exit(1)

            mem.seek(start + index)
            mem.write(replace.ljust(len(search), b'\x00'))
    except Exception:
        print("Error: cannot access memory file")
        sys.exit(1)


if __name__ == "__main__":
    main()
