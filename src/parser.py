import sys

import strings
import constants
import wavescii


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


def numberToHytes(value, bits):
    numFullHytes = bits // 6
    numLeftoverBits = bits % 6

    hytes = []
    for i in range(numFullHytes):
        hytes.append(value % 64)
        value //= 64

    if numLeftoverBits > 0:
        mask = (2**numLeftoverBits) - 1
        hytes.append(value & mask)

    # reverse because little-endian
    hytes.reverse()
    return hytes


def decodeNumber(token):
    match token[0]:
        case "%":
            # binary number
            number = int(token[1:], 2)
        case "!":
            # octal number
            number = int(token[1:], 8)
        case "$":
            # hexadecimal number
            number = int(token[1:], 16)
        case _:
            # decimal number
            number = int(token)
    return number


def decodeValue(token):
    global labels, lineCounter

    label = token
    index = -1
    splitTokens = token.split('@')
    if len(splitTokens) > 1:
        label = splitTokens[0]
        index = splitTokens[1]
        try:
            index = int(index)
        except:
            abortError(lineCounter, strings.INVALID_PREPROCESSOR_USAGE)
    if label in labels:
        value = decodeValue(str(labels[label]))
    else:
        value = decodeNumber(label)
    if index >= 0:
        return fetchNthWord(value, index)
    return value

def fetchNthWord(value, n):
    words = numberToHytes(value, (n + 1) * 6)
    if n < len(words):
        return words[0]
    return 0

def wavesciify(string):
    hytes = []
    for char in string:
        hytes.append(wavescii.definitions[char])
    hytes.append(0)  # terminate string
    return hytes


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
            value = numberToHytes(
                decodeValue(futureLabel.labelName), futureLabel.valueSize
            )
        except:
            abortError(futureLabel.line, strings.EXPECTED_NUMBER_OR_LABEL)
        for i in range(len(value)):
            if futureLabel.romOffset + i >= constants.ROM_SIZE:
                abortError(lineCounter, strings.OUT_OF_SPACE)
            rom[futureLabel.romOffset + i] |= value[i]


# opcode signature handlers
def instruction_1hyte(opcode, tokens):
    global romOffset
    hytes = []
    hytes.append(opcode)
    try:
        value = decodeValue(tokens[1])
    except:
        registerFutureLabel(tokens[1], romOffset + 1, 6)
        value = 0
    hytes += numberToHytes(value, 6)
    return hytes


def instruction_2hyte(opcode, tokens):
    global romOffset
    hytes = []
    hytes.append(opcode)
    try:
        value = decodeValue(tokens[1])
    except:
        registerFutureLabel(tokens[1], romOffset + 1, 12)
        value = 0
    hytes += numberToHytes(value, 12)
    return hytes


