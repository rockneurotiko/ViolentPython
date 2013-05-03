import pexpect

PROMPT = ["#", ">>>", ">", "\$"]

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before

def connect(user, host, password):
    ssh_newkey = "Are you sure you want to continue connecting"
    connString = "ssh %s@%s" % (user, host)
    child =pexpect.spawn(connString)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, "[P|p]assword:"])
    if ret == 0:
        print "[-] Error connecting"
        return
    if ret == 1:
        child.sendline("yes")

    ret = child.expect([pexpect.TIMEOUT, "[P|p]assword:"])
    if ret == 0:
        print "[-] Error connecting"
        return
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host = "localhost"
    user = "root"
    password = "toor"
    child = connect(user, host, password)
    if child:
        #send_command(child, "cat /etc/shadow | grep root")
        send_command(child, "cd ~ ; pwd")


if __name__ == "__main__":
    main()




