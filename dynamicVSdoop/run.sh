#!/bin/bash

set -e      # Exit immediately if a command exits with a nonzero exit status
set -u      # Treat unset variables as an error
#set -x     # Print commands and their arguments as they are executed (debugging)

RESULTS_DIR=${1:-tmp}
ANALYSES_DIR=${2:-.}

for f in averroes-dynamic-call-graphs/*.gxl ; do
	b=${f##*/} ; b=${b%.*}
	if ! [ -x $ANALYSES_DIR/$b ] ; then continue ; fi

	### COLLECT AVERROES CALL-GRAPH
	java -jar averroes-dynamic-call-graphs/cginfo.jar -a2a $f > $RESULTS_DIR/${b}.a2a.dyn
	java -jar averroes-dynamic-call-graphs/cginfo.jar -a2l $f > $RESULTS_DIR/${b}.a2l.dyn
	java -jar averroes-dynamic-call-graphs/cginfo.jar -l2a $f > $RESULTS_DIR/${b}.l2a.dyn


	### COLLECT DOOP CALL-GRAPH
	./collectDoopCallGraph.sh $ANALYSES_DIR/$b $b $RESULTS_DIR


	### NORMALIZE FILES
	./dynamicVSdoop.sh $RESULTS_DIR/${b}.a2a.dyn $RESULTS_DIR/${b}.a2a.doop --normalize
	./dynamicVSdoop.sh $RESULTS_DIR/${b}.a2l.dyn $RESULTS_DIR/${b}.a2l.doop --normalize
	./dynamicVSdoop.sh $RESULTS_DIR/${b}.l2a.dyn $RESULTS_DIR/${b}.l2a.doop --normalize

	echo "a2a" > $RESULTS_DIR/${b}.mustCheck
	cat $RESULTS_DIR/${b}.a2a.mustCheck.csv >> $RESULTS_DIR/${b}.mustCheck
	echo "a2l" >> $RESULTS_DIR/${b}.mustCheck
	cat $RESULTS_DIR/${b}.a2l.mustCheck.csv >> $RESULTS_DIR/${b}.mustCheck
	echo "l2a" >> $RESULTS_DIR/${b}.mustCheck
	cat $RESULTS_DIR/${b}.l2a.mustCheck.csv >> $RESULTS_DIR/${b}.mustCheck


	### FIND MISSING EDGES IN DOOP
	cat $RESULTS_DIR/${b}.a2a.mustCheck.csv | grep -v Main2 > mustCheck.csv
	cp $RESULTS_DIR/${b}.a2a.doopNorm.csv sNorm.csv

	cat $RESULTS_DIR/${b}.AssignCompatible.csv |
	sed 's/^  // ; s/\/[0-9]\+// ; s/, /,/' > AssignCompatible.csv

	cat $RESULTS_DIR/${b}.nulls.doop |
	sed 's/^  // ; s/\/[0-9]\+//' |
	sed 's/^\([^:]\+\): [^ ]\+ /\1./ ; s/^<// ; s/>\//\// ; s/([^)]*)//' |
	sed 's/\.\([^.]\+\)$/","\1"/ ; s/^/"/ ; s/\//","/' > nulls.csv

	bloxbatch -script findMissing.lb && rm -r FindMissing

	mv MissingTarget.csv $RESULTS_DIR/${b}.MissingTarget.csv
	mv MissingSource.csv $RESULTS_DIR/${b}.MissingSource.csv

	cat NullsTrans.csv | sed 's/","\([^,]\+\)$/.\1/' > $RESULTS_DIR/${b}.NullsTrans.csv

	cat $RESULTS_DIR/${b}.MissingTarget.csv | sed 's/([^)]*)//g' | (
		while read line ; do
			count=$(grep -c -F "$line" $RESULTS_DIR/${b}.NullsTrans.csv || true)
			if [ $count -ne '0' ] ; then echo "$line" ; fi
		done > MissingNulls.csv
	)
	cat $RESULTS_DIR/${b}.MissingTarget.csv | sed 's/([^)]*)//g' | (
		while read line ; do
			count=$(grep -c -F "$line" $RESULTS_DIR/${b}.NullsTrans.csv || true)
			if [ $count = '0' ] ; then echo "$line" ; fi
		done > MissingNotNulls.csv
	)
	mv MissingNulls.csv $RESULTS_DIR/${b}.MissingNulls.csv
	mv MissingNotNulls.csv $RESULTS_DIR/${b}.MissingNotNulls.csv

	rm AssignCompatible.csv nulls.csv sNorm.csv mustCheck.csv NullsTrans.csv

done	
