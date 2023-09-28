from typing import List
import os


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


def validateByte(byteBuffer: bytearray, bufferIndex: int, comparison) -> None:
    inInt = byteBuffer[bufferIndex]
    compInt = returnCharCode(comparison)
    if (inInt != compInt):
        raise Exception(
            f"Byte Failed Validation. BNUM: {bufferIndex}. in: {inInt}. comp: {compInt}")


def getIntFromByte(buffer: bytearray, position: int, size: int) -> int:
    return int.from_bytes(buffer[position:position + 4], 'big')


def stringBinary(buffer: bytearray, startIndex: int, length: int) -> str:
    stringOut = ""
    for i in range(length):
        stringOut += chr(buffer[startIndex + i])
    return stringOut


class chunk():
    def __init__(self) -> None:
        self.length = 0
        self.type = "null"
        self.data = bytearray()
        self.crc = 0

    def setLength(self, length: int) -> None:
        self.length = length

    def setType(self, type: str) -> None:
        self.type = type

    def setData(self, data: bytearray) -> None:
        self.data = data

    def setCRC(self, crc: bytearray) -> None:
        self.crc = crc


class buffer():
    def __init__(self, filePath: str) -> None:
        checkFileExists(filePath)
        self.buffer = bytearray(open(filePath, "rb").read())
        self.checkPNGHeader()
        self.pos = 8

    def checkPNGHeader(self) -> bool:
        HEADER_PNG_BYTES = [b'\x89', 'P', 'N', 'G', '\r', '\n', b'\x1a', '\n']
        for counter in range(len(HEADER_PNG_BYTES)):
            validateByte(self.buffer, counter, HEADER_PNG_BYTES[counter])
        return True

    def getChunk(self) -> chunk:
        chunkOut = chunk()
        byteJumps = 4
        chunkOut.setLength(getIntFromByte(self.buffer, self.pos, byteJumps))
        self.pos += byteJumps
        chunkOut.setType(stringBinary(self.buffer, self.pos, byteJumps))
        self.pos += byteJumps
        chunkOut.setData(self.buffer[self.pos: self.pos + chunkOut.length])
        self.pos += chunkOut.length
        chunkOut.setCRC(self.buffer[self.pos: self.pos + byteJumps])
        self.pos += byteJumps
        return chunkOut


class image():
    def __init__(self) -> None:
        self.chunks: List[chunk] = []

    def addChunk(self, chunk: chunk) -> None:
        self.chunks.append(chunk)

    def containsChunkType(self, type: str) -> bool:
        for _chunk in self.chunks:
            if (_chunk.type == type):
                return True
        return False

    def getChunks(self, type: str) -> List[chunk]:
        chunksOut = []
        for _chunk in self.chunks:
            if (_chunk.type == type):
                chunksOut.append(_chunk)
        return chunksOut


class byteStorage():
    def __init__(self, size: int, signed: bool = False) -> None:
        self.size = size
        self.value = 0
        self.signed = signed

    def setByte(self, bytes: bytes) -> None:
        if (len(bytes) < self.size):
            return
        self.value = int.from_bytes(bytes[:self.size])

    def getByte(self) -> bytes:
        return self.value.to_bytes(self.size, "big", self.signed)


class IHDR():
    def __init__(self, chunk: chunk) -> None:
        self.chunk = chunk
        self.chunkType = b'IHDR'
        self.width = byteStorage(4)
        self.height = byteStorage(4)
        self.bitDepth = byteStorage(1)
        self.colorType = byteStorage(1)
        self.compressionMethod = byteStorage(1)
        self.filterMethod = byteStorage(1)
        self.interlaceMethod = byteStorage(1)

    def readChunk(self) -> None:
        pos = 0
        byteJumps = 4
        self.width.setByte(self.chunk.data[pos:pos + byteJumps])
        pos += byteJumps
        self.height.setByte(self.chunk.data[pos:pos + byteJumps])
        pos += byteJumps
        byteJumps = 1
        self.bitDepth.setByte(self.chunk.data[pos:pos + byteJumps])
        pos += byteJumps
        self.colorType.setByte(self.chunk.data[pos:pos + byteJumps])
        pos += byteJumps
        self.compressionMethod.setByte(self.chunk.data[pos:pos + byteJumps])
        pos += byteJumps
        self.filterMethod.setByte(self.chunk.data[pos:pos + byteJumps])
        pos += byteJumps
        self.interlaceMethod.setByte(self.chunk.data[pos:pos + byteJumps])

    def writeChunk(self) -> bytes:
        bytesOut = bytearray()
        data = self.writeData()
        dataLength = len(data).to_bytes(4, "big", False)
        bytesOut.append(dataLength)
        bytesOut.append(self.chunkType)
        bytesOut.append(data)
        bytesOut.append(self.writeCRC())
        return bytes(bytesOut)

    def writeCRC(self) -> bytes:
        bytesOut = bytearray()
        # need to finish this
        return bytes(bytesOut)

    def writeData(self) -> bytes:
        bytesOut = bytearray()
        bytesOut.append(self.width.getByte())
        bytesOut.append(self.height.getByte())
        bytesOut.append(self.bitDepth.getByte())
        bytesOut.append(self.colorType.getByte())
        bytesOut.append(self.compressionMethod.getByte())
        bytesOut.append(self.filterMethod.getByte())
        bytesOut.append(self.interlaceMethod.getByte())
        return bytes(bytesOut)
