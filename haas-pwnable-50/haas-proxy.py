#!/usr/bin/env python

import subprocess
import sys
import os
import threading
import random

def stdinreader():
    while True:
        try:
            l = sys.stdin.readline()
        except KeyboardInterrupt:
            break
        if not l:
            break
        yield l

class Proxy:
    def __init__(self, blacklist, phrases, args):
        self.blacklist = blacklist
        self.phrases = phrases
        try:
            self.chld = subprocess.Popen(args, stdin=subprocess.PIPE)
        except OSError:
            print "Error starting the haas process."
            sys.exit(1)

    def is_allowed(self, l):
        return reduce(lambda x,y: x and y, [x not in l for x in self.blacklist], True)

    def listen(self):
        for line in stdinreader():
            if self.chld.poll() is None:
                if self.is_allowed(line):
                    self.chld.communicate(line)
                else:
                    print random.choice(self.phrases)
                    break
            else:
                return
        self.chld.terminate()

    def run(self):
        t = threading.Thread(target=self.listen)
        t.daemon = True
        t.start()
        self.chld.wait()

if __name__ == '__main__':
    bl = ['shell','unix','system','cd','argv']
    phrases = ['Nice try...', 'Nope.', 'What are you trying to do?!?', "Sorry, that's not implemented!"]
    ex = os.path.join(os.path.dirname(os.path.realpath(__file__)), "haas")
    if len(sys.argv) == 2:
        ex = sys.argv[1]
    proxy = Proxy(bl, phrases, [ex])
    proxy.run()
