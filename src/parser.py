import strings

# this is to handle labels across methods
labels = {}

# HAAAAAAAAAAAAAAACK, needs cleaning up
lineCounter = 0

def abortError(line, message):
    print(strings.ERROR_ON_LINE + f' {line}: {message}')
    print(strings.COMPILATION_ABORTED)
    exit(1)

def printdbg(message):
    print(f'DEBUG: {message}')

def registerNameToID(name):
    regid = ord(name)
    if regid >= ord('A') and regid <= ord('H'):
        return regid - ord('A')
    raise Exception('invalid register name')

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
        case '%':
            # binary number
            number = int(token[1:], 2)
        case '!':
            # octal number
            number = int(token[1:], 8)
        case '$':
            # hexadecimal number
            number = int(token[1:], 16)
        case _:
            # decimal number
            number = int(token)
    return number

def decodeValue(token):
    global labels
    if token in labels:
        return decodeValue(str(labels[token]))
    return decodeNumber(token)


# opcode signature handlers
def instruction_1hyte(opcode, tokens):
    hytes = []
    hytes.append(opcode)
    try:
        value = decodeValue(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
    hytes += numberToHytes(value, 6)
    return hytes

def instruction_2hyte(opcode, tokens):
    hytes = []
    hytes.append(opcode)
    try:
        value = decodeValue(tokens[1])
    except:
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
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
    hytes = []
    hytes.append(opcode)
    try:
        reg = registerNameToID(tokens[1])
        if tokens[2][0] == '#':
            immediate = True
            value = decodeValue(tokens[2][1:])
        else:
            immediate = False
            value = decodeValue(tokens[2])
    except:
        abortError(lineCounter, strings.EXPECTED_REGISTER_NUMBER_OR_VALUE)
    hytes += numberToHytes(value, 8)
    hytes[1] |= reg << 3
    if immediate: hytes[1] |= 0b000100
    return hytes

def instruction_hybrid(opcodereg, opcodeval, tokens):
    tworeg = False
    try:
        registerNameToID(tokens[2])
        tworeg = True
    except:
        pass

    if tworeg: return instruction_2registers(opcodereg, tokens)
    else: return instruction_regivalue(opcodeval, tokens)

def instruction_reg2hyte(opcode, tokens):
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
        abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
    hytes += numberToHytes(value, 12)
    return hytes

# actual parsing
def parse(fileNameIn):
    global labels, lineCounter
    rom = []
    labels = {}
    with open(fileNameIn, 'r') as file:
        sourceFile = file.readlines()

    lineCounter = 0
    for line in sourceFile:
        lineCounter += 1
        printdbg(lineCounter)
        tokens = line.strip().split(' ')
        bytesToAdd = []
        printdbg(line)
        printdbg(tokens)

        # filter empty tokens
        tokens[:] = [x for x in tokens if x]
        printdbg(tokens)

        # handle comments
        tokensToKeep = len(tokens)
        for i in range(len(tokens)):
            if tokens[i][0] == ';':
                tokensToKeep = i
                break
        tokensToRemove = len(tokens) - tokensToKeep
        for i in range(tokensToRemove):
            tokens.pop()

        # handle empty lines
        if len(tokens) == 0: continue

        # handle labels
        if tokens[0][-1] == ':' or (len(tokens) == 3 and tokens[1] == '='):
            if tokens[0][-1] == ':':
                expectedTokens = 1
                labelName = tokens[0][:-1]
                labelValue = len(rom)
            elif tokens[1] == '=':
                expectedTokens = 3
                labelName = tokens[0]
                if len(tokens) < 3: abortError(lineCounter, strings.MISSING_LABEL_VALUE)
                try:
                    labelValue = decodeValue(tokens[2])
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
        printdbg(instruction)
        match instruction:
            case 'CALL':
                bytesToAdd += instruction_2hyte(0o00, tokens)
            
            case 'JUMP':
                bytesToAdd += instruction_2hyte(0o01, tokens)
            
            case 'RJUMP':
                bytesToAdd += instruction_1hyte(0o02, tokens)
            
            case 'RETURN':
                bytesToAdd.append(0o03)

            case 'ADD':
                bytesToAdd += instruction_2registers(0o13, tokens)

            case 'SUBTRACT':
                bytesToAdd += instruction_2registers(0o14, tokens)

            case 'OR':
                bytesToAdd += instruction_2registers(0o15, tokens)

            case 'AND':
                bytesToAdd += instruction_2registers(0o16, tokens)

            case 'XOR':
                bytesToAdd += instruction_2registers(0o17, tokens)

            case 'SHIFTL':
                bytesToAdd += instruction_register(0o20, tokens)

            case 'SHIFTR':
                bytesToAdd += instruction_register(0o21, tokens)

            case 'LOAD':
                bytesToAdd += instruction_hybrid(0o12, 0o06, tokens)

            case 'STORE':
                bytesToAdd += instruction_regivalue(0o07, tokens)

            case 'EQUAL':
                bytesToAdd += instruction_hybrid(0o10, 0o04, tokens)

            case 'NOTEQUAL':
                bytesToAdd += instruction_hybrid(0o11, 0o05, tokens)

            case 'PLOAD':
                bytesToAdd += instruction_reg2hyte(0o4, tokens)

            case 'PSTORE':
                bytesToAdd += instruction_reg2hyte(0o5, tokens)

            case _:
                abortError(lineCounter, strings.UNKNOWN_INSTRUCTION)

        rom += bytesToAdd
    
    return rom

    
