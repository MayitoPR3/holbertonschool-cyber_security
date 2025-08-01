#!/bin/bash
nmap --script vulners "$1" 80 443
