"""Socket listener for web services
You may ignore this file currently
"""

from socket import *
from count import *
import os

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 21431))
s.listen(5)

# Initialize data
os.path.walk('data/', check, None)

print('Data initialized')
logfile = open('log/access.log' % (), 'a')

gifDir = '/home/httpd/html/dota/img'

invalidChar = ('/', ':', ';', '*', '\\')
pset = set()

def invalidString(s):
    for c in invalidChar:
        if c in s:
            return True

    return False

while True:
    try:
        client, addr = s.accept()
        player = client.recv(1024)

        player = player.strip()
        logfile.write('%s: %s\n' % (addr, player))
        logfile.flush()


        if invalidString(player):
            client.close()
            continue
        
        pset.clear()
        explore(player, pset)
        genDot(counter, pset, 'dot/%s.dot' % player, player)
        os.system('dot -Tgif dot/%s.dot -o %s/%s.gif' % (player, gifDir, player))
        
        print(player)
        client.send(player)
    except error:
        print(error)
        client.close()
        break

    client.close()

print('listener closed.')
s.close()
logfile.close()
