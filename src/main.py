#!/bin/python

# kasm (K6/K8 Assembler)
# Part of furry-world project
# Written by qRea, 2025


# TODO:
#   - restructure to be cleaner
#   - maybe implement preprocessor commands (like MADS)
#   - DOCS!!!

import sys
import os.path

import parser


def printUsage():
    print("kasm-k8 v0.3 (alpha)")
    print(f"usage: {sys.argv[0]} <INPUT FILE> [SWITCHES]")
    print()
    print("valid switches:")
    print("   -h          print help")
    print("   -o=<FILE>   specify output file name")


fileNameIn = ""
fileNameOut = ""
arguments = sys.argv[1:]
for arg in arguments:
    if arg.startswith("-h"):
        printUsage()
        sys.exit()

    if arg.startswith("-o="):
        fileNameOut = arg[3:]
        break

    fileNameIn = arg

if fileNameIn == "":
    printUsage()
    sys.exit()

if fileNameOut == "":
    fileNameOut = os.path.basename(fileNameIn).split(".")[0] + ".rom"


rom = parser.parse(fileNameIn)


with open(fileNameOut, "wb") as file:
    for byte in rom:
        file.write(byte.to_bytes(1))
