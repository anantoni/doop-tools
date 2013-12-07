import doop, gxl, java, reflect, synthetic, sys

from decimal import *
from itertools import chain
from prettyprint import *
from stats import Statistics

def display(static, dynamic, diff):

    def maketitle():
        f = lambda x: "Appplication" if x == 'a' else "Library"
        def trans(tp):
            st, tt = tp.split('2')
            return rectprint("{0} ===> {1}".format(f(st), f(tt)))
        return trans

    caption = maketitle()

    # Print results
    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        nStatic  = len(getattr(static, tp))
        nDynamic = len(getattr(dynamic, tp))
        nMissing = len(getattr(diff, tp))

        print caption(tp)
        print "%20s: %6d" % ("Total static edges", nStatic)
        print "%20s: %6d" % ("Total dynamic edges", nDynamic)
        print "%20s: %6d" % ("Edges found", nDynamic - nMissing)

        if nDynamic > 0:
            perc = Decimal(100 * nMissing) / nDynamic
            print "%20s: %6d (%.2f%%)" % ("Edges missing", nMissing, perc)

def diff(db, trace, **kwargs):

    doopconn = doop.Connector(db)
    probe = gxl.Probe(trace)

    # Get statistics from a doop static analysis
    static = Statistics.from_doop(doopconn)

    # Get dynamic analysis statistics from a gxl trace
    dynamic = Statistics.from_trace(probe, doopconn)

    # Compute dynamic \ static
    diff = Statistics.difference(dynamic, static)

    # Construct a transformation chain
    diffchain = [(diff, 'Default')]

    def add_filter(refinement, msg):
        last = diffchain[-1][0]
        diffchain.append((refinement(last), msg))
        refinement.report()

    # Compute (dynamic \ static) \ synthetic
    if 'cp' in kwargs:
        add_filter(synthetic.Refinement(kwargs['cp']), 'No synthetic')

    # Statically unknown classes / methods
    add_filter(reflect.NoFactsRefinement(doopconn), 'No facts')

    for (diff, msg) in diffchain:
        print "--- {0} ---".format(msg)
        display(static, dynamic, diff)
    return (static, dynamic, diffchain)

if __name__ == "__main__":
    diff(sys.argv[1], sys.argv[2], cp = sys.argv[4])
