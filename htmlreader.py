"""HTML Parser for AA game reports.
"""

from sgmllib import SGMLParser

class AAParser(SGMLParser):
    def reset(self):
        self.liOpen = False
        self.liCount = 0
        self.playerCount = 0
        self.playerInfo = [None, None, None]
        self.sentinels = []
        self.scourges = []
        SGMLParser.reset(self)


    def start_li(self, attr):
        self.liOpen = True

    def handle_data(self, text):
        if self.liOpen:
            self.playerInfo[self.liCount] = text.strip()
            self.liCount += 1
            if self.liCount >= 3:
                self.liCount = 0
                self.playerCount += 1
                if self.playerCount > 5:
                    self.scourges.append(self.playerInfo[:])
                else:
                    self.sentinels.append(self.playerInfo[:])

    def end_li(self):
        self.liOpen = False
            
    def result(self):
        """Return a tuple of records of players in sentinels and scourges respectively.
        """
        return (self.sentinels, self.scourges)

def showStats((sentinels, scourges)):
    print('Sentinels')
    for line in sentinels:
        print("%15s\t%s\t%s" % (line[0], line[1], line[2]))

    print('Scourges')
    for line in scourges:
        print("%15s\t%s\t%s" % (line[0], line[1], line[2]))

if __name__ == '__main__':
    f = open('data/W-2008_12_19_12_20_11.html', 'r')
    html = f.read()

    parser = AAParser()
    parser.feed(html)
    showStats(parser.result())
    
