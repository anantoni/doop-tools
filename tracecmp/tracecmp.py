import doop, gxl, sys

from decimal import *
from itertools import chain
from prettyprint import *

class Statistics:
    pass

def diff(db, trace):

    def fieldmapping(app):
        f = lambda n : 'a' if n in app else 'l'
        return lambda (s,t): '{0}2{1}'.format(f(s), f(t))

    def maketitle():
        f = lambda x: "Appplication" if x == 'a' else "Library"
        def trans(tp):
            st, tt = tp.split('2')
            return rectprint("{0} ===> {1}".format(f(st), f(tt)))
        return trans

    doopconn = doop.Connector(db)
    probe = gxl.Probe()

    # Get statistics from a doop static analysis
    doopstats = Statistics()
    edgeset = fieldmapping(doopconn.methods(app_only = True))

    doopstats.a2a = doopconn.calledges(_from = 'app', _to = 'app')
    doopstats.a2l = doopconn.calledges(_from = 'app', _to = 'lib')
    doopstats.l2a = doopconn.calledges(_from = 'lib', _to = 'app')
    doopstats.l2l = doopconn.calledges(_from = 'lib', _to = 'lib')
    doopstats.nulls = doopconn.nulls()

    # for (s,t) in doopstats.a2a:
    #    print s, "===>", t

    # Get dynamic analysis statistics from a gxl trace
    dynstats = Statistics()

    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        setattr(dynstats, tp, [])

    for e in probe.calledges(trace):
        getattr(dynstats, edgeset(e)).append(e)

    # Compute dynamic \ static
    diff = Statistics()

    # isgen = reflect.generated(doopconn)

    # Compute diff
    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        dynamic, static = getattr(dynstats, tp), getattr(doopstats, tp)
        setattr(diff, tp, [e for e in dynamic if e not in static])

    caption = maketitle()

    # Print results
    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        nStatic  = len(getattr(doopstats, tp))
        nDynamic = len(getattr(dynstats, tp))
        nMissing = len(getattr(diff, tp))

        print caption(tp)
        print "%20s: %6d" % ("Total static edges", nStatic)
        print "%20s: %6d" % ("Total dynamic edges", nDynamic)
        print "%20s: %6d" % ("Edges found", nDynamic - nMissing)

        if nDynamic > 0:
            perc = Decimal(100 * nMissing) / nDynamic
            print "%20s: %6d (%.2f%%)" % ("Edges missing", nMissing, perc)

    return diff

if __name__ == "__main__":
    diff(sys.argv[1], sys.argv[2])
