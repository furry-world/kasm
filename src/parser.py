import strings

# this is to handle labels across methods
labels = {}

def abortError(line, message):
    print(strings.ERROR_ON_LINE + f' {line}: {message}')
    print(strings.COMPILATION_ABORTED)
    exit(1)

def printdbg(message):
    print(f'DEBUG: {message}')

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
    if token[0] == "#":
        return int(token[1:])
    if token in labels:
        return decodeValue(str(labels[token]))
    return decodeNumber(token)

def parse(fileNameIn):
    global labels
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
                bytesToAdd.append(0o00)

                try:
                    address = decodeValue(tokens[1])
                except:
                    abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
                
                bytesToAdd += numberToHytes(address, 12)
            
            case 'JUMP':
                bytesToAdd.append(0o01)

                try:
                    address = decodeValue(tokens[1])
                except:
                    abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
                
                bytesToAdd += numberToHytes(address, 12)
            
            case 'RJUMP':
                bytesToAdd.append(0o02)

                try:
                    offset = decodeValue(tokens[1])
                except:
                    abortError(lineCounter, strings.EXPECTED_NUMBER_OR_LABEL)
                
                bytesToAdd += numberToHytes(offset, 6)
            
            case 'RETURN':
                bytesToAdd.append(0o03)

            case _:
                abortError(lineCounter, strings.UNKNOWN_INSTRUCTION)

        rom += bytesToAdd
    
    return rom

    
