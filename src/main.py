from typing import List
import chunks
import sys

argsRequired = 2
if (len(sys.argv) < argsRequired):
    raise Exception(f"Missing inputs. required: {argsRequired}")

launchLocation = str(sys.argv[0])

fileBuffers: List[chunks.sbuffer] = []

for i in range(1, len(sys.argv)):
    fileBuffers.append(chunks.buffer(str(sys.argv[i])))

images: List[chunks.image] = []

for fileBuffer in fileBuffers:
    tempImage = chunks.image()
    while (fileBuffer.pos < len(fileBuffer.buffer)):
        tempImage.addChunk(fileBuffer.getChunk())
