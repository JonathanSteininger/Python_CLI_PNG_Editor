from bitarray import bitarray
from enum import Enum


def CRC32(message: bytes) -> bytes:
    poli = getPolinomial32()
    # initiates the CRC bit array that will get manipulated by bitwise operations.
    crc = bitarray('1' * 32)
    # loops through each byte in the message
    for byte in message:
        byteBits = bitarray()
        byteBits.frombytes(byte.to_bytes(1, 'big'))
        crc[:8] ^= byteBits
        for void in range(8):
            if crc[-1]:
                crc = (crc >> 1) ^ poli
            else:
                crc = crc >> 1
    crc = ~crc
    return crc.tobytes()


class Polinomial32():
    Normal = 0x04C11DB7
    Reversed = 0xEDB88320
    reciprocal = 0xDB710641
    reversedReciprocal = 0x82608EDB


def getPolinomial32() -> bitarray:
    poliNum = Polinomial32().Reversed
    polinomialBytes = poliNum.to_bytes(4, 'big')
    polinomialBits = bitarray(endian='big')
    polinomialBits.frombytes(polinomialBytes)
    return polinomialBits
    startingIndex = polinomialBits.find(1)
    polinomialBits = polinomialBits[startingIndex:]
    return polinomialBits
