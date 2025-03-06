import opcodes

def abortError(line, message):
    print(f'ERROR on line {line}: {message}')
    print('Compilation aborted')
    exit(1)

def printdbg(message):
    print(f'DEBUG: {message}')

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

def parse(fileNameIn):
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
        if tokens[0][-1] == ':':
            if len(tokens) > 1:
                abortError(lineCounter, 'unexpected tokens after label definition')
            labels[tokens[0][:-1]] = len(rom)
            continue

        # now, actual instructions.
        instruction = tokens[0].upper()
        printdbg(instruction)
        match instruction:
            case 'CALL':
                bytesToAdd.append(0o00)

                try:
                    address = decodeNumber(tokens[1])
                except:
                    abortError(lineCounter, 'expected a number. Labels are not supported yet :<')
                
                bytesToAdd.append((address >> 6) & 0b111111)
                bytesToAdd.append(address & 0b111111)
            
            case 'JUMP':
                bytesToAdd.append(0o01)

                try:
                    address = decodeNumber(tokens[1])
                except:
                    abortError(lineCounter, 'expected a number. Labels are not supported yet :<')
                
                bytesToAdd.append((address >> 6) & 0b111111)
                bytesToAdd.append(address & 0b111111)
            
            case 'RJUMP':
                bytesToAdd.append(0o02)

                try:
                    offset = decodeNumber(tokens[1])
                except:
                    abortError(lineCounter, 'expected a number. Labels are not supported yet :<')
                
                bytesToAdd.append(offset & 0b111111)
            
            case 'RETURN':
                bytesToAdd.append(0o03)

            case _:
                abortError(lineCounter, 'unknown instruction')
        rom += bytesToAdd
    
    return rom

    
