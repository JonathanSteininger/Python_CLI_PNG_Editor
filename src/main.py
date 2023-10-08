from typing import List
import chunks
import sys

argsRequired = 2
if (len(sys.argv) < argsRequired):
    raise Exception(f"Missing inputs. required: {argsRequired}")

launchLocation = str(sys.argv[0])

fileBuffers: List[chunks.buffer] = []

for i in range(1, len(sys.argv)):
    fileBuffers.append(chunks.buffer(str(sys.argv[i])))

images: List[chunks.image] = []

for fileBuffer in fileBuffers:
    tempImage = chunks.image()
    while (fileBuffer.pos < len(fileBuffer.buffer)):
        tempImage.addChunk(fileBuffer.getChunk())
    images.append(tempImage)

typeChunk = "IHDR"
for image in images:
    image.containsChunkType(typeChunk)
    print("IHDR BEFORE")
    tempChunk = image.getChunks(typeChunk)[0]
    print(tempChunk.crc, len(tempChunk.crc))

    temp = chunks.ihdr(tempChunk)
    
    chunkOut = temp.writeChunk()
