#!/usr/bin/env python

import argparse, doop, sys, re
from decimal import *

def cleanFld(fld):
	_, fld = fld.split(": ")
	_, fld = fld.split(" ")
	return fld[:-1]



def filterHTML(value):
	return value.replace("<", "&lt;").replace(">", "&gt;")

def genPart(id, title):
	return "<div id=\"{0}\"><h2>{1}</h2>".format(id, title)
def genPartEnd():
	return "</div>"

def genVar(var, idSuffix=""):
	return "<a href=\"#{0}{1}\">{0}</a>".format(var, idSuffix)

def genHeap(heap):
	if re.match('^<<.*>>$', heap):
		heap = heap.replace("<<", "").replace(">>", "")
		return "<b>{0}</b>".format(heap)
	else:
		return heap

def genVarPointsHead(var, heap):
	extra = " style=\"color: red;\"" if heap == "@" else ""
	return "<hr /><h3{1}><a id=\"{0}\">{0}</a></h3>".format(var, extra)

def genElem(element):
	return "<div>{0}</div>".format(element)

def genHTML(db, method):
	doopconn = doop.Connector(db)

	cl, sig = method[1:-1].split(": ")
	sig, _ = sig.split("(")

	res = " ".join( doopconn.modifiers(method) )
	sig = res + " " + filterHTML(sig) + "("

	res = doopconn.formals(method)
	res.sort()

	formals = []
	for elem in res:
		parts = elem.split(", ")
		_, var = parts[2].split("/")
		formals.append( parts[1] + " " + genVar(var) )
	sig += ", ".join( formals ) + ")"

	print "<div id=\"meth\"><h1>[{0}] {1}</h1></div>".format(cl, sig)

	print genPart("locals", "Local Variables")
	res = doopconn.locals(method)
	res.sort()
	for elem in res:
		parts = elem.split(", ")
		_, var = parts[1].split("/")
		print genElem( "{0} {1}".format(parts[0], genVar(var)) )
	print genPartEnd()

	print genPart("allocations", "Allocations")
	res = doopconn.allocations(method)
	for elem in res:
		parts = elem.split(", ")
		_, var = parts[0].split("/")
		heap = "/".join( parts[1].split("/")[-2:] )
		print genElem( "{0} = {1}".format(genVar(var), genHeap(heap)) )
	print genPartEnd()

	print genPart("assigns", "Assigns")
	res = doopconn.assigns(method)
	for elem in res:
		parts = elem.split(", ")
		_, toVar = parts[0].split("/")
		_, fromVar = parts[1].split("/")
		print genElem( "{0} = {1}".format(genVar(toVar), genVar(fromVar)) )
	print genPartEnd()

	print genPart("casts", "Casts")
	res = doopconn.casts(method)
	for elem in res:
		parts = elem.split(", ")
		_, toVar = parts[0].split("/")
		_, fromVar = parts[2].split("/")
		print genElem( "{0} = ({1}) {2}".format(genVar(toVar), parts[1], genVar(fromVar)) )
	print genPartEnd()

	print genPart("loadFlds", "Load Instance Fields")
	res = doopconn.loadInstanceFields(method)
	for elem in res:
		parts = elem.split(", ")
		_, toVar = parts[0].split("/")
		_, baseVar = parts[1].split("/")
		_, fld = parts[2].split(": ")
		_, fld = fld.split(" ")
		fld = fld[:-1]
		print genElem( "{0} = {1} . {2}".format(genVar(toVar), genVar(baseVar), genVar(fld, "$from$"+baseVar)) )
	print genPartEnd()

	print genPart("storeFlds", "Store Instance Fields")
	res = doopconn.storeInstanceFields(method)
	for elem in res:
		parts = elem.split(", ")
		_, baseVar = parts[0].split("/")
		_, fld = parts[1].split(": ")
		_, fld = fld.split(" ")
		fld = fld[:-1]
		_, fromVar = parts[2].split("/")
		print genElem( "{0} . {1} = {2}".format(genVar(baseVar), genVar(fld, "$from$"+baseVar), genVar(fromVar)) )
	print genPartEnd()

	print genPart("loadStaticFlds", "Load Static Fields")
	res = doopconn.loadStaticFields(method)
	for elem in res:
		parts = elem.split(", ")
		_, toVar = parts[0].split("/")
		_, fld = parts[2].split(": ")
		_, fld = fld.split(" ")
		fld = fld[:-1]
		print genElem( "{0} = {1} . {2}".format(genVar(toVar), parts[1], genVar(fld, "$staticFld$"+parts[1])) )
	print genPartEnd()

	print genPart("storeStaticFlds", "Store Static Fields")
	res = doopconn.storeStaticFields(method)
	for elem in res:
		parts = elem.split(", ")
		_, fld = parts[1].split(": ")
		_, fld = fld.split(" ")
		fld = fld[:-1]
		_, fromVar = parts[2].split("/")
		print genElem( "{0} . {1} = {2}".format(parts[0], genVar(fld, "$staticFld$"+parts[0]), genVar(fromVar)) )
	print genPartEnd()

	print genPart("loadArr", "Load Arrays")
	res = doopconn.loadArrays(method)
	for elem in res:
		parts = elem.split(", ")
		_, toVar = parts[0].split("/")
		_, fromVar = parts[1].split("/")
		print genElem( "{0} = {1} [ {2} ]".format(genVar(toVar), genVar(fromVar), genVar("?", fromVar+"$index$")) )
	print genPartEnd()

	print genPart("storeArr", "Store Arrays")
	res = doopconn.storeArrays(method)
	for elem in res:
		parts = elem.split(", ")
		_, toVar = parts[0].split("/")
		_, fromVar = parts[1].split("/")
		print genElem( "{0} [ {1} ] = {2}".format(genVar(toVar), genVar("?", toVar+"$index$"), genVar(fromVar)) )
	print genPartEnd()

	print genPart("returns", "Returns")
	res = doopconn.returns(method)
	for elem in res:
		_, var = elem.split("/")
		print genElem( "return {0}".format(genVar(var)) )
	print genPartEnd()

	def printInvocations(res, linkInvocationFlag=False):
		returnStr = mainStr = ""
		prev = None
		for elem in res:
			parts = elem.split(", ")
			_, invo = parts[0].split("/", 1)
			_, var = parts[2].split("/")
			invo = filterHTML(invo)

			if invo != prev:
				if prev != None:
					print genElem( "{0}{1}{2})".format(returnStr, mainStr, ", ".join(actuals)) )
				returnStr = ""
				if linkInvocationFlag:
					mainStr = "{0} (".format( genVar(invo) )
				else:
					mainStr = "{0} (".format(invo)
				actuals = []
				prev = invo

			if parts[1] == "-2":
				returnStr = "{0} = ".format(genVar(var))
			elif parts[1] == "-1":
				mainStr = "{0} . {1}".format(genVar(var), mainStr)
			else:
				actuals.append(genVar(var))
		
		if prev != None:
			print genElem( "{0}{1}{2})".format(returnStr, mainStr, ", ".join(actuals)) )

	print genPart("specialInvo", "Special Method Invocations")
	res = doopconn.specialInv(method)
	res.sort()
	printInvocations(res)
	print genPartEnd()

	print genPart("virtualInvo", "Virtual Method Invocations")
	res = doopconn.virtualInv(method)
	res.sort()
	printInvocations(res, True)
	print genPartEnd()

	print genPart("staticInvo", "Static Method Invocations")
	res = doopconn.staticInv(method)
	res.sort()
	printInvocations(res)
	res = doopconn.staticInvNoVars(method)
	for elem in res:
		_, invo = elem.split("/", 1)
		invo = filterHTML(invo)
		print genElem( "{0} ()".format(invo) )
	print genPartEnd()


	print "<hr /><hr />"
	print genPart("results", "Results")
	res = doopconn.varPointsTo(method)
	res.sort()
	res = res + doopconn.nullVars(method)
	prev = None
	for elem in res:
		var, heap = elem.split(", ")
		_, var = var.split("/")
		heap = filterHTML(heap)
		if prev != var:
			print genVarPointsHead(var, heap)
			prev = var
		print genElem("" if heap == "@" else heap)
	print genPartEnd()

	print genPart("callGraph", "Call Graph")
	res = doopconn.virtualCallGraph(method)
	res.sort()
	prev = None
	for elem in res:
		invo, meth = elem.split(", ")
		_, invo = invo.split("/", 1)
		meth = meth.replace("<", "").replace(">", "")
		if prev != invo:
			print genVarPointsHead(invo, None)
			prev = invo
		print genElem( meth )
	print genPartEnd()

	print genPart("fldPointsTo", "Field Points To")
	res = doopconn.fldPointsTo(method)
	res.sort()
	res = res + doopconn.nullFldPointsTo(method)
	prev = None
	for elem in res:
		parts = elem.split(", ")
		fld = cleanFld(parts[0])
		_, base = parts[1].split("/")
		id = "{0}$from${1}".format(fld, base)
		if prev != id:
			print genVarPointsHead(id, parts[3])
			prev = id
		print genElem( "{0} ~~(fld)~~> {1}".format( filterHTML(parts[2]), filterHTML(parts[3]) ) )
	print genPartEnd()

	print genPart("staticFldPointsTo", "Static Field Points To")
	res = doopconn.staticFldPointsTo(method)
	res.sort()
	res = res + doopconn.nullStaticFldPointsTo(method)
	prev = None
	for elem in res:
		parts = elem.split(", ")
		fld = cleanFld(parts[1])
		id = "{0}$staticFld${1}".format(fld, parts[0])
		if prev != id:
			print genVarPointsHead(id, parts[2])
			prev = id
		print genElem( filterHTML(parts[2]) )
	print genPartEnd()
	
	print genPart("array", "Array Index")
	res = doopconn.arrayPointsTo(method)
	res.sort()
	res = res + doopconn.nullArrayPointsTo(method)
	prev = None
	for elem in res:
		parts = elem.split(", ")
		_, base = parts[0].split("/")
		id = "?{0}$index$".format(base)
		if prev != id:
			print genVarPointsHead(id, parts[2])
			prev = id
		print genElem( "{0} ~~[index]~~> {1}".format( filterHTML(parts[1]), filterHTML(parts[2]) ) )
	print genPartEnd()


def main(cmd):
	if isinstance(cmd, basestring):
		cmd = cmd.split()

    # Command-line argument parsing
	parser = argparse.ArgumentParser(
		usage = 'toHTML.py [-h] workspace method')

	parser.add_argument('workspace', 
		help = 'the db directory of a Doop static analysis')
	parser.add_argument('method', 
		help = 'the target method to reconstruct')

	args = parser.parse_args(cmd)
     
	genHTML(args.workspace, args.method)

if __name__ == "__main__":
    main(sys.argv[1:])
