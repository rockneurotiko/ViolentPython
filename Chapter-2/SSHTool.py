import pexpect
import pxssh
from pxssh import ExceptionPxssh
import optparse
import sys
from getpass import getpass

def correct_empty_argvs(parser):
    allowed_switches=[] #lista que va a tener las opciones permitidas
    for opt in parser.option_list:
        allowed_switches.extend(opt._short_opts) #cogemos las opciones y las ponemos en la lista

    for a in range(len(sys.argv)): #recorremos los argumentos
        argv = sys.argv[a]
        if argv in allowed_switches: #Si el argumento es una opcion permitida
            #Si es el ultimo argumento, o el siguiente tambien esta en los argumentos...
            if (a == len(sys.argv) -1) or (sys.argv[a+1] in allowed_switches):
                sys.argv.insert(a + 1, "")


def send_command(sshConn, cmd):
    sshConn.sendline(cmd)
    sshConn.prompt()
    print sshConn.before

def connect(host, user, password):
    try:
        sshConn = pxssh.pxssh()
        sshConn.login(host, user, password)
        return sshConn
    except ExceptionPxssh, e:
        print e
        exit(1)
    except:
        print "[-] Error Connecting"
        print "[-] Check your host:%s user:%s or passwd:(I'm not going to show it man...) "%(host, user)
        exit(1)

def main():
    help_text ="""
        %prog [-u <user>] [-h <host>] [-p [Password]]

Description:
        Basic ssh connection script in Python.
        If the connection is stablished, you can send commands and recive answer.
        [[WARNING!]] You can't do any sudo or su command, you can't change of user once you are connected.
        Author = "Rock Neurotiko"
        License = WTFPL (do What The Fuck you want to Public License: http://www.wtfpl.net/ )
        BUT! If you write the acknowledgment(fucking difficult word to non-english u.U) you are so awesome man! =D"""
    parser = optparse.OptionParser(usage=help_text, conflict_handler="resolve", version="%prog version 0.WTF?")
    parser.add_option("-u", dest="user", type="string", help="Specify the user (if not, root will be use)", metavar="<user>")
    parser.add_option("-h", dest="host", type="string", help="Specify the host (if not, localhost will be use", metavar="<host>")
    parser.add_option("-p", dest="password", type="string", help="""Specify the password (if not, toor will be use)\n
            [If just -p is writed, the program will ask you to write the password (securely)]""", metavar = "[password]")

    correct_empty_argvs(parser)
    (options, args) = parser.parse_args()
    host = options.host
    user = options.user
    password = options.password

    if host == "" or host == None:
        host = "localhost"
    if user == "" or user == None:
        user = "root"
    if password == "":
        password = getpass("Password: ")
    elif password == None:
        password = "toor"

    #CARE WITH THE NEXT PRINT, USE IT JUST FOR DEBUG (PASSWORD SHOWED!!!)
    #print "We will connect to %s@%s // %s" % (user, host, password)

    sshConn = connect(host, user, password)
    command=raw_input("[%s@%s]>$ " %(user, host))
    while(command != "exit"):
        send_command(sshConn,command)
        command=raw_input("[%s@%s]>$ "%(user, host))

    sshConn.logout()


if __name__ == "__main__":
    main()
