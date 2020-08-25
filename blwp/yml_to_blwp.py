# yml_to_bwlp.py
import blwp
import yaml
import argparse
import pathlib
import oead

def main():
    parser = argparse.ArgumentParser(description='Command to convert a yml file to a Prod encoded file that can be used by nintendo systems.')
    parser.add_argument('ymlFile', type=str, help="Yml file to open and read data from.", default=None)
    parser.add_argument('bwlpFile', nargs='?', type=str, help='Name to give the outputted bwlp file.', default=None)
    parser.add_argument('--nocompression', '-nc', dest='compression', action='store_true', help="Don't compress the output file using yaz0.")
    args = parser.parse_args()
    ymlFile = args.ymlFile

    if args.bwlpFile == None:
        if args.compression == True:
            ext = 'blwp'
        else:
            ext = 'sblwp'
        bwlpFile = f'{str(ymlFile.split(".")[0])}.{ext}'
    else:
        bwlpFile = f"{str(args.bwlpFile).split('.')[0]}.{ext}"

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