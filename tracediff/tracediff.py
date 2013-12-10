#!/usr/bin/env python

import argparse, clinit, doop, gxl, reflect, synthetic, sys, unreachable
from decimal import *
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

    # filter false positive calls to <clinit>
    add_filter(clinit.ClassInitRefinement(doopconn), '<clinit>')

    # Compute (dynamic \ static) \ synthetic
    classpath = kwargs.get('cp', None)

    if classpath:
        add_filter(synthetic.Refinement(classpath), 'No synthetic')

    # Statically unknown classes / methods
    add_filter(reflect.NoFactsRefinement(doopconn), 'No facts')

    # Prune call-edges with unreachable origin
    add_filter(unreachable.Refinement(doopconn), 'Unreachable origin')
    
    nSteps = len(diffchain)
    steps  = range(1, 1 + nSteps)

    for ((diff, msg), step) in zip(diffchain, steps):
        print "\n--- {0}. Step {1}/{2} ---\n".format(msg, step, nSteps)
        display(static, dynamic, diff)

    for e in diffchain[-1][0].a2a:
        print e

    return static, dynamic, diffchain

def main(cmd):
    if isinstance(cmd, basestring):
        cmd = cmd.split()

    # Command-line argument parsing
    parser = argparse.ArgumentParser()

    parser.add_argument('-cp', metavar = 'classpath', action='append',
        help = 'for locating java classes')
    parser.add_argument('workspace', 
        help = 'the db directory of a Doop static analysis')
    parser.add_argument('trace', 
        help = 'dynamic trace in gxl format')

    args = parser.parse_args(cmd)
    if args.cp:
        args.cp = ':'.join(args.cp)

    diff(args.workspace, args.trace, cp = args.cp)

if __name__ == "__main__":
    main(sys.argv[1:])
