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
import argparse

import parser

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(
        prog='kasm-k8',
        description='kasm-k8 v0.4 (alpha) - Kepler K8 Assembler',
    )

    argParser.add_argument('filename', help='assembly source file to compile')
    argParser.add_argument('-o', '--output', help='set output binary filename')

    arguments = argParser.parse_args(sys.argv[1:])

    fileNameIn = arguments.filename
    fileNameOut = arguments.output

    if fileNameIn is None:
        printUsage()
        sys.exit()

    if fileNameOut is None:
        fileNameOut = os.path.splitext(fileNameIn)[0] + ".rom"


    rom = parser.parse(fileNameIn)


    with open(fileNameOut, "wb") as file:
        for byte in rom:
            file.write(byte.to_bytes(1))
