import os
import sys
import numpy as np


def checkFileExists(filePath: str):
    if (not os.path.isfile(filePath)):
        raise Exception(f"File error: {filePath}")


def validateByteChar(byteBuffer: bytearray, bufferIndex: int, charComparison: chr) -> bool:
    if (chr(byteBuffer[bufferIndex]) != charComparison):
        print("Byte invalid. ByteIndex: ", bufferIndex, "Checked Byte: ",
              chr(byteBuffer[bufferIndex]), "Comparison Byte: ", charComparison)
        return False
    return True


def returnCharCode(input) -> int:
    if isinstance(input, str):
        if (len(input) <= 0):
            raise Exception("Input string is empty")
        return ord(input[0])
    if isinstance(input, bytes):
        return input[0]
    if isinstance(input, int):
        return input
    if isinstance(input, float):
        return int(input)
    raise TypeError("input not recognised")


def validateByte(byteBuffer: bytearray, bufferIndex: int, comparison) -> bool:
    inInt = byteBuffer[bufferIndex]
    compInt = returnCharCode(comparison)
    if (inInt != compInt):
        raise Exception(
            f"Byte Failed Validation. BNUM: {bufferIndex}. in: {inInt}. comp: {compInt}")


HEADER_PNG_BYTES = [b'\x89', 'P', 'N', 'G', '\r', '\n', b'\x1a', '\n']


def checkPNGHeader(buffer: bytearray) -> bool:
    for counter in range(len(HEADER_PNG_BYTES)):
        validateByte(buffer, counter, HEADER_PNG_BYTES[counter])
    return True


argsRequired = 2
if (len(sys.argv) < argsRequired):
    raise Exception(f"Missing inputs. required: {argsRequired}")

launchLocation = str(sys.argv[0])
fileArg1 = str(sys.argv[1])
# fileArg2 = str(sys.argv[2])

checkFileExists(fileArg1)

buffer1 = bytearray(open(fileArg1, "rb").read())
out = checkPNGHeader(buffer1)
print("header: ", out)
