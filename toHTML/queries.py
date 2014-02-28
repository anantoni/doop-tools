MODIFIERS = """
_(mod) <-
	meth = "{0}", MethodModifier(mod, meth).
"""

FORMALS = """
_(index, type, formal) <-
	meth = "{0}", FormalParam[index, meth] = formal, Var:Type[formal] = type.
"""

LOCALS = """
_(type, local) <-
	meth = "{0}", _localVar(local, meth), Var:Type[local] = type.

_localVar(local, meth) <-
	meth = "{0}", Var:DeclaringMethod(local, meth),
	!FormalParam[_, meth] = local, !ThisVar[meth] = local.
"""

ALLOCATIONS = """
_(var, heap) <-
	meth = "{0}", AssignHeapAllocation(heap, var, meth).
"""

ASSIGNS = """
_(to, from) <-
	meth = "{0}", AssignLocal(from, to, meth).
"""

CASTS = """
_(to, type, from) <-
	meth = "{0}", AssignCast(type, from, to, meth).
"""

LOAD_INSTANCE_FIELDS = """
_(to, base, fld) <-
	meth = "{0}", LoadInstanceField(base, fld, to, meth).
"""

LOAD_STATIC_FIELDS = """
_(to, cls, fld) <-
	meth = "{0}", LoadStaticField(fld, to, meth), Field:DeclaringClass[fld] = cls.
"""

STORE_INSTANCE_FIELDS = """
_(base, fld, from) <-
	meth = "{0}", StoreInstanceField(from, base, fld, meth).
"""

STORE_STATIC_FIELDS = """
_(cls, fld, from) <-
	meth = "{0}", StoreStaticField(from, fld, meth), Field:DeclaringClass[fld] = cls.
"""

LOAD_ARRAYS = """
_(to, base) <-
	meth = "{0}", LoadArrayIndex(base, to, meth).
"""

STORE_ARRAYS = """
_(base, from) <-
	meth = "{0}", StoreArrayIndex(from, base, meth).
"""


SPECIAL_INV = """
_t(invo) <-
	meth = "{0}", SpecialMethodInvocation:In(invo, meth).

_(invo, index, base) -> MethodInvocationRef(invo), int[32](index), VarRef(base).

_(invo, -1, base) <-
	_t(invo), SpecialMethodInvocation:Base[invo] = base.

_(invo, index, actual) <-
	_t(invo), ActualParam[index, invo] = actual.

_(invo, -2, ret) <-
	_t(invo), AssignReturnValue[invo] = ret.
"""

VIRTUAL_INV = """
_t(invo) <-
	meth = "{0}", VirtualMethodInvocation:In(invo, meth).

_(invo, index, base) -> MethodInvocationRef(invo), int[32](index), VarRef(base).

_(invo, -1, base) <-
	_t(invo), VirtualMethodInvocation:Base[invo] = base.

_(invo, index, actual) <-
	_t(invo), ActualParam[index, invo] = actual.

_(invo, -2, ret) <-
	_t(invo), AssignReturnValue[invo] = ret.
"""

STATIC_INV = """
_t(invo) <-
	meth = "{0}", StaticMethodInvocation:In(invo, meth).

_(invo, index, base) -> MethodInvocationRef(invo), int[32](index), VarRef(base).

_(invo, index, actual) <-
	_t(invo), ActualParam[index, invo] = actual.

_(invo, -2, ret) <-
	_t(invo), AssignReturnValue[invo] = ret.
"""

STATIC_INV_NO_VARS = """
_(invo) <-
	meth = "{0}", StaticMethodInvocation:In(invo, meth),
	!AssignReturnValue[invo] = _, !ActualParam[_, invo] = _.
"""

RETURNS = """
_(var) <-
	meth = "{0}", ReturnVar(var, meth).
"""



VAR_POINTS_TO = """
_(var, heap) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var).

_(var, dummy) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), !VarPointsTo(_, _, _, var),
	MainMethodArgsArray(dummy).
"""

VAR_POINTS_TO_COUNTS = """
_(var, 0) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), !VarPointsTo(_, _, _, var).

_(var, cnt) <- _c[var] = cnt.

_t(var, heap) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var).

_c[var] = cnt <- agg<<cnt = count()>> _t(var, _).
"""

