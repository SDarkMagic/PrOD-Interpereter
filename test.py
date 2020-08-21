from PrOD import blwp
import pathlib

dataList = blwp.decoder(pathlib.Path('tests/test.sblwp'))

#print(dataList)
dataOut = blwp.encoder(dataList)

#(open(pathlib.Path('tests/test.sblwp'), 'wb')).write(dataOut.read())