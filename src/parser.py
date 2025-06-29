import sys

import strings
import constants
import wavescii
import utils

class FutureLabel:
    line = -1
    romOffset = -1
    labelName = ""
    valueSize = -1


# this is to handle labels across methods
labels = {}
futureLabels = []

# HAAAAAAAAAAAAAAACK, needs cleaning up
lineCounter = 0
rom = [constants.FILL_VALUE for x in range(constants.ROM_SIZE)]
romOffset = 0

wordSize = 8

def abortError(line, message):
    print(strings.ERROR_ON_LINE + f" {line}: {message}")
    print(strings.COMPILATION_ABORTED)
    sys.exit(1)


def printdbg(message):
    print(f"DEBUG: {message}")


def registerNameToID(name):
    regid = ord(name)
    if regid >= ord("A") and regid <= ord("H"):
        return regid - ord("A")
    raise Exception("invalid register name")

def wavesciify(string):
    words = []
    for char in string:
        words.append(wavescii.definitions[char])
    words.append(0)  # terminate string
    return words


def registerFutureLabel(labelName, romOffset, valueSize):
    global futureLabels

    futureLabel = FutureLabel()
    futureLabel.line = lineCounter
    futureLabel.romOffset = romOffset
    futureLabel.labelName = labelName
    futureLabel.valueSize = valueSize
    futureLabels.append(futureLabel)
    return 0  # will be masked later, return 0 for now


def populateFutureLabels():
    global labels, futureLabels, rom
    for futureLabel in futureLabels:
        try:
            value = utils.numberToWords(
                utils.decodeValue(futureLabel.labelName, labels), futureLabel.valueSize, wordSize
            )
        except:
            abortError(futureLabel.line, strings.EXPECTED_NUMBER_OR_LABEL)
        for i in range(len(value)):
            if futureLabel.romOffset + i >= constants.ROM_SIZE:
                abortError(lineCounter, strings.OUT_OF_SPACE)
            rom[futureLabel.romOffset + i] |= value[i]


# opcode signature handlers
def instruction_words(opcode, tokens, numWords):
    global romOffset
    words = []
    words.append(opcode)
    try:
        value = utils.decodeValue(tokens[1], labels)
    except:
        registerFutureLabel(tokens[1], romOffset + 1, wordSize * numWords)
        value = 0
    words += utils.numberToWords(value, wordSize * numWords, wordSize)
    return words


def instruction_register(opcode, tokens):
    try:
        reg = registerNameToID(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    opcode |= reg
    return [opcode]


def instruction_registerwords(opcode, tokens, numWords):
    try:
        reg = registerNameToID(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    opcode |= reg
    tokens.pop(1)
    return instruction_words(opcode, tokens, numWords)


def instruction_2registers(opcode, tokens):
    words = []
    words.append(opcode)
    try:
        regx = registerNameToID(tokens[1])
        regy = registerNameToID(tokens[2])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    words.append(regx << 3 | regy)
    return words


def instruction_flag(opcode, tokens):
    try:
        value = utils.decodeValue(tokens[1], labels)
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    opcode |= value % 2
    return [opcode]


def instruction_immediateable(opcode, tokens):
    global romOffset
    words = []

    try:
        reg = registerNameToID(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)

    opcode |= reg

    try:
        if tokens[2][0] == "#":
            immediate = True
        else:
            immediate = False

        if immediate:
            try:
                value = utils.decodeValue(tokens[2][1:], labels)
            except:
                registerFutureLabel(tokens[2][1:], romOffset + 1, wordSize)
        else:
            try:
                value = utils.decodeValue(tokens[2], labels)
            except:
                registerFutureLabel(tokens[2], romOffset + 1, wordSize)
    except:
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)

    if not immediate: opcode |= 0b00001000

    words.append(opcode)
    if immediate:
        words += utils.numberToWords(value, wordSize, wordSize)
    else:
        words += utils.numberToWords(value, wordSize * 2, wordSize)

    return words


def instruction_hybrid(opcodereg, opcodeval, tokens):
    tworeg = False
    try:
        registerNameToID(tokens[2])
        tworeg = True
    except:
        pass

    if tworeg:
        return instruction_2registers(opcodereg, tokens)
    else:
        return instruction_immediateable(opcodeval, tokens)

# directive handlers
def directive_1value(tokens):
    try:
        return utils.decodeValue(tokens[1], labels)
    except:
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)


def directive_listofvalues(tokens):
    values = []
    try:
        for i in tokens[1:]:
            values.append(utils.decodeValue(i, labels))
    except:
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
    return values


def directive_string(line):
    string = ""
    startIndex = line.find('"') + 1
    if startIndex == 0:
        abortError(lineCounter, strings.EXPECTED_STRING)

    terminated = False
    endIndex = len(line)
    currentPos = startIndex
    while currentPos < endIndex:
        if line[currentPos] == "\\":
            currentPos += 1
            match line[currentPos]:
                case "\\":
                    string += "\\"
                case "0":
                    string += "\0"
                case "n":
                    string += "\n"
                case '"':
                    string += '"'
        elif line[currentPos] == '"':
            terminated = True
            break
        else:
            string += line[currentPos]
        currentPos += 1
    if not terminated:
        abortError(lineCounter, strings.STRING_NOT_TERMINATED)
    return string


