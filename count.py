"""A package to help calculate stats and generate dot files
"""

import os, sys
import operator
from htmlreader import *
from string import lower

parser = AAParser()
counter = {}
playertime = {}
lower2normal = {} # ID case record

hiddenlist = ()  # IDs in this list will be ignored in search
              
playerset = set()

outputDot = 'dot/result.dot'
outputGif = 'dot/result.gif'

ownColor = 'red'
colorLevel = [50, 40, 30, 20, 10, 0]
colorLevelVal = ['orangered', 'orange', 'lightpink', 'khaki', 'papayawhip', 'white']
minTime = 6   # Minimal games required to regard as 'being together'
minPlayer = 8 # Deprecated parameter
maxDepth = 1  # Maximum depth(s) to explore a friend list of the player

def addStats(team):
    for m in team:
        lm = lower(m[0])
        if not counter.has_key(lm):
            lower2normal[lm] = m[0]
            counter[lm] = {}
            playertime[lm] = 1
        else:
            playertime[lm] += 1

        plist = counter[lm]
        for n in team:
            ln = lower(n[0])
            if not lm == ln:
                if not plist.has_key(ln):
                    plist[ln] = 1
                else:
                    plist[ln] += 1

def showCounter(counter):
    for player, plist in counter.iteritems():
        print(player)
        for partner, count in plist.iteritems():
            print('%s : %d' % (partner, count))

        print
    
def check(arg, dirname, names):
    """Read files under dirname and import all the reports
    """
    for fname in names:
        if not lower(fname).endswith('html'):
            continue
        path = dirname + fname

        fin = open(dirname + fname, 'r')
        parser.reset()
        parser.feed(fin.read())
        sentinels, scourges = parser.result()
        addStats(sentinels)
        addStats(scourges)

def getColor(times):
    for x, c in zip(colorLevel, colorLevelVal):
        if times >= x:
            return c
    print('getColor: couldn\'t find color for time=', times)
    return 'white'

def genDot(counter, pset, filename, pid=None):
    """Generate dot file with information about players in pset
    """
    f = open(filename, 'w')
    f.write('graph G {\n');

    printset = set()
    for p1 in pset:
        plist = counter[p1]
        
        for p2, times in plist.iteritems():
            if p1 > p2 and p2 in pset and times >= minTime:
                f.write('%u -- %u [label="%d"];\n' % (hash(p1), hash(p2), times))
                printset.add(p1)
                printset.add(p2)

    if pid:
        pid = lower(pid)
        if not counter.has_key(pid):
            f.write('}\n')
            f.close()
            return
        plist = counter[pid]
        for player in printset:
            if plist.has_key(player):
                times = plist[player]
            else:
                times = 0
            if pid == player:
                f.write('%u [label="%s", style=filled, peripheries=2, color="%s"];\n' % (hash(player), lower2normal[player], ownColor))
            else:
                f.write('%u [label="%s", style=filled, color=black, fillcolor="%s"];\n' % (hash(player), lower2normal[player], getColor(times)))
        
    f.write('}\n')
    f.close()
                
def makeList(player, depth, pset):
    """Recursively find player's friends
    """
    if depth > maxDepth:
        return

    for p, t in counter[player].iteritems():
        if t < minTime:
            continue
        pset.add(p)
        makeList(p, depth + 1, pset)
        

def explore(player, pset):
    """Create a player list starting from player with maximum depth equal to maxDepth
    """
    player = lower(player)
    if not playertime.has_key(player):
        return
    pset.add(player)
    makeList(player, 1, pset)

if __name__ == '__main__':
    os.path.walk('data/', check, None)

    for x,t in sorted(playertime.items(), key=lambda(k,v):(v,k)):
        playerset.add(x)
        explore(x, playerset)

    playerset.clear()

#    playerset.difference_update(set(hiddenlist))

    explore('YamateH', playerset)

    genDot(counter, playerset, outputDot, 'YamateH')

