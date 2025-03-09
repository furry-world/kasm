#!/bin/python

# KASM (K6 Assembler)
# Part of furry-world project
# Written by qRea, 2025


# TODO:
#   - fix labels not being able to be defined after reference
#   - restructure to be cleaner
#   - implement org, data
#   - maybe implement preprocessor commands (like MADS)

import sys

import parser

def printUsage():
    # TODO: update
    parameters = [
        ("-i=<path>", "Set input file"),
        ("-o=<path>", "Set output file")
    ]

    print("Parameters:")
    for i in parameters:
        print(i[0], "\t", i[1])


romSize = 0

fileNameIn = ""
fileNameOut = "out.gnw"
arguments = sys.argv[1:]
for arg in arguments:
    
    if arg.startswith("-i="):
        fileNameIn = arg[3:]
        break

    if arg.startswith("-o="):
        fileNameOut = arg[3:]
        break
    
    fileNameIn = arg

rom = parser.parse(fileNameIn)

print(rom)

with open(fileNameOut, 'wb') as file:
    for hyte in rom:
        byte = hyte.to_bytes(1)
        file.write(byte)
