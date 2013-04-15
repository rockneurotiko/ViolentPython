import zipfile
import sys
import os
import optparse

from threading import Thread

def extractFile(zipFile, password):
    try:
        zipFile.extractall(pwd=password)
        print "[+] Password = " + password + "\n"
    except:
        pass
def checkFile(filePath, programName):
    if not os.path.isfile(filePath):
        print "[-] " + filePath + " passwords file does not exists."
        exit(0)
    if not os.access(filePath, os.R_OK):
        print "[-] " + filePath + " passwords file access denied."
        exit(0)

def help(programName):
    print "[-] Usage: " + programName + " -f <ZipFile> + -d [path to dictionary file]"
    print "[-] If not path is given for dictionary file, the program will use \"dictionary.txt\" file."
def main():
    parser = optparse.OptionParser("[-] Usage: " + sys.argv[0] + "-f <zipfile> -d [dictionary]")
    parser.add_option("-f", dest="zipFilePath", type="string", help="specify zip file")
    parser.add_option("-d", dest="dictFilePath", type="string", help="specify dictionary file (not necesary)")
    (options, args) = parser.parse_args()
    if options.zipFilePath == None:
        print parser.usage
        exit(0)
    if options.dictFilePath == None:
        options.dictFilePath = "dictionary.txt"
    (zipFilePath, dictFilePath) = options.zipFilePath, options.dictFilePath

    checkFile(zipFilePath, sys.argv[0])
    checkFile(dictFilePath, sys.argv[0])

    zipFile = zipfile.ZipFile(zipFilePath)
    dictFile = open(dictFilePath)
    for line in dictFile.readlines():
        password = line.strip("\n")
        t = Thread(target=extractFile, args=(zipFile,password))
        t.start()
    #print "[-] Sorry, the password couldn't be founded with that dictionary"

if __name__ == "__main__":
    main()

