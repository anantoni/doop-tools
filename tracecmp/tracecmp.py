import blox, queries, gxl, sys

from decimal import *
from itertools import chain
from prettyprint import *

class Analysis:
    pass

def canonical(signature):
    rec, meth = signature.split(": ")
    simplename, delim, args = meth.partition('(')
    return rec + ': ' + simplename.rpartition(' ')[2] + '(' + args

def callgraphs(db, trace):
    connector = blox.Connector(db)
    probe = gxl.Probe()

    # Get a static analysis from a doop database
    doop = Analysis()

    parse = lambda l: tuple(canonical(x) for x in l[1:-1].split(">, <"))

    app = set(canonical(m[1:-1]) for m in connector.query(queries.APP_METHODS))

    doop.a2a = map(parse, connector.query(queries.APP_TO_APP))
    doop.a2l = map(parse, connector.query(queries.APP_TO_LIB))
    doop.l2a = map(parse, connector.query(queries.LIB_TO_APP))
    doop.l2l = map(parse, connector.query(queries.LIB_TO_LIB))
    doop.nulls = map(parse, connector.query(queries.NULLS, toprint = "_n"))

    # for (s,t) in doop.a2a:
    #    print s, "===>", t

    # Get a dynamic analysis from a gxl trace
    dyn = Analysis()
    dyn.a2a = []
    dyn.a2l = []
    dyn.l2a = []
    dyn.l2l = []

    for (s,t) in probe.calledges(trace):
        f = lambda n : 'a' if n in app else 'l'
        field = '{0}2{1}'.format(f(s), f(t))
        getattr(dyn, field).append((s,t))

    # Initialization
    nDynamic = {}
    nStatic  = {}
    nFound   = {}
    missing  = {}

    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        nDynamic[tp] = len(getattr(dyn, tp))
        nStatic[tp]  = len(getattr(doop, tp))
        nFound[tp]   = 0
        missing[tp]  = []

    # Compute diff
    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        dynamic, static = getattr(dyn, tp), getattr(doop, tp)
        for (s,t) in dynamic:
            if (s,t) in static:
                nFound[tp] += 1
            else:
                missing[tp].append((s,t))

    # Print results
    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        st, tt = tp.split('2')
        full = lambda x: "Appplication" if x == 'a' else "Library"

        print rectprint("{0} ===> {1}".format(full(st), full(tt)))
        print "%20s: %6d" % ("Total static edges", nStatic[tp])
        print "%20s: %6d" % ("Total dynamic edges", nDynamic[tp])
        print "%20s: %6d" % ("Edges found", nFound[tp])
        
        nMissing = len(missing[tp])
        nTotal   = nDynamic[tp]

        if nTotal > 0:
            perc = Decimal(100 * nMissing) / nTotal
            print "%20s: %6d (%.2f%%)" % ("Edges missing", nMissing, perc)

    return missing

if __name__ == "__main__":
    callgraphs(sys.argv[1], sys.argv[2])
