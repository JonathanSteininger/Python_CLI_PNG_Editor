from bitarray import bitarray


def CRC32(message: bytes) -> bytes:
    poli = getPolinomial32()
    crc = bitarray('1' * 32)
    for byte in message:
        byteBits = bitarray()
        byteByte = byte.to_bytes(1, 'big')
        byteBits.frombytes(byteByte)
        crc[:8] ^= byteBits
        for void in range(8):
            if crc[-1]:
                crc = (crc >> 1) ^ poli
            else:
                crc = crc >> 1
    crc = ~crc
    return crc.tobytes()


def CRC(message: bytes) -> bytes:
    messageBits = bitarray(endian='big')
    messageBits.frombytes(message)
    polinomial = getPolinomial32()
    outBits = runCRCOperation(messageBits, polinomial)
    desiredLen = 8 * 4
    outBits = padBits(outBits, desiredLen)
    outBits = ~outBits
    return outBits.tobytes()


def padBits(bitsIn: bitarray, length: int) -> bitarray:
    lenBitsIn = len(bitsIn)
    if (lenBitsIn >= length):
        return bitsIn
    diffLength = length - lenBitsIn
    outBits = bitarray(diffLength)
    outBits.setall(0)
    outBits.extend(bitsIn)
    return outBits


def getPolinomial32() -> bitarray:
    normal = 0x04C11DB7
    reversed = 0xEDB88320
    reciprocal = 0xDB710641
    reversedReciprocal = 0x82608EDB
    polinomialBytes = reversed.to_bytes(4, 'big')
    polinomialBits = bitarray(endian='big')
    polinomialBits.frombytes(polinomialBytes)
    return polinomialBits
    startingIndex = polinomialBits.find(1)
    polinomialBits = polinomialBits[startingIndex:]
    return polinomialBits


def runCRCOperation(message: bitarray, poli: bitarray) -> bitarray:
    lengthMessage = len(message)
    lengthPoli = len(poli)
    message.extend('0' * (lengthPoli - 1))
    for pos in range(lengthMessage):
        if (message[pos] == 1):
            message[pos:pos + lengthPoli] ^= poli
    finalBits = message[lengthMessage:]
    return finalBits
