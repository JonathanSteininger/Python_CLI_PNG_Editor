import os
import sys


def checkFileExists(filePath: str):
    if (not os.path.isfile(filePath)):
        raise Exception(f"File error: {filePath}")


def validateByteChar(byteBuffer: bytearray, bufferIndex: int, charComparison: chr) -> bool:
    if (chr(byteBuffer[bufferIndex]) != charComparison):
        print("Byte invalid. ByteIndex: ", bufferIndex, "Checked Byte: ",
              chr(byteBuffer[bufferIndex]), "Comparison Byte: ", charComparison)
        return False
    return True


def validateByte(byteBuffer: bytearray, bufferIndex: int, byteComparison: bytes) -> bool:
    if (byteBuffer[bufferIndex] != byteComparison[0]):
        print("Byte invalid. ByteIndex: ", bufferIndex, "Checked Byte: ",
              byteBuffer[bufferIndex], "Comparison Byte: ", byteComparison[0])
        return False
    return True


def checkPNGHeader(buffer: bytearray) -> bool:
    output = True
    output = output and validateByte(buffer, 0, b'\x89')
    output = output and validateByteChar(buffer, 1, 'P')
    return output


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