# actual parsing
def parse(fileNameIn):
    global labels, lineCounter, rom, romOffset
    try:
        with open(fileNameIn, "r") as file:
            sourceFile = file.readlines()
    except:
        abortError(lineCounter, strings.FILE_NOT_FOUND)

    for line in sourceFile:
        lineCounter += 1
        tokens = line.strip().split(" ")
        bytesToAdd = []

        # filter empty tokens
        tokens[:] = [x for x in tokens if x]

        # handle comments
        tokensToKeep = len(tokens)
        for i in range(len(tokens)):
            if tokens[i][0] == ";":
                tokensToKeep = i
                break
        tokensToRemove = len(tokens) - tokensToKeep
        for i in range(tokensToRemove):
            tokens.pop()

        # handle empty lines
        if len(tokens) == 0:
            continue

        # handle labels
        if tokens[0][-1] == ":" or (len(tokens) == 3 and tokens[1] == "="):
            if tokens[0][-1] == ":":
                expectedTokens = 1
                labelName = tokens[0][:-1]
                labelValue = romOffset
            elif tokens[1] == "=":
                expectedTokens = 3
                labelName = tokens[0]
                if len(tokens) < 3:
                    abortError(lineCounter, strings.MISSING_LABEL_VALUE)
                try:
                    labelValue = utils.decodeValue(tokens[2], labels)
                except:
                    abortError(lineCounter, strings.INVALID_LABEL_VALUE)

            if len(tokens) != expectedTokens:
                abortError(lineCounter, strings.INVALID_LABEL_DEFINITION)
            if labelName.isnumeric():
                abortError(lineCounter, strings.LABEL_NAME_CANNOT_BE_NUMERIC)
            if not labelName.isalnum():
                abortError(lineCounter, strings.LABEL_NAME_MUST_BE_ALPHANUMERIC)
            if labelName in labels:
                abortError(lineCounter, strings.DUPLICATE_DEFINITION_OF_LABEL)
            labels[labelName] = labelValue
            continue

        # now, actual instructions.
        instruction = tokens[0].upper()
        match instruction:
            case "CALL":
                bytesToAdd += instruction_words(0b00000000, tokens, 2)

            case "RETURN":
                bytesToAdd.append(0b00000001)

            case "JUMP":
                bytesToAdd += instruction_words(0b00000010, tokens, 2)

            case "RJUMP":
                bytesToAdd += instruction_words(0b00000011, tokens, 1)

            case "INTERRUPT":
                bytesToAdd += instruction_words(0b00001000, tokens, 1)

            case "POP":
                bytesToAdd += instruction_register(0b00100000, tokens)

            case "PUSH":
                bytesToAdd += instruction_register(0b00101000, tokens)


            case "MOVE":
                bytesToAdd += instruction_2registers(0b01000000, tokens)

            case "ILOAD":
                bytesToAdd += instruction_registerwords(0b01001000, tokens, 2)

            case "ISTORE":
                bytesToAdd += instruction_registerwords(0b01011000, tokens, 2)

            case "LOAD":
                bytesToAdd += instruction_immediateable(0b01101000, tokens)

            case "STORE":
                bytesToAdd += instruction_registerwords(0b01111000, tokens, 2)


            case "ADD":
                bytesToAdd += instruction_2registers(0b10001000, tokens)

            case "SUBTRACT":
                bytesToAdd += instruction_2registers(0b10001001, tokens)

            case "OR":
                bytesToAdd += instruction_2registers(0b10001100, tokens)

            case "AND":
                bytesToAdd += instruction_2registers(0b10001110, tokens)

            case "XOR":
                bytesToAdd += instruction_2registers(0b10001111, tokens)

            case "SHIFTL":
                bytesToAdd += instruction_register(0b10010000, tokens)

            case "SHIFTR":
                bytesToAdd += instruction_register(0b10011000, tokens)


            case "EQUAL":
                bytesToAdd += instruction_hybrid(0b11000000, 0b11100000, tokens)

            case "NOTEQUAL":
                bytesToAdd += instruction_hybrid(0b11001000, 0b11110000, tokens)


            # compiler directives
            case "ORIGIN":
                romOffset = directive_1value(tokens)

            case "DATA":
                bytesToAdd = directive_listofvalues(tokens)

            case "STRING":
                try:
                    bytesToAdd = wavesciify(directive_string(line).upper())
                except:
                    abortError(lineCounter, strings.STRING_CONTAINS_ILLEGAL_CHARS)

            case "INCLUDE":
                try:
                    parse(directive_string(line))
                except:
                    abortError(lineCounter, strings.STRING_CONTAINS_ILLEGAL_CHARS)

            case _:
                abortError(lineCounter, strings.UNKNOWN_INSTRUCTION)

        for i in range(len(bytesToAdd)):
            rom[romOffset] = bytesToAdd[i]
            romOffset += 1
            if romOffset >= constants.ROM_SIZE:
                abortError(lineCounter, strings.OUT_OF_SPACE)

    populateFutureLabels()
    return rom
