# blwp_to_yml.py
import blwp
import yaml
import argparse
import pathlib

def main():
    parser = argparse.ArgumentParser(description='Command to convert an imported prod encoded file to a yml file for easy editting.')
    parser.add_argument('blwpFile', type=str, help="File to open and read data from.", default=None)
    parser.add_argument('ymlFile', nargs='?', type=str, help='Name to give the outputted yml file.', default=None)

    args = parser.parse_args()
    bwlpFile = args.blwpFile

    if args.ymlFile == None:
        yml = f'{str(bwlpFile.split(".")[0])}.yml'
    else:
        yml = f"{str(args.ymlFile).split('.')[0]}.yml"

    openFile = pathlib.Path(bwlpFile)
    dataOut = blwp.prod.decoder(openFile)
    writeFile = open(pathlib.Path(yml), 'wt')
    writeFile.write(yaml.safe_dump(dataOut))
    writeFile.close()
    return
        

if  __name__ == "__main__":
    main()