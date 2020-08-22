from PrOD import blwp
import pathlib
import json

dataList = blwp.decoder(pathlib.Path('tests/testOut.blwp'))
(open(pathlib.Path('tests/testOutB.json'), 'wt')).write(json.dumps(dataList, indent=2))

#print(dataList)
dataOut = blwp.encoder(dataList)
#print(dataOut)

#(open(pathlib.Path('tests/testOut.blwp'), 'wb')).write(dataOut)