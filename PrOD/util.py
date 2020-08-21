# util.py

import oead
import struct

# A function for checking if a file is yaz0 compressed and then determining whether or not to decompress it based off of that
def checkCompression(fileCheck):
    fileInRead = fileCheck
    if (oead.yaz0.get_header(fileInRead) is not None):
        uncompressedFile = oead.yaz0.decompress(fileInRead)
    else:
        uncompressedFile = fileInRead
    return(uncompressedFile)

# Very short function to partially emulate C's 'ReadInt32' function
def readInt32(bytesIn):
    bytesOut = int.from_bytes(bytesIn, byteorder='big', signed=True)
    return(bytesOut)

def writeInt32(intIn):
    bytesOut = intIn.to_bytes(4, 'big', signed=True)
    return(bytesOut)

def readFloat(bytesIn):
    [bytesOut] = struct.unpack('>f', bytesIn)
    return(bytesOut)

def writeFloat(floatIn):
    bytesOut = struct.pack('>f', round(floatIn, 5))
    return(bytesOut)

def newKeyIndx(keyList):
    if bool(keyList) != False:
        newKey = int(keyList[-1]) + 1
    else:
        newKey = int(0)
    return(newKey)