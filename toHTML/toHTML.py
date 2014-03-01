#!/usr/bin/env python

import argparse, doop, sys, re
from decimal import *

def cleanVar(var):
	_, var = var.split("/")
	return var

def cleanFld(fld):
	_, fld = fld.split(": ")
	_, fld = fld.split(" ")
	return fld[:-1]

def cleanHeap(heap):
	return heap.replace("<", "").replace(">", "")

def filterHTML(value):
	return value.replace("<", "&lt;").replace(">", "&gt;")

def printInvocations(res, linkInvocation=False):
	returnStr = mainStr = ""
	prev = None
	for elem in res:
		parts = elem.split(", ")
		_, invo = parts[0].split("/", 1)
		invo = filterHTML(invo)
		var = genLink( cleanVar(parts[2]) )

		if invo != prev:
			if prev != None:
				print genElem( "{0}{1}{2})".format(returnStr, mainStr, ", ".join(actuals)) )
			returnStr = ""
			if linkInvocation:
				mainStr = "{0} (".format(genLink(invo))
			else:
				mainStr = "{0} (".format(invo)
			actuals = []
			prev = invo

		if parts[1] == "-2":
			returnStr = "{0} = ".format(var)
		elif parts[1] == "-1":
			mainStr = "{0} . {1}".format(var, mainStr)
		else:
			actuals.append(var)
	
	if prev != None:
		print genElem( "{0}{1}{2})".format(returnStr, mainStr, ", ".join(actuals)) )


def getColour(cnt):
	if cnt == "0":
		return "Brown"
	elif cnt == "1":
		return "LightGreen"
	else:
		return "Khaki"

def genHeader(title):
	return "\n<h2>{0}</h2>".format(title)

def genGroupHeader(value, colour = "Silver", id = None):
	id = value if id == None else id
	return "<h3 style=\"background: {2};\"><a id=\"{0}\">{1}</a></h3><div>".format(id, value, colour)

def genGroupHeader2(value, colour):
	return "<h4 style=\"background: {1};\">{0}</h4><div>".format(value, colour)

def genGroupHeaderEnd():
	return "</div>"

def genElem(element):
	return "<div>{0}</div>".format(element)

def genLink(value, id = None):
	id = value if id == None else id
	return "<a href=\"#{0}\">{1}</a>".format(id, value)

def genComment(value):
	return "<span class=\"comment\">// {0}</span>".format(value)


HEADER = """<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>{0}</title>
	<style type="text/css">
		h2 {{
			background: Silver;
			padding: 15px;
			text-aling: center;
		}}
		h3 {{
			margin-bottom: 0;
			padding: 10px;
			border: 1px solid grey;
		}}
		h4 {{
			margin-bottom: 0;
			padding: 10px;
			border: 1px solid grey;
		}}
		h3 + div, h4 + div {{
			padding: 10px;
			border: 1px solid grey;
			border-top: 0;
		}}
		.comment {{
			margin-left: 20px;
			color: Grey;
			font-style: italic;
		}}
	</style>
</head>
<body>
"""

FOOTER = """
</body>
</html>
"""

