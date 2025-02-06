#!/bin/bash
pwd="$1"
pwd="${pwd#'{xor}'}"
decopwd=$(echo "$pwd" | base64 -d)

decopwdxor=""
for ((i = 0; i < ${#decopwd}; i++)); do
    char="${decopwd:$i:1}"
    ascii_value=$(printf "%d" "'$char")
    xor_result=$(( ascii_value ^ 95 ))
    decopwdxor+="$(printf "$(printf '\\x%x' $xor_result)")"
done

echo -e "$decopwdxor"
