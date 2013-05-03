import nmap
import optparse
from socket import gethostbyname

def nmapScan(targetIP, targetPort):
    try:
        nmScan = nmap.PortScanner()
        nmScan.scan(targetIP, targetPort)
        state = nmScan[targetIP]['tcp'][int(targetPort)]['state']
        print " [*] %s tcp/%s + %s" % (targetIP, targetPort, state)
    except:
        print " [-] Something went wrong scanning the host %s in %s port" %(targetHost, targetPort)


def main():
    parser = optparse.OptionParser("usage%prog -H <target host> -p <target port>")
    parser.add_option("-H", dest="targetHost", type="string", help="specify target host")
    parser.add_option("-p", dest="targetPorts", type="string", help="specify target port[s] separated by comma")
    (options, args) = parser.parse_args()
    targetHost = options.targetHost
    targetPorts = str(options.targetPorts).split(",")

    if (targetHost == None) | (targetPorts == None):
        print parser.usage
        exit(0)
    try:
        targetIP = gethostbyname(targetHost)
    except:
        print "[-] Cannot resolve \"%s\": Unknown host." % targetHost
        exit(0)

    for targetPort in targetPorts:
        nmapScan(targetIP, targetPort)


if __name__ == "__main__":
    main()
