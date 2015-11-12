#! /usr/bin/python2.7
#-*- coding: utf-8 -*-

import sys
from pyprogress import Counter

if len(sys.argv) > 1:
    total = sys.argv[1]
else:
    total = None

c = Counter(total=total)
c.start()

while True:
    line = sys.stdin.readline()
    if len(line) > 0:
        c.inc()
    else:
        break

c.stop()
c.join()

print ""
