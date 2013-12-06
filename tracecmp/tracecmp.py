import doop, gxl, sys

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

def diff(db, trace):

    def runtime_created(conn):
        methods = conn.methods()
        classes = conn.classes()
        formeth  = lambda x: x not in methods
        forclass = lambda x: x not in classes
        return forclass, formeth

    doopconn = doop.Connector(db)
    probe = gxl.Probe(trace)

    # Get statistics from a doop static analysis
    static = Statistics.from_doop(doopconn)

    # Get dynamic analysis statistics from a gxl trace
    dynamic = Statistics.from_trace(probe, doopconn)

    # Compute dynamic \ static
    diff = Statistics.difference(dynamic, static)

    # Runtime-created classes / methods
    unknown_class, unknown_method = runtime_created(doopconn)
    rt_generated = set()

    # Compute diff
    for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
        missing = getattr(diff, tp)

        for (s,t) in missing:
            for meth in (s,t):
                receiver = meth.split(':')[0]
                if receiver in rt_generated:
                    continue
                if unknown_class(receiver):
                    rt_generated.add(receiver)
                    print "Runtime-created <class>:  ", receiver
                elif unknown_method(meth):
                    print "Runtime-created <method>:     ", meth

    display(static, dynamic, diff)
    return (static, dynamic, diff)

if __name__ == "__main__":
    diff(sys.argv[1], sys.argv[2])