def genHTML(db, method):
	doopconn = doop.Connector(db)

	cl, sig = method[1:-1].split(": ")
	sig, _ = sig.split("(")

	print HEADER.format(filterHTML(sig))

	res = " ".join( doopconn.modifiers(method) )
	sig = res + " " + filterHTML(sig) + "("

	res = doopconn.formals(method)
	res.sort()
	formals = []
	for elem in res:
		parts = elem.split(", ")
		formal = genLink( cleanVar(parts[2]) )
		formals.append( "{0} {1}".format(parts[1], formal) )
	sig += ", ".join( formals ) + ")"
	print "<h1>[{0}] {1}</h1>".format(cl, sig)

	print genGroupHeader("Local Variables")
	res = doopconn.locals(method)
	res.sort()
	for elem in res:
		cls, var = elem.split(", ")
		var = genLink( cleanVar(var) )
		print genElem( "{0} {1}".format(cls, var) )
	print genGroupHeaderEnd()

	print genGroupHeader("Allocations")
	res = doopconn.allocations(method)
	for elem in res:
		var, heap = elem.split(", ")
		var = genLink( cleanVar(var) )
		heap = cleanHeap( "/".join( heap.split("/")[-2:] ) )
		print genElem( "{0} = {1}".format(var, heap) )
	print genGroupHeaderEnd()

	print genGroupHeader("Assigns")
	res = doopconn.assigns(method)
	for elem in res:
		toVar, fromVar = elem.split(", ")
		toVar = genLink( cleanVar(toVar) )
		fromVar = genLink( cleanVar(fromVar) )
		print genElem( "{0} = {1}".format(toVar, fromVar) )
	print genGroupHeaderEnd()

	print genGroupHeader("Casts")
	res = doopconn.casts(method)
	for elem in res:
		parts = elem.split(", ")
		toVar = genLink( cleanVar(toVar) )
		fromVar = genLink( cleanVar(fromVar) )
		print genElem( "{0} = ({1}) {2}".format(toVar, parts[1], fromVar) )
	print genGroupHeaderEnd()

	res = doopconn.fldModifiers(method)
	res.sort()
	modifiers = {}
	t = []
	prev = None
	for elem in res:
		fld, mod = elem.split(", ")
		if prev != fld:
			if prev != None: modifiers[prev] = " ".join( t )
			t = []
			prev = fld
		t.append(mod)
	if prev != None: modifiers[prev] = " ".join( t )
	getMods = lambda x: genComment(modifiers[x]) if x in modifiers else ""

	print genGroupHeader("Load Instance Fields")
	res = doopconn.loadInstanceFields(method)
	for elem in res:
		parts = elem.split(", ")
		toVar = genLink( cleanVar(parts[0]) )
		baseVar = cleanVar(parts[1])
		fld = cleanFld(parts[2])
		fld = genLink( fld, fld+"$from$"+baseVar )
		print genElem( "{0} = {1} . {2} {3}".format(toVar, genLink(baseVar), fld, getMods(parts[2])) )
	print genGroupHeaderEnd()

	print genGroupHeader("Store Instance Fields")
	res = doopconn.storeInstanceFields(method)
	for elem in res:
		parts = elem.split(", ")
		baseVar = cleanVar(parts[0])
		fld = cleanFld(parts[1])
		fld = genLink( fld, fld+"$from$"+baseVar )
		fromVar = genLink( cleanVar(parts[2]) )
		print genElem( "{0} . {1} = {2} {3}".format(genLink(baseVar), fld, fromVar, getMods(parts[1])) )
	print genGroupHeaderEnd()

	print genGroupHeader("Load Static Fields")
	res = doopconn.loadStaticFields(method)
	for elem in res:
		parts = elem.split(", ")
		toVar = genLink( cleanVar(parts[0]) )
		fld = cleanFld(parts[2])
		fld = genLink( fld, fld+"$staticFld$"+parts[1] )
		print genElem( "{0} = {1} . {2} {3}".format(toVar, parts[1], fld, getMods(parts[2])) )
	print genGroupHeaderEnd()

	print genGroupHeader("Store Static Fields")
	res = doopconn.storeStaticFields(method)
	for elem in res:
		parts = elem.split(", ")
		fld = cleanFld(parts[1])
		fld = genLink( fld, fld+"$staticFld$"+parts[0] )
		fromVar = genLink( cleanVar(parts[2]) )
		print genElem( "{0} . {1} = {2} {3}".format(parts[0], fld, fromVar, getMods(parts[1])) )
	print genGroupHeaderEnd()

	print genGroupHeader("Load Arrays")
	res = doopconn.loadArrays(method)
	for elem in res:
		toVar, fromVar = elem.split(", ")
		toVar = genLink( cleanVar(toVar) )
		fromVar = cleanVar(fromVar)
		print genElem( "{0} = {1} [ {2} ]".format(toVar, genLink(fromVar), genLink("?", fromVar+"$index$")) )
	print genGroupHeaderEnd()

	print genGroupHeader("Store Arrays")
	res = doopconn.storeArrays(method)
	for elem in res:
		toVar, fromVar = elem.split(", ")
		toVar = cleanVar(toVar)
		fromVar = genLink( cleanVar(fromVar) )
		print genElem( "{0} [ {1} ] = {2}".format(genLink(toVar), genLink("?", toVar+"$index$"), fromVar) )
	print genGroupHeaderEnd()

	print genGroupHeader("Returns")
	res = doopconn.returns(method)
	for elem in res:
		print genElem( "return {0}".format(genLink(cleanVar(elem))) )
	print genGroupHeaderEnd()

	print genGroupHeader("Special Method Invocations")
	res = doopconn.specialInv(method)
	res.sort()
	printInvocations(res)
	print genGroupHeaderEnd()

	print genGroupHeader("Virtual Method Invocations")
	res = doopconn.virtualInv(method)
	res.sort()
	printInvocations(res, True)
	print genGroupHeaderEnd()

	print genGroupHeader("Static Method Invocations")
	res = doopconn.staticInv(method)
	res.sort()
	printInvocations(res)
	res = doopconn.staticInvNoVars(method)
	for elem in res:
		_, invo = elem.split("/", 1)
		print genElem( "{0} ()".format(filterHTML(invo)) )
	print genGroupHeaderEnd()


	print "<div style=\"margin-top: 40px; border: 5px dashed grey;\"></div>"
	print genHeader("Variables")
	counts = dict(elem.split(", ") for elem in doopconn.varPointsToCounts(method))
	res = doopconn.varPointsTo(method)
	res.sort()
	prev = None
	for elem in res:
		var, heap = elem.split(", ")
		counter = counts[var]
		colour = getColour(counter)
		var = cleanVar(var)
		heap = cleanHeap(heap)
		if prev != var:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(var, colour)
			prev = var
		if counter != "0": print genElem(heap)
	if res: print genGroupHeaderEnd()

	print genHeader("Fields")

	g1 = lambda x, y: "{0}, {1}".format(x, y)
	g2 = lambda parts: ( g1(parts[0], parts[1]), parts[2] )
	counts = dict( g2(elem.split(", ")) for elem in doopconn.fldPointsToCounts(method) )
	res = doopconn.fldPointsTo(method)
	res.sort()
	prev = None
	prevHeap = None
	for elem in res:
		parts = elem.split(", ")
		fld = cleanFld(parts[0])
		base = cleanVar(parts[1])
		id = "{0}$from${1}".format(fld, base)
		counter = counts[ g1(parts[2], parts[0]) ]
		colour = getColour(counter)
		if prev != id:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(base+"."+fld, id = id)
			prev = id
			prevHeap = None
		if prevHeap != parts[2]:
			if prevHeap != None: print genGroupHeaderEnd()
			print genGroupHeader2(cleanHeap(parts[2]), colour)
			prevHeap = parts[2]
		if counter != "0": print genElem( cleanHeap(parts[3]) )
	if res: print genGroupHeaderEnd() + genGroupHeaderEnd()

	counts = dict(elem.split(", ") for elem in doopconn.staticFldPointsToCounts(method))
	res = doopconn.staticFldPointsTo(method)
	res.sort()
	prev = None
	for elem in res:
		parts = elem.split(", ")
		counter = counts[parts[1]]
		colour = getColour(counter)
		fld = cleanFld(parts[1])
		id = "{0}$staticFld${1}".format(fld, parts[0])
		if prev != id:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(parts[0]+"."+fld, colour, id)
			prev = id
		if counter != "0": print genElem( cleanHeap(parts[2]) )
	if res: print genGroupHeaderEnd()
	
	print genHeader("Arrays")
	counts = dict(elem.split(", ") for elem in doopconn.arrayPointsToCounts(method))
	res = doopconn.arrayPointsTo(method)
	res.sort()
	prev = None
	prevHeap = None
	for elem in res:
		parts = elem.split(", ")
		_, base = parts[0].split("/")
		id = "{0}$index$".format(base)
		counter = counts[parts[1]]
		colour = getColour(counter)
		if prev != id:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(base+" [ ? ]", id = id)
			prev = id
			prevHeap = None
		if prevHeap != parts[1]:
			if prevHeap != None: print genGroupHeaderEnd()
			print genGroupHeader2(cleanHeap(parts[1]), colour)
			prevHeap = parts[1]
		if counter != "0": print genElem( cleanHeap(parts[2]) )
	if res: print genGroupHeaderEnd() + genGroupHeaderEnd()

	print genHeader("Virtual Call Graph")
	counts = dict(elem.split(", ") for elem in doopconn.virtualCallGraphCounts(method))
	res = doopconn.virtualCallGraph(method)
	res.sort()
	prev = None
	for elem in res:
		invo, meth = elem.split(", ")
		counter = counts[invo]
		colour = getColour(counter)
		_, invo = invo.split("/", 1)
		if prev != invo:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(invo, colour)
			prev = invo
		if counter != "0": print genElem( cleanHeap(meth) )
	if res: print genGroupHeaderEnd()

	print FOOTER


def main(cmd):
	if isinstance(cmd, basestring):
		cmd = cmd.split()

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
