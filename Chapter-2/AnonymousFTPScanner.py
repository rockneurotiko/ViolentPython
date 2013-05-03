import ftplib
import optparse
import re
from threading import *

maxConnections = 20 # The number of max connections at time
connection_lock = BoundedSemaphore(value=maxConnections) #The Semaphore to control the max connections

def anonLogin(* hostname):
    """
    anonLogin tries to do the anonymous connection against the hostname or IP given as argument

    Have to remake the IP because sometimes the argument is a tuple instead of
    a string [A tuple like ("1","9","2",".","0",".","0",".","1")]
    """
    IP = ""
    for i in hostname:
        IP = IP + i
    hostname = IP

    try:
        ftp = ftplib.FTP(hostname)
        ftp.login("anonymous", "me@your.com")
        print "\n[+]" + str(hostname) + " FTP Anonymous Logon Succeded"
        ftp.quit()
        return True
    except Exception, e:
        print "\n[-] %s FTP Logon Failed." % str(hostname)
        return False

    finally:
        connection_lock.release()


def ipRange(start_ip, end_ip):
    """
    ipRange is a function that takes a start IP and an end IP and
    return a list with all the range of the IPs
    >>> ipRange(192.168.1.1, 192.168.1.3)
    ["192.168.1.1","192.168.1.2","192.168.1.3"]
    """
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    return ip_range


"""
[TODO]
If difference between a range of IPs or a hostname, so if a hostname is given
try to do the Anon FTP Login against that hostname
"""
def main():
    #Take the flags options.
    parser = optparse.OptionParser("usage %prog -s <IP from> -e <IP end>")
    parser.add_option("-s", dest="startIP", type="string", help="Specify the first IP")
    parser.add_option("-e", dest="endIP", type="string", help="Specify the last IP")

    (options, args) = parser.parse_args()
    startIP = options.startIP
    endIP = options.endIP

    #Control that both arguments have been passed
    if startIP == None or endIP == None:
        print parser.usage
        exit(1)

    #Check IPs with a regular expression.
    IPpattern = re.compile(r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
    isStartIP = IPpattern.search(startIP)
    isEndIP   = IPpattern.search(endIP)
    if isStartIP == None or isEndIP == None:
        print parser.usage
        exit(1)

    #Split the IP's
    startIPRanges = startIP.split(".")
    endIPRanges = endIP.split(".")

    #Check if second one is grather or equal than the first one. That works beause of the lazy operators
    if endIPRanges[0] < startIPRanges[0] or endIPRanges[1] < startIPRanges[1] or endIPRanges[2] < startIPRanges[2] or endIPRanges[3] < startIPRanges[3]:
        print "[-] Error, the last IP must be greater"
        exit(1)

    IP_Range = ipRange(startIP, endIP)

    for i in IP_Range:
        connection_lock.acquire() #This semaphore is just to don't do more than 20 threads at time and don't overload the CPU
        print "[-] Testing %s" % i
        t = Thread(target=anonLogin, args=i)
        child = t.start()


if __name__ == "__main__":
    main()
