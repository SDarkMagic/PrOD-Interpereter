from PrOD import blwp
import pathlib
import json
import oead

dataList = blwp.decoder(pathlib.Path('tests/E-5_TeraTree.bak.sblwp'))
(open(pathlib.Path('tests/E-5.json'), 'wt')).write(json.dumps(dataList, indent=2))

#print(dataList)
dataOut = blwp.encoder(json.loads(open('tests/E-5.json', 'rt').read()))
#print(dataOut)

if dataOut != None:
    (open(pathlib.Path('tests/E-5_TeraTree.sblwp'), 'wb')).write(oead.yaz0.compress(dataOut))
else:
    print('Nothing to write.')