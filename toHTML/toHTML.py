#!/usr/bin/env python

import argparse, doop, sys, re, hashlib
from decimal import *

def cleanVar(var):
	_, var = var.split("/", 1)
	return var

def cleanFld(fld):
	_, fld = fld.split(": ")
	_, fld = fld.split(" ")
	return fld[:-1]

def cleanHeap(heap, stringConstants):
	constant = True if heap in stringConstants else False
	heap = heap.replace("<", "").replace(">", "")
	if constant: return "<b>\"{0}\"</b>".format(heap)
	else: return heap

def filterHTML(value):
	return value.replace("<", "&lt;").replace(">", "&gt;")

def printInvocations(file, res, linkInvocation = False):
	returnStr = mainStr = ""
	prev = None
	for elem in res:
		parts = elem.split(", ")
		_, invo = parts[0].split("/", 1)
		invo = filterHTML(invo)
		var = genLink( cleanVar(parts[2]) )

		if invo != prev:
			if prev != None:
				toFile(genElem( "{0}{1}{2})".format(returnStr, mainStr, ", ".join(actuals)) ), file = file)
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
		toFile(genElem( "{0}{1}{2})".format(returnStr, mainStr, ", ".join(actuals)) ), file = file)

def getColourClass(cnt):
	if int(cnt) == 0:
		return "emptyPTSet"
	elif int(cnt) == 1:
		return "singlePTSet"
	elif int(cnt) >= 2:
		return "multiplePTSet"
	elif int(cnt) <= -2:
		return "multiplePTSet singleTypePTSet"
	else:
		return "neutral"

def genHeader(title):
	return "\n<h2>{0}</h2>".format(title)

def genGroupHeader(value, colourClass = "neutral", id = None):
	id = value if id == None else id
	return "<h3 class=\"{2}\"><a id=\"{0}\">{1}</a></h3><div>".format(id, value, colourClass)

def genGroupHeader2(value, colourClass):
	return "<h4 class=\"{1}\">{0}</h4><div>".format(value, colourClass)

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
		body {{
			font-family: Consolas, Monaco, 'Andale Mono', monospace;
		}}
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
		.emptyPTSet {{
			background: Brown;
		}}
		.singlePTSet {{
			background: LightGreen;
		}}
		.multiplePTSet {{
			background: Khaki;
		}}
		.singleTypePTSet {{
			background-image: repeating-linear-gradient(45deg, transparent, transparent 50px, LightGreen 50px, LightGreen 100px);
		}}
		.neutral {{
			background: Silver;
		}}
	</style>
