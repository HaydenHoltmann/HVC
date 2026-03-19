#!/bin/bash

pyinstaller main.py -n "hvc" --onefile

rm hvc

mv dist/hvc hvc

./hvc status
