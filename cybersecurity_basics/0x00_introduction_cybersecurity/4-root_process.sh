#!/bin/bash
ps -u "$1" -eo pid,vsz,rss,cmd --sort=pid | grep -v ' 0  0 ' | grep -v ' 0   0 ' 