def instruction_register(opcode, tokens):
    hytes = []
    hytes.append(opcode)
    try:
        reg = registerNameToID(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    hytes.append(reg << 3)
    return hytes


def instruction_2registers(opcode, tokens):
    hytes = []
    hytes.append(opcode)
    try:
        regx = registerNameToID(tokens[1])
        regy = registerNameToID(tokens[2])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    hytes.append(regx << 3 | regy)
    return hytes


def instruction_regivalue(opcode, tokens):
    global romOffset
    hytes = []
    hytes.append(opcode)
    try:
        reg = registerNameToID(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    try:
        if tokens[2][0] == "#":
            immediate = True
            value = decodeValue(tokens[2][1:])
        else:
            immediate = False
            value = decodeValue(tokens[2])
    except:
        try:
            if tokens[2][0] == "#":
                immediate = True
                registerFutureLabel(tokens[2][1:], romOffset + 1, 8)
            else:
                immediate = False
                registerFutureLabel(tokens[2], romOffset + 1, 8)
            value = 0
        except:
            abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
    hytes += numberToHytes(value, 8)
    hytes[1] |= reg << 3
    if not immediate:
        hytes[1] |= 0b000100
    return hytes


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
        return instruction_regivalue(opcodeval, tokens)


def instruction_reg2hyte(opcode, tokens):
    global romOffset
    hytes = []
    hytes.append(opcode << 3)
    try:
        reg = registerNameToID(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_VALID_REGISTER)
    hytes[0] |= reg
    try:
        value = decodeValue(tokens[2])
    except:
        registerFutureLabel(tokens[2], romOffset + 1, 12)
        value = 0
    hytes += numberToHytes(value, 12)
    return hytes


# directive handlers
def directive_1value(tokens):
    try:
        return decodeValue(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)


def directive_listofvalues(tokens):
    values = []
    try:
        for i in tokens[1:]:
            values.append(decodeValue(i))
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


def directive_bininclude(fileNameIn):
    try:
        with open(fileNameIn, "rb") as file:
            sourceFile = file.read()
    except:
        abortError(lineCounter, strings.FILE_NOT_FOUND)

    bytesToAdd = []
    for i in sourceFile:
        bytesToAdd.append(int(i))

    return bytesToAdd


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
                labelValue = decodeValue(tokens[2])
                try:
                    labelValue = decodeValue(tokens[2])
                except:
                    abortError(lineCounter, strings.INVALID_LABEL_VALUE)

            # prob hacky, fix pls
            atIndex = labelName.find('@')
            if atIndex >= 0: labelName = labelName[0:atIndex]

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
                bytesToAdd += instruction_2hyte(0o00, tokens)

            case "JUMP":
                bytesToAdd += instruction_2hyte(0o01, tokens)

            case "RJUMP":
                bytesToAdd += instruction_1hyte(0o02, tokens)

            case "RETURN":
                bytesToAdd.append(0o03)

            case "ADD":
                bytesToAdd += instruction_2registers(0o13, tokens)

            case "SUBTRACT":
                bytesToAdd += instruction_2registers(0o14, tokens)

            case "OR":
                bytesToAdd += instruction_2registers(0o15, tokens)

            case "AND":
                bytesToAdd += instruction_2registers(0o16, tokens)

            case "XOR":
                bytesToAdd += instruction_2registers(0o17, tokens)

            case "SHIFTL":
                bytesToAdd += instruction_register(0o20, tokens)

            case "SHIFTR":
                bytesToAdd += instruction_register(0o21, tokens)

            case "LOAD":
                bytesToAdd += instruction_hybrid(0o12, 0o06, tokens)

            case "STORE":
                bytesToAdd += instruction_regivalue(0o07, tokens)

            case "ILOAD":
                bytesToAdd += instruction_regivalue(0o22, tokens)

            case "ISTORE":
                bytesToAdd += instruction_regivalue(0o23, tokens)

            case "NPLOAD":
                bytesToAdd += instruction_regivalue(0o24, tokens)

            case "NPSTORE":
                bytesToAdd += instruction_regivalue(0o25, tokens)

            case "EQUAL":
                bytesToAdd += instruction_hybrid(0o10, 0o04, tokens)

            case "NOTEQUAL":
                bytesToAdd += instruction_hybrid(0o11, 0o05, tokens)

            case "PLOAD":
                bytesToAdd += instruction_reg2hyte(0o4, tokens)

            case "PSTORE":
                bytesToAdd += instruction_reg2hyte(0o5, tokens)

            case "IPLOAD":
                bytesToAdd += instruction_reg2hyte(0o6, tokens)

            case "IPSTORE":
                bytesToAdd += instruction_reg2hyte(0o7, tokens)

            # compiler directives
            case "ORIGIN":
                romOffset = directive_1value(tokens)

            case "DATA":
                bytesToAdd += directive_listofvalues(tokens)

            case "STRING":
                try:
                    bytesToAdd += wavesciify(directive_string(line).upper())
                except:
                    abortError(lineCounter, strings.STRING_CONTAINS_ILLEGAL_CHARS)

            case "INCLUDE":
                try:
                    parse(directive_string(line))
                except:
                    abortError(lineCounter, strings.STRING_CONTAINS_ILLEGAL_CHARS)

            case "INCLUDEBINARY":
                try:
                    bytesToAdd += directive_bininclude(directive_string(line))
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
