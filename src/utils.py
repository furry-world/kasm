def numberToWords(value, bits, wordSize, isLittleEndian = True):
    numValuesInWord = 2**wordSize
    numFullWords = bits // wordSize
    numLeftoverBits = bits % wordSize

    words = []
    for i in range(numFullWords):
        words.append(value % numValuesInWord)
        value //= numValuesInWord

    if numLeftoverBits > 0:
        mask = (2**numLeftoverBits) - 1
        words.append(value & mask)

    if isLittleEndian:
        words.reverse()

    return words


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

def decodeValue(token, labels):
    if token in labels:
        return decodeValue(str(labels[token]), labels)
    return decodeNumber(token)
