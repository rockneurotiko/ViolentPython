import crypt
import sys
import os
def testPass(cryptPass, dictFilePath):
    salt = cryptPass[0:2]
    dictFile = open(dictFilePath, 'r')
    for word in dictFile.readlines():
        word = word.strip("\n")
        cryptWord = crypt.crypt(word,salt)
        if (cryptWord == cryptPass):
            print "[+] Found Password: " + word + "\n"
            return
    print "[-] Password Not Found.\n"
    return
def help(programName):
    print "[-] Usage: " + programName + " [path to passwords file] + [path to dictionary file]"
    print "[-] If not path is given for password file, the program will use \"passwords.txt\" file."
    print "[-] If not path is given for dictionary file, the program will use \"dictionary.txt\" file."
def main():
    if len(sys.argv) >= 2:
        passFilePath = sys.argv[1]
        if len(sys.argv) == 3:
            dictFilePath = sys.argv[2]
        else:
            dictFilePath = "dictionary.txt"
    else:
        passFilePath = "passwords.txt"
        dictFilePath = "dictionary.txt"

    if not os.path.isfile(passFilePath):
        print "[-] " + passFilePath + " passwords file does not exists."
        help(sys.argv[0])
        exit(0)
    if not os.access(passFilePath, os.R_OK):
        print "[-] " + passFilePath + " passwords file access denied."
        help(sys.argv[0])
        exit(0)
    if not os.path.isfile(dictFilePath):
        print "[-] " + dictFilePath + " dictionary file does not exists."
        help(sys.argv[0])
        exit(0)
    if not os.access(dictFilePath, os.R_OK):
        print "[-] " + dictFilePath + " dictionary file access denied."
        help(sys.argv[0])
        exit(0)

    passFile = open(passFilePath)
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptPass = line.split(":")[1].strip(" ")
            print "[*] Cracking Password for : " + user
            testPass(cryptPass, dictFilePath)

if __name__ == "__main__":
    main()