FLD_POINTS_TO = """
_(fld, base, baseHeap, heap) <-
	meth = "{0}",
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	InstanceFieldPointsTo(_, heap, fld, _, baseHeap).

_(fld, base, baseHeap, dummy) <-
	meth = "{0}",
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!InstanceFieldPointsTo(_, _, fld, _, baseHeap),
	MainMethodArgsArray(dummy).
"""

FLD_POINTS_TO_COUNTS = """
_(baseHeap, fld, 0) <-
	meth = "{0}",
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!InstanceFieldPointsTo(_, _, fld, _, baseHeap).

_(baseHeap, fld, cnt) <- _c[baseHeap, fld] = cnt.

_t(baseHeap, fld, heap) <-
	meth = "{0}",
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	InstanceFieldPointsTo(_, heap, fld, _, baseHeap).

_c[baseHeap, fld] = cnt <- agg<<cnt = count()>> _t(baseHeap, fld, _).
"""

STATIC_FLD_POINTS_TO = """
_(cls, fld, heap) <-
	meth = "{0}",
	(LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	StaticFieldPointsTo(_, heap, fld), Field:DeclaringClass[fld] = cls.

_(cls, fld, dummy) <-
	meth = "{0}",
	(LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	!StaticFieldPointsTo(_, _, fld), Field:DeclaringClass[fld] = cls,
	MainMethodArgsArray(dummy).
"""

STATIC_FLD_POINTS_TO_COUNTS = """
_(fld, 0) <-
	meth = "{0}",
	(LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	!StaticFieldPointsTo(_, _, fld).

_(fld, cnt) <- _c[fld] = cnt.

_t(fld, heap) <-
	meth = "{0}",
	(LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	StaticFieldPointsTo(_, heap, fld).

_c[fld] = cnt <- agg<<cnt = count()>> _t(fld, _).
"""

ARRAY_POINTS_TO = """
_(base, baseHeap, heap) <-
	meth = "{0}",
	(LoadArrayIndex(base, _, meth) ; StoreArrayIndex(_, base, meth)),
	VarPointsTo(_, baseHeap, _, base),
	ArrayIndexPointsTo(_, heap, _, baseHeap).

_(base, baseHeap, dummy) <-
	meth = "{0}",
	(LoadArrayIndex(base, _, meth) ; StoreArrayIndex(_, base, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!ArrayIndexPointsTo(_, _, _, baseHeap),
	MainMethodArgsArray(dummy).
"""

ARRAY_POINTS_TO_COUNTS = """
_(baseHeap, 0) <-
	meth = "{0}",
	(LoadArrayIndex(base, _, meth) ; StoreArrayIndex(_, base, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!ArrayIndexPointsTo(_, _, _, baseHeap).

_(baseHeap, cnt) <- _c[baseHeap] = cnt.

_t(baseHeap, heap) <-
	meth = "{0}",
	(LoadArrayIndex(base, _, meth) ; StoreArrayIndex(_, base, meth)),
	VarPointsTo(_, baseHeap, _, base),
	ArrayIndexPointsTo(_, heap, _, baseHeap).

_c[baseHeap] = cnt <- agg<<cnt = count()>> _t(baseHeap, _).
"""

VIRTUAL_CALL_GRAPH = """
_(invo, toMeth) <-
	meth = "{0}", VirtualMethodInvocation:In(invo, meth), 
	CallGraphEdge(_, invo, _, toMeth).

_(invo, dummy) <-
	meth = "{0}", VirtualMethodInvocation:In(invo, meth), 
	!CallGraphEdge(_, invo, _, _), MainMethodDeclaration(dummy).
"""

VIRTUAL_CALL_GRAPH_COUNTS = """
_(invo, 0) <-
	meth = "{0}", VirtualMethodInvocation:In(invo, meth), 
	!CallGraphEdge(_, invo, _, _).

_(invo, cnt) <- _c[invo] = cnt.

_t(invo, toMeth) <-
	meth = "{0}", VirtualMethodInvocation:In(invo, meth), 
	CallGraphEdge(_, invo, _, toMeth).

_c[invo] = cnt <- agg<<cnt = count()>> _t(invo, _).
"""
