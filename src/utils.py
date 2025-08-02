import strings
import constants

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

def splitWordSelectorToken(token):
    index = -1
    splitTokens = token.split('@')
    if len(splitTokens) > 1:
        label = splitTokens[0]
        index = splitTokens[1]
        try:
            index = int(index)
        except:
            abortError(lineCounter, strings.INVALID_PREPROCESSOR_USAGE)

    return splitTokens[0], index

def decodeValue(token, labels):
    label, index = splitWordSelectorToken(token)

    if label in labels:
        value = decodeValue(str(labels[label]), labels)
    else:
        value = decodeNumber(label)
    if index >= 0:
        return fetchNthWord(value, index)
    return value

def fetchNthWord(value, n):
    words = numberToWords(value, (n + 1) * constants.WORD_SIZE, constants.WORD_SIZE)
    if n < len(words):
        return words[0]
    return 0

def wavesciify(string):
    words = []
    for char in string:
        words.append(wavescii.definitions[char])
    words.append(0)  # terminate string
    return words
