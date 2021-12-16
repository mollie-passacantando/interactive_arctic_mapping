## This file is called fabile.py because the fabric
## package will look for it to run commands to the server

import fabric

def remote_connection():
    c = fabric.Connection(host = "192.168.1.198",user = "mollie")
    print('this was good')
    return c.get('testfile.txt')