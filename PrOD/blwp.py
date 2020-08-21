# bwlp.py

import oead
import io
import pathlib
from PrOD import util

def decoder(fileIn):
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
#    print(f'magic: {magic} unknown0: {unknown0} unknown1: {unknown1} unknown2: {unknown2} padding: {padding}')
    
    if magic == b'PrOD':
        if (
            unknown0 == b'\x01\00\00\00'
            and
            unknown1 == b'\x00\00\00\01'
            and
            padding == b'\x00\00\00\00'
        ):
#            print(len(entryCount))
            instanceHeader = {} # Creates a dictionary called instanceHeader with the keys being the instanceNames
            instanceLists = {}
            for entry in entryCount:
                if iterCount < len(entryCount):
                    iterCount += 1
                    size = fileStream.read(4)
                    instanceCount = list(range(util.readInt32(fileStream.read(4))))
                    stringOffset = util.readInt32(fileStream.read(4))
                    testVar = util.readInt32(fileStream.read(4))
                    
                    if testVar == 0:
                        currentStreamPos = fileStream.tell() # Gets the current reader position and stores it to a variable
                        fileStream.seek(int(stringTableOffset + stringOffset)) # Finds individual instance name in the string table
                        instanceName = str(fileStream.read().decode('ANSI')).partition('\x00')[0] # Sets the instance name variable
                        fileStream.seek(currentStreamPos) # Returns the reader position to twhere it was before reading the instance name
                        subIterCount = int(0) # Resets the subIterCount variable

                        
                        for instance in instanceCount:
                            if subIterCount < len(instanceCount):
                                subIterCount += 1
                                indx = list(sorted(instanceLists.keys()))
                                newKey = util.newKeyIndx(indx)

                                # Reads and updates the instance dictionary with t/r/s values
                                translate = [util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4))]
                                rotation = [util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4)), util.readFloat(fileStream.read(4))]
                                scale = util.readFloat(fileStream.read(4))
                                instanceLists.update({newKey: {'translate': translate, 'rotation': rotation, 'scale': scale}})


                                # Reads for padding bytes
                                check = util.readInt32(fileStream.read(4))
                                
                                # Confirms that bytes obtained from 'check' are actually padding bytes
                                if check == 0:
                                    continue
                                else:
                                    print('An error occurred when obtaining the values.')
                                    return
                                    
                        instanceHeader.update({instanceName: instanceLists})
                        instanceLists = {}
                        

                    else:
                        continue
                else:
                    print('No entries could be found in the file.')

        else:
            print('File was not formatted properly; ending operations.')
            return
    else:
        print('File was not a PrOD file; cancelling operations.')
        return
    return(instanceHeader)

def encoder(rawDataIn):
    fileStream = io.BytesIO()
    magic = 'PrOD'
    compileKeys = []
    uniqueKeys = list(rawDataIn.keys())
    if isinstance(rawDataIn, dict):
        objectInstances = len(list(rawDataIn.keys()))
        print('dict in')
        fileStream.write(magic.encode('ANSI'))
        fileStream.write(util.writeInt32(0x01000000))
        fileStream.write(util.writeInt32(0x00000001))

        fileStream.write(util.writeInt32(0x00000000)) # Placeholder for offset to string table data
        fileStream.write(util.writeInt32(0x00000000)) # Placeholder for file size
        fileStream.write(util.writeInt32(objectInstances)) # Number of instances
        fileStream.write(util.writeInt32(0x00000000)) # Placeholder for string table offset
        fileStream.write(util.writeInt32(0x00000000)) # Padding; always 0

        stringTable = io.BytesIO()
        for key in list(rawDataIn.keys()):
            key = list(dictionary.keys())[0]
            compileKeys.append(key)
            if key in uniqueKeys:
                continue
            else:
                uniqueKeys.append(key)
        for key in uniqueKeys:
            instCount = int(compileKeys.count(key))
            fileStream.write(util.writeInt32(instCount * 32)) # Size of each instance in bytes
            fileStream.write(util.writeInt32(instCount)) # Number of instances
            fileStream.write(util.writeInt32(int(stringTable.tell()) + 8))

            stringTable.write(bytes(key.encode('ANSI'))) # Add Name to string table
            fileStream.write(util.writeInt32(0x00000000)) # Null terminator for string

            alignment = ((((len(key) + 1) + 3) &~ (3)) - (len(key) + 1))
            stringPadding = util.writeInt32(alignment)
            stringTable.write(stringPadding)

            fileStream.write(util.writeInt32(0))

            for dictionary in rawDataIn:
                print(dictionary)
                try:
                    currDict = dictionary.get(key)
                except:
                    continue
                if currDict != None:
#                    print(currDict)
                    translate = currDict.get('translate')
                    rotation = currDict.get('rotation')
                    scale = currDict.get('scale')

                    # Writes the Translation values
                    fileStream.write(util.writeFloat(translate[0]))
                    fileStream.write(util.writeFloat(translate[1]))
                    fileStream.write(util.writeFloat(translate[2]))

                    # Writes the rotation values
                    fileStream.write(util.writeFloat(rotation[0]))
                    fileStream.write(util.writeFloat(rotation[1]))
                    fileStream.write(util.writeFloat(rotation[2]))

                    # Writes the uniform scale value
                    fileStream.write(util.writeFloat(scale))

                    # More padding, always 0
                    fileStream.write(util.writeInt32(0))

                    currDictIndx = rawDataIn.index(dictionary)
                    rawDataIn.pop(currDictIndx)
                    currDict = None
                else:
                    continue
#            print(rawDataIn)
#        fileStream.seek(0x0c)
#        fileStream.write()
            
#        print(compileKeys)
        fileStream.seek(0)
#        (open(pathlib.Path('tests/testOut.blwp'), 'wb')).write(fileStream.read())
#        print(fileStream.read())



    else:
        print('Inputted data was not formatted properly.')
        return
    return(fileStream)