import os
import sys
import numpy as np


def checkFileExists(filePath: str):
    if (not os.path.isfile(filePath)):
        raise Exception(f"File error: {filePath}")

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




def GetInt4Chunk(buffer: bytearray, position: int) -> int:
    return int.from_bytes(buffer[position:position + 4], 'big')


def stringBinary(buffer: bytearray, startIndex: int, length: int) -> str:
    stringOut = ""
    for i in range(length):
        stringOut += chr(buffer[startIndex + i])
    return stringOut


class chunk():
    def __init__(self):
        self.length = 0
        self.type = "null"
        self.data = bytearray()
        self.crc = 0

    def setLength(self, length: int):
        self.length = length

    def setType(self, type: str):
        self.type = type

    def setData(self, data: bytearray):
        self.data = data

    def setCRC(self, crc: bytearray):
        self.crc = crc


class buffer():
    def __init__(self, filePath: str):
        checkFileExists(filePath)
        self.buffer = bytearray(open(filePath, "rb").read())
        self.pos = 8

    def getChunk(self) -> chunk:
        chunkOut = chunk()
        chunkOut.setLength(GetInt4Chunk(self.buffer, self.pos))
        self.pos += 4
        chunkOut.setType(stringBinary(self.buffer, self.pos, 4))
        self.pos += 4
        chunkOut.setData(self.buffer[self.pos : self.pos + chunkOut.length])
        self.pos += chunkOut.length
        chunkOut.setCRC(self.buffer[self.pos : self.pos + 4])
        self.pos += 4
        return chunkOut


argsRequired = 2
if (len(sys.argv) < argsRequired):
    raise Exception(f"Missing inputs. required: {argsRequired}")

launchLocation = str(sys.argv[0])
fileArg1 = str(sys.argv[1])

file1 = buffer(fileArg1)
checkPNGHeader(file1.buffer)

counter = 0
while(file1.pos < len(file1.buffer)):
    counter += 1
    _chunk = file1.getChunk()
    print(f"Chunk{counter} ->  Type: {_chunk.type}. Length: {_chunk.length}. CRC: {_chunk.crc}")
print("done!")
