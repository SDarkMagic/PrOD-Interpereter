# bwlp.py

import oead
import io
import readchar
from PrOD import util

def decode(fileIn):
    readFile = open(fileIn, 'rb').read()
    uncompressedFile = util.checkCompression(readFile)
    fileStream = io.BytesIO(uncompressedFile)
    magic = fileStream.read(4)
    unknown0 = fileStream.read(4)
    unknown1 = fileStream.read(4)
    unknown2 = fileStream.read(4)
    fileSize = fileStream.read(4)
    entryCount = list(range(util.readInt32(fileStream.read(4))))
    stringTableOffset = util.readInt32(fileStream.read(4))
    padding = fileStream.read(4)
#    fileArray = bytearray(fileStream.read(4))
    firstIter = True
    iterCount = int(0)
    instList = []
    print(f'magic: {magic} unknown0: {unknown0} unknown1: {unknown1} unknown2: {unknown2} padding: {padding}')
    
    if magic == b'PrOD':
        if (
            unknown0 == b'\x01\00\00\00'
            and
            unknown1 == b'\x00\00\00\01'
            and
            padding == b'\x00\00\00\00'
        ):
            print(len(entryCount))
            for entry in entryCount:
                if iterCount < len(entryCount):
                    iterCount += 1
                    size = fileStream.read(4)
                    instanceCount = list(range(util.readInt32(fileStream.read(4))))
                    stringOffset = util.readInt32(fileStream.read(4))
                    testVar = util.readInt32(fileStream.read(4))
#                    print(testVar)
                    if testVar == 0:
#                        print('continuing')
                        currentStreamPos = fileStream.tell()
                        print(currentStreamPos)
                        fileStream.seek(int(stringTableOffset + stringOffset))
                        """
                        if firstIter == True:
                            unknown3 = fileStream.read(8)
                            firstIter = False
                        else:
                            unknown3 = fileStream.read(8)
                        """
                        instanceName = str(fileStream.read().decode('ANSI')).partition('\x00')[0]
#                        print(instanceName)
                        instanceHeader = {instanceName: {}}
                        fileStream.seek(currentStreamPos)
                        subIterCount = int(0)
                        print(instanceCount)
                        for instance in instanceCount:
                            if subIterCount < len(instanceCount):
                                subIterCount += 1
                                instanceLists = {}
                                translate = [util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4))]
                                rotation = [util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4))]
                                scale = util.readFloat(fileStream.read(4))
                                instanceLists.update({'translate': translate, 'rotation': rotation, 'scale': scale})
                                instanceHeader.update({instanceName: instanceLists})
                                instList.append(instanceHeader)
                                print(instanceHeader)
                                check = util.readInt32(fileStream.read(4))
                                if check == 0:
                                    continue
                                else:
                                    print('An error occurred when obtaining the values.')
                                    return

                    else:
                        continue
                else:
                    print('No entries could be found in the file.')
            print(instList)

        else:
            print('File was not formatted properly; ending operations.')
            return
    else:
        print('File was not a PrOD; cancelling operations.')
        return