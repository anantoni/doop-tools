#!/bin/bash

if [ $# -ne 3 ] ; then
	echo 'Usage: <DB> <BENCHMARK> <RESULTS_DIR>'
	exit 1
fi

DB=$1
BENCHMARK=$2
RESULTS_DIR=$3

function doDB() {
bloxbatch -db $DB -query '_(from, to) <- Stats:Simple:InsensCallGraphEdge(callsite, to), Instruction:Method[callsite] = from, Stats:Simple:ApplicationMethod(from), Stats:Simple:ApplicationMethod(to).' > $RESULTS_DIR/$BENCHMARK.a2a.doop
bloxbatch -db $DB -query '_(from) <- Stats:Simple:InsensCallGraphEdge(callsite, to), Instruction:Method[callsite] = from, Stats:Simple:ApplicationMethod(from), !Stats:Simple:ApplicationMethod(to).' > $RESULTS_DIR/$BENCHMARK.a2l.doop
bloxbatch -db $DB -query '_(to) <- Stats:Simple:InsensCallGraphEdge(callsite, to), Instruction:Method[callsite] = from, !Stats:Simple:ApplicationMethod(from), Stats:Simple:ApplicationMethod(to).' > $RESULTS_DIR/$BENCHMARK.l2a.doop
bloxbatch -db $DB -query AssignCompatible > $RESULTS_DIR/$BENCHMARK.AssignCompatible.csv
bloxbatch -db $DB -query '_r(inv) <- Stats:Simple:ReachableVirtualMethodInvocation(inv). _r(inv) <- Reachable(meth), SpecialMethodInvocation:In(inv, meth). _n(inv) <- Stats:Simple:NullVirtualMethodInvocation(inv). _n(inv) <- _r(inv), SpecialMethodInvocation:Base[inv] = base, !(Stats:Simple:InsensVarPointsTo(_, base)).' -print _n > $RESULTS_DIR/$BENCHMARK.nulls.doop
}

doDB
