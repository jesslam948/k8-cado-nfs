#!/bin/python3
import os
import sys

if len(sys.argv) != 3:
    raise Exception("Please input two log file paths")

f1path = sys.argv[1]
f2path = sys.argv[2]

f1 = open(f1path, "r")
f2 = open(f2path, "r")
f = open("logcat.csv", "w")

f1lines = f1.readlines()
f2lines = f2.readlines()

heading = f"Category, {f1path} time, {f2path} time, extra1, extra2\n"
f.write(heading)

for i in range(len(f1lines)):
    # split into each 'column'
    l1 = f1lines[i].split(":")
    l2 = f2lines[i].split(":")

    category = l1[1]
    temp = category.split(",")
    if len(temp) != 1:
        category = f"{temp[0]} ({temp[1][1:]})"

    num1 = l1[-1]
    num2 = l2[-1]
    
    # cut off \n and leading whitespace
    num1 = num1.split("\n")[0][1:]
    num2 = num2.split("\n")[0][1:]

    # processing
    num1s = num1.split("/")
    num2s = num2.split("/")
    if len(num1s) > 1:
        col1 = num1s[1] + ", " + num2s[1]
        col2 = num1s[0] + ", " + num2s[0]
    elif num1[-1] == 's':
        col1 = num1[:-1] + ", " + num2[:-1]
        col2 = "s" + ", s"
    else:
        col1 = num1
        col2 = num2

    wline = category + ", " + col1 + ", " + col2 + "\n"
    f.write(wline)

f.close()
f1.close()
f2.close()
    
