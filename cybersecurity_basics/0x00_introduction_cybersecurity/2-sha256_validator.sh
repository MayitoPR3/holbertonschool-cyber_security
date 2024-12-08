#!/bin/bash
echo "$(sha256sum "$1" | cut -d ' ' -f 1)" == "$2" && echo "$1: OK" || echo "$1: FAILED"
