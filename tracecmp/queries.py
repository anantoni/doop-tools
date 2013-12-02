APP_METHODS = """
_(meth) <- 
   Stats:Simple:ApplicationMethod(meth).
"""

APP_TO_APP = """
_(from, to) <- 
   Stats:Simple:InsensCallGraphEdge(callsite, to), 
   Instruction:Method[callsite] = from, 
   Stats:Simple:ApplicationMethod(from), 
   Stats:Simple:ApplicationMethod(to).
"""

APP_TO_LIB = """
_(from, to) <- 
   Stats:Simple:InsensCallGraphEdge(callsite, to), 
   Instruction:Method[callsite] = from, 
   Stats:Simple:ApplicationMethod(from), 
   !Stats:Simple:ApplicationMethod(to).
"""

LIB_TO_APP = """
_(from, to) <- 
   Stats:Simple:InsensCallGraphEdge(callsite, to), 
   Instruction:Method[callsite] = from, 
   !Stats:Simple:ApplicationMethod(from), 
   Stats:Simple:ApplicationMethod(to).
"""

LIB_TO_LIB = """
_(from, to) <- 
   Stats:Simple:InsensCallGraphEdge(callsite, to), 
   Instruction:Method[callsite] = from, 
   !Stats:Simple:ApplicationMethod(from), 
   !Stats:Simple:ApplicationMethod(to).
"""

NULLS = """
_r(inv) <- 
   Stats:Simple:ReachableVirtualMethodInvocation(inv). 

_r(inv) <- 
   Reachable(meth), 
   SpecialMethodInvocation:In(inv, meth).

_n(inv) <- 
   Stats:Simple:NullVirtualMethodInvocation(inv). 

_n(inv) <- 
   _r(inv), 
   SpecialMethodInvocation:Base[inv] = base, 
   !(Stats:Simple:InsensVarPointsTo(_, base)).
"""
