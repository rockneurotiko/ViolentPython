import optparse

from socket import *
from threading import Thread, Semaphore


screenLock = Semaphore(value=1)

def conectionScan(targetHost, targetPort):
    try:
        connSocket = socket(AF_INET, SOCK_STREAM)
        connSocket.connect((targetHost, targetPort))
        connSocket.send("ViolentPython\r\n")
        results = connSocket.recv(100)
        screenLock.acquire()
        print "[+]%s:%d/tcp open" % (targetHost,targetPort)
        print "[+]%s" % str(results)
    except:
        screenLock.acquire()
        print "[-]%s:%d/tcp closed" % (targetHost,targetPort)
    finally:
        screenLock.release()
        connSocket.close()


def portScan(targetHost, targetPorts):
    try:
        targetIP = gethostbyname(targetHost)
    except:
        print "[-] Cannot resolve \"%s\": Unknown host" % targetHost
        return
    try:
        targetName = gethostbyaddr(targetIP)
        print "\n[+] Scan Results for: " + targetName[0]
    except:
        print "\n[+] Scan Results for: " + targetIP

    setdefaulttimeout(1)
    for targetPort in targetPorts:
        #print "Scanning port " + targetPort
        t = Thread(target = conectionScan, args=(targetHost, int(targetPort)))
        t.start()


def main():
    parser = optparse.OptionParser("usage %prog -H " + "<target host> -p <target port>")
    parser.add_option("-H", dest="targetHost", type="string", help="Specify target host")
    parser.add_option("-p", dest="targetPorts", type="string", help="Specify target port[s] separated by comma")

    (options, args) = parser.parse_args()

    targetHost = options.targetHost
    targetPorts = str(options.targetPorts).split(',')

    if (targetHost == None) | (targetPorts == None):
        print parser.usage
        exit(0)
    portScan(targetHost, targetPorts)


if __name__ == "__main__":
    main()
