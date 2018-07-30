#!/bin/bash
if [ $(ps aux | grep 'ropehelper.py' | grep -v grep | wc -w) -gt 0 ] ;
then
echo "Script running" ;
exit
fi
python3 /opt/scripts/ropehelper/ropehelper.py
