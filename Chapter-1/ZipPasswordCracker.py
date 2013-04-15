import zipfile
import sys
import os
import optparse

from threading import Thread

def extractFile(zipFile, password):
    """ function that tries to extract the zip with the password given
    and if it's possible print the password"""
    try:
        zipFile.extractall(pwd=password)
        print "[+] Password = " + password + "\n"
    except:
        pass

def checkFile(filePath, programName):
    """ function implemented to check if the file in the path is a file and you have read acces"""
    if not os.path.isfile(filePath):
        print "[-] " + filePath + " passwords file does not exists."
        exit(0)
    if not os.access(filePath, os.R_OK):
        print "[-] " + filePath + " passwords file access denied."
        exit(0)


def main():

    #parser is used to parse the options given as argvs
    parser = optparse.OptionParser("[-] Usage: " + sys.argv[0] + "-f <zipfile> -d [dictionary]")
    parser.add_option("-f", dest="zipFilePath", type="string", help="specify zip file")
    parser.add_option("-d", dest="dictFilePath", type="string", help="specify dictionary file (not necesary)")
    (options, args) = parser.parse_args()   #right here get the args defined in the options
    if options.zipFilePath == None:         #the zip file must be passed
        print parser.usage
        exit(0)
    if options.dictFilePath == None:        #but if not diccionary is given, will try to use "dictionary.txt"
        options.dictFilePath = "dictionary.txt"
    (zipFilePath, dictFilePath) = options.zipFilePath, options.dictFilePath


    #check the files with the function implemented
    checkFile(zipFilePath, sys.argv[0])
    checkFile(dictFilePath, sys.argv[0])

    zipFile = zipfile.ZipFile(zipFilePath) #read the zip file
    dictFile = open(dictFilePath)           #read the dictionary
    for line in dictFile.readlines():       #for every word in the dictionary
        password = line.strip("\n")
        t = Thread(target=extractFile, args=(zipFile,password)) #creates a thread that call the function extractFile
        t.start()

if __name__ == "__main__":
    main()

