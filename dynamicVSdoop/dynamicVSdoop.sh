#!/bin/bash

DYNCALLS=$1
DOOPCALLS=$2

if [ $# -gt 2 ] && [ $3 = '--normalize' ] ; then

# From the averroes results
while read dC ; do
	dFrom=$(echo "$dC" | awk -F '===>' '{print $1}')
	dTo=$(echo "$dC" | awk -F '===>' '{print $2}')

	dFromClass=$(echo "$dFrom" | awk -F ':' '{print $1}' | sed 's/ //g')
	dFromMeth=$(echo "$dFrom" | awk -F ':' '{print $2}')
	dFromMethS=$(echo "$dFromMeth" | sed 's/\(^.\+\)(\(.*\))/\1/' | sed 's/ //g')
	dFromMethA=$(echo "$dFromMeth" | sed 's/\(^.\+\)(\(.*\))/\2/' | sed 's/ //g' | ./bytecodePrimitives2source)

	dToClass=$(echo "$dTo" | awk -F ':' '{print $1}' | sed 's/ //g')
	dToMeth=$(echo "$dTo" | awk -F ':' '{print $2}')
	dToMethS=$(echo "$dToMeth" | sed 's/\(^.\+\)(\(.*\))/\1/' | sed 's/ //g')
	dToMethA=$(echo "$dToMeth" | sed 's/\(^.\+\)(\(.*\))/\2/' | sed 's/ //g' | ./bytecodePrimitives2source)

	echo "\"${dFromClass}.${dFromMethS}($dFromMethA)\",\"${dToClass}.${dToMethS}($dToMethA)\""
done < $DYNCALLS > ${DYNCALLS}Norm.csv

fi

while read sC ; do
	sFrom=$(echo "$sC" | awk -F '>, ' '{print $1}')
	sTo=$(echo "$sC" | awk -F '>, ' '{print $2}')

	sFromClass=$(echo "$sFrom" | awk -F ':' '{print $1}' | sed 's/ //g' | sed 's/^<//')
	sFromMeth=$(echo "$sFrom" | awk -F ':' '{print $2}')
	sFromMethS=$(echo "$sFromMeth" | sed 's/\(^.\+\)(\(.*\)).*/\1/' | awk '{print $2}' | sed 's/ //g')
	sFromMethA=$(echo "$sFromMeth" | sed 's/\(^.\+\)(\(.*\)).*/\2/' | sed 's/ //g')

	sToClass=$(echo "$sTo" | awk -F ':' '{print $1}' | sed 's/ //g' | sed 's/^<//')
	sToMeth=$(echo "$sTo" | awk -F ':' '{print $2}' | sed 's/>$//')
	sToMethS=$(echo "$sToMeth" | sed 's/\(^.\+\)(\(.*\))/\1/' | awk '{print $2}' | sed 's/ //g')
	sToMethA=$(echo "$sToMeth" | sed 's/\(^.\+\)(\(.*\))/\2/' | sed 's/ //g')

	echo "\"${sFromClass}.${sFromMethS}($sFromMethA)\",\"${sToClass}.${sToMethS}($sToMethA)\""
done < $DOOPCALLS > ${DOOPCALLS}Norm.csv


# Find invocations from dynamic-calls that don't appear in doop-infered-calls
while read dC ; do
	count=$(grep -c -F "$dC" ${DOOPCALLS}Norm.csv || true)
	if [ $count = '0' ] ; then echo "$dC" ; fi
done < ${DYNCALLS}Norm.csv > ${DYNCALLS%.*}.mustCheck.csv
