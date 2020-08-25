# yml_to_bwlp.py
import blwp
import yaml
import argparse
import pathlib
import oead

def main():
    parser = argparse.ArgumentParser(description='Command to convert an imported prod encoded file to a yml file for easy editting.')
    parser.add_argument('ymlFile', type=str, help="Yml file to open and read data from.", default=None)
    parser.add_argument('bwlpFile', nargs='?', type=str, help='Name tp give the outputted bwlp file.', default=None)
    parser.add_argument('--nocompression', '-nc', dest='compression', action='store_true', help="Don't compress the output file using yaz0.")
    args = parser.parse_args()
    ymlFile = args.ymlFile

    if args.bwlpFile == None:

        bwlpFile = f'{str(ymlFile.split(".")[0])}.sblwp'
    else:
        bwlpFile = str(args.bwlpFile).split('.')[0]

    openFile = open(pathlib.Path(ymlFile), 'rt')
    readFile = yaml.safe_load(openFile.read())
    dataOut = blwp.prod.encoder(readFile)
    writeFile = open(pathlib.Path(bwlpFile), 'wb')
    if args.compression == True:
        dataOut = dataOut
    else:
        dataOut = oead.yaz0.compress(dataOut)

    writeFile.write(dataOut)
    writeFile.close()
    openFile.close()
    return
        

if  __name__ == "__main__":
    main()