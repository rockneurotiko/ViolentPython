import crypt
import sys
import os


def testPass(cryptPass, dictFilePath):
    salt = cryptPass[0:2]                   #parse the salt
    dictFile = open(dictFilePath, 'r')      #open the dictionary
    for word in dictFile.readlines():
        word = word.strip("\n")
        cryptWord = crypt.crypt(word,salt)  #crypt the word in the dictionary with the salt
        if (cryptWord == cryptPass):        #check if is the password
            print "[+] Found Password: " + word + "\n"
            return
    print "[-] Password Not Found.\n"
    return


def checkFile(filePath, programName):
    if not os.path.isfile(filePath):
        print "[-] " + filePath + " passwords file does not exists."
        exit(0)
    if not os.access(filePath, os.R_OK):
        print "[-] " + filePath + " passwords file access denied."
        exit(0)

def main():
    #check the args (if not given, passwords.txt and dictionary.txt will be used)
    if len(sys.argv) >= 2:
        passFilePath = sys.argv[1]
        if len(sys.argv) == 3:
            dictFilePath = sys.argv[2]
        else:
            dictFilePath = "dictionary.txt"
    else:
        passFilePath = "passwords.txt"
        dictFilePath = "dictionary.txt"

    #use the function checkFile that check if the file of the path is a file and can be readed
    checkFile(passFilePath, sys.argv[0])
    checkFile(dictFilePath, sys.argv[0])

    #Open the file of the passwords
    passFile = open(passFilePath)
    for line in passFile.readlines():
        if ":" in line:                                 #Parses the lines
            user = line.split(":")[0]                   #   "    "   "
            cryptPass = line.split(":")[1].strip(" ")   #   "    "   "
            print "[*] Cracking Password for : " + user
            testPass(cryptPass, dictFilePath)           #and test the hash with the dictionary

if __name__ == "__main__":
    main()