</head>
<body>
"""

FOOTER = """
</body>
</html>
"""


def h(x): sha = hashlib.sha512(x) ; return sha.hexdigest()

def toFile(str, method = None, file = None):
	if file == None:
		if method != None: file = open("HTMLs/{0}".format(h(method)), 'a')
		else: raise Exception("Method name not given")
	file.write(str + "\n")
	return file

def splitPerMethod(res):
	d = {}
	for elem in res:
		method, rest = elem.split(", ", 1)
		if method in d: d[method].append(rest)
		else: d[method] = [rest]
	return d


def genHTML(db):
	doopconn = doop.Connector(db)

	modifiersPerMethod = {}
	d = splitPerMethod( doopconn.modifiers() )
	for method in d:
		modifiersPerMethod[method] = " ".join( d[method] )

	formalsPerMethod = {}
	d = splitPerMethod( doopconn.formals() )
	for method in d:
		formals = []
		d[method].sort()
		for elem in d[method]:
			parts = elem.split(", ")
			formal = genLink( cleanVar(parts[2]) )
			formals.append( "{0} {1}".format(parts[1], formal) )
		formalsPerMethod[method] = ", ".join( formals )

	d = doopconn.reachable()
	for method in d:
		cl, sig = method[1:-1].split(": ")
		sig, _ = sig.split("(")
		modifiers = modifiersPerMethod[method] if method in modifiersPerMethod else ""
		formals = formalsPerMethod[method] if method in formalsPerMethod else ""
		sig = modifiers + " " + filterHTML(sig) + "(" + formals + ")"
		file = toFile(HEADER.format(filterHTML(sig)), method = method)
		toFile("<h1>[{0}] {1}</h1>".format(cl, filterHTML(sig)), file = file)


	stringConstants = doopconn.stringConstants()

	## TODO: Handle empty sets

	d = splitPerMethod( doopconn.locals() )
	for method in d:
		file = toFile(genGroupHeader("Local Variables"), method = method)
		for elem in d[method]:
			cls, var = elem.split(", ")
			var = genLink( cleanVar(var) )
			toFile(genElem("{0} {1}".format(cls, var)), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.allocations() )
	for method in d:
		file = toFile(genGroupHeader("Allocations"), method = method)
		for elem in d[method]:
			var, heap = elem.split(", ", 1)
			var = genLink( cleanVar(var) )
			heap = cleanHeap( "/".join( heap.split("/")[-2:] ), stringConstants )
			toFile(genElem( "{0} = {1}".format(var, heap) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.assigns() )
	for method in d:
		file = toFile(genGroupHeader("Assigns"), method = method)
		for elem in d[method]:
			toVar, fromVar = elem.split(", ")
			toVar = genLink( cleanVar(toVar) )
			fromVar = genLink( cleanVar(fromVar) )
			toFile(genElem( "{0} = {1}".format(toVar, fromVar) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)
		
	d = splitPerMethod( doopconn.casts() )
	for method in d:
		file = toFile(genGroupHeader("Casts"), method = method)
		for elem in d[method]:
			parts = elem.split(", ")
			toVar = genLink( cleanVar(toVar) )
			fromVar = genLink( cleanVar(fromVar) )
			toFile(genElem( "{0} = ({1}) {2}".format(toVar, parts[1], fromVar) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)


	modD = splitPerMethod( doopconn.fldModifiers() )
	modifiersPerMethod = {}
	for method in modD:
		modifiers = {}
		t = []
		prev = None
		for elem in modD[method]:
			fld, mod = elem.split(", ")
			if prev != fld:
				if prev != None: modifiers[prev] = " ".join( t )
				t = []
				prev = fld
			t.append(mod)
		if prev != None: modifiers[prev] = " ".join( t )
		modifiersPerMethod[method] = modifiers

	#getMods = lambda m, x: genComment(modifiersPerMethod[m][x]) if x in modifiersPerMethod[m] else ""
	def getMods(m, x):
		#if m not in modifiersPerMethod: print "(MISSING METHOD) " + m
		return genComment(modifiersPerMethod[m][x]) if m in modifiersPerMethod and x in modifiersPerMethod[m] else ""


	d = splitPerMethod( doopconn.loadInstanceFields() )
	for method in d:
		file = toFile(genGroupHeader("Load Instance Fields"), method = method)
		for elem in d[method]:
			parts = elem.split(", ")
			toVar = genLink( cleanVar(parts[0]) )
			baseVar = cleanVar(parts[1])
			fld = cleanFld(parts[2])
			fld = genLink( fld, fld+"$from$"+baseVar )
			toFile(genElem( "{0} = {1} . {2} {3}".format(toVar, genLink(baseVar), fld, getMods(method, parts[2])) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.storeInstanceFields() )
	for method in d:
		file = toFile(genGroupHeader("Store Instance Fields"), method = method)
		for elem in d[method]:
			parts = elem.split(", ")
			baseVar = cleanVar(parts[0])
			fld = cleanFld(parts[1])
			fld = genLink( fld, fld+"$from$"+baseVar )
			fromVar = genLink( cleanVar(parts[2]) )
			toFile(genElem( "{0} . {1} = {2} {3}".format(genLink(baseVar), fld, fromVar, getMods(method, parts[1])) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.loadStaticFields() )
	for method in d:
		file = toFile(genGroupHeader("Load Static Fields"), method = method)
		for elem in d[method]:
			parts = elem.split(", ")
			toVar = genLink( cleanVar(parts[0]) )
			fld = cleanFld(parts[2])
			fld = genLink( fld, fld+"$staticFld$"+parts[1] )
			toFile(genElem( "{0} = {1} . {2} {3}".format(toVar, parts[1], fld, getMods(method, parts[2])) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.storeStaticFields() )
	for method in d:
		file = toFile(genGroupHeader("Store Static Fields"), method = method)
		for elem in d[method]:
			parts = elem.split(", ")
			fld = cleanFld(parts[1])
			fld = genLink( fld, fld+"$staticFld$"+parts[0] )
			fromVar = genLink( cleanVar(parts[2]) )
			toFile(genElem( "{0} . {1} = {2} {3}".format(parts[0], fld, fromVar, getMods(method, parts[1])) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.loadArrays() )
	for method in d:
		file = toFile(genGroupHeader("Load Arrays"), method = method)
		for elem in d[method]:
			toVar, fromVar = elem.split(", ")
			toVar = genLink( cleanVar(toVar) )
			fromVar = cleanVar(fromVar)
			toFile(genElem( "{0} = {1} [ {2} ]".format(toVar, genLink(fromVar), genLink("?", fromVar+"$index$")) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.storeArrays() )
	for method in d:
		file = toFile(genGroupHeader("Store Arrays"), method = method)
		for elem in d[method]:
			toVar, fromVar = elem.split(", ")
			toVar = cleanVar(toVar)
			fromVar = genLink( cleanVar(fromVar) )
			toFile(genElem( "{0} [ {1} ] = {2}".format(genLink(toVar), genLink("?", toVar+"$index$"), fromVar) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.returns() )
	for method in d:
		file = toFile(genGroupHeader("Returns"), method = method)
		for elem in d[method]:
			toFile(genElem( "return {0}".format(genLink(cleanVar(elem))) ), file = file)
		toFile(genGroupHeaderEnd(), file = file)


	d = splitPerMethod( doopconn.specialInv() )
	for method in d:
		file = toFile(genGroupHeader("Special Method Invocations"), method = method)
		d[method].sort()
		printInvocations(file, d[method])
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.virtualInv() )
	for method in d:
		file = toFile(genGroupHeader("Virtual Method Invocations"), method = method)
		d[method].sort()
		printInvocations(file, d[method], True)
		toFile(genGroupHeaderEnd(), file = file)

	d = splitPerMethod( doopconn.staticInv() )
	d2 = splitPerMethod( doopconn.staticInvNoVars() )
	for method in d:
		file = toFile(genGroupHeader("Static Method Invocations"), method = method)
		d[method].sort()
		printInvocations(file, d[method])
		# Static Method Invocations without any variable (arguments, return)
		if method in d2:
			for elem in d2[method]:
				_, invo = elem.split("/", 1)
				toFile(genElem( "{0} ()".format(filterHTML(invo)) ), file = file)

		toFile(genGroupHeaderEnd(), file = file)
	# Methods not covered before
	for method in d2:
		if method not in d:
			file = toFile(genGroupHeader("Static Method Invocations"), method = method)
			for elem in d2[method]:
				_, invo = elem.split("/", 1)
				toFile(genElem( "{0} ()".format(filterHTML(invo)) ), file = file)
			toFile(genGroupHeaderEnd(), file = file)
	d2 = None

	return





	print "<div style=\"margin-top: 40px; border: 5px dashed grey;\"></div>"
	print genHeader("Variables")
	counts = dict(elem.split(", ") for elem in doopconn.varPointsToCounts(method))
	res = doopconn.varPointsTo(method)
	res.sort()
	prev = None
	for elem in res:
		var, heap = elem.split(", ")
		counter = counts[var]
		colourClass = getColourClass(counter)
		var = cleanVar(var)
		heap = cleanHeap(heap, stringConstants)
		if prev != var:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(var, colourClass)
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
		colourClass = getColourClass(counter)
		if prev != id:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(base+"."+fld, id = id)
			prev = id
			prevHeap = None
		if prevHeap != parts[2]:
			if prevHeap != None: print genGroupHeaderEnd()
			print genGroupHeader2(cleanHeap(parts[2], stringConstants), colourClass)
			prevHeap = parts[2]
		if counter != "0": print genElem( cleanHeap(parts[3], stringConstants) )
	if res: print genGroupHeaderEnd() + genGroupHeaderEnd()

	counts = dict(elem.split(", ") for elem in doopconn.staticFldPointsToCounts(method))
	res = doopconn.staticFldPointsTo(method)
	res.sort()
	prev = None
	for elem in res:
		parts = elem.split(", ")
		counter = counts[parts[1]]
		colourClass = getColourClass(counter)
		fld = cleanFld(parts[1])
		id = "{0}$staticFld${1}".format(fld, parts[0])
		if prev != id:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(parts[0]+"."+fld, colourClass, id)
			prev = id
		if counter != "0": print genElem( cleanHeap(parts[2], stringConstants) )
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
		colourClass = getColourClass(counter)
		if prev != id:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(base+" [ ? ]", id = id)
			prev = id
			prevHeap = None
		if prevHeap != parts[1]:
			if prevHeap != None: print genGroupHeaderEnd()
			print genGroupHeader2(cleanHeap(parts[1], stringConstants), colourClass)
			prevHeap = parts[1]
		if counter != "0": print genElem( cleanHeap(parts[2], stringConstants) )
	if res: print genGroupHeaderEnd() + genGroupHeaderEnd()

	print genHeader("Virtual Call Graph")
	counts = dict(elem.split(", ") for elem in doopconn.virtualCallGraphCounts(method))
	res = doopconn.virtualCallGraph(method)
	res.sort()
	prev = None
	for elem in res:
		invo, meth = elem.split(", ")
		counter = counts[invo]
		colourClass = getColourClass(counter)
		_, invo = invo.split("/", 1)
		if prev != invo:
			if prev != None: print genGroupHeaderEnd()
			print genGroupHeader(invo, colourClass)
			prev = invo
		if counter != "0": print genElem( cleanHeap(meth, stringConstants) )
	if res: print genGroupHeaderEnd()

	print FOOTER


def main(cmd):
	if isinstance(cmd, basestring):
		cmd = cmd.split()

	parser = argparse.ArgumentParser(
		usage = 'toHTML.py [-h] workspace')

	parser.add_argument('workspace', 
		help = 'the db directory of a Doop static analysis')

	args = parser.parse_args(cmd)
     
	genHTML(args.workspace)

if __name__ == "__main__":
    main(sys.argv[1:])
