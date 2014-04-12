REACHABLE = """_(meth) <- Reachable(meth)."""

MODIFIERS = """
_(meth, mod) <-
	Reachable(meth), MethodModifier(mod, meth).
"""

FORMALS = """
_(meth, index, type, formal) <-
	Reachable(meth), FormalParam[index, meth] = formal, Var:Type[formal] = type.
"""

LOCALS = """
_(meth, type, local) <-
	_localVar(local, meth), Var:Type[local] = type.

_localVar(local, meth) <-

	Reachable(meth), Var:DeclaringMethod(local, meth),
	!FormalParam[_, meth] = local, !ThisVar[meth] = local.
"""

ALLOCATIONS = """
_(meth, var, heap) <-
	Reachable(meth), AssignHeapAllocation(heap, var, meth).
"""

ASSIGNS = """
_(meth, to, from) <-
	Reachable(meth), AssignLocal(from, to, meth).
"""

CASTS = """
_(meth, to, type, from) <-
	Reachable(meth), AssignCast(type, from, to, meth).
"""

FLD_MODIFIERS = """
_(meth, fld, mod) <-
	Reachable(meth),
	(LoadInstanceField(_, fld, _, meth) ; StoreInstanceField(_, _, fld, meth) ;
	 LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	FieldModifier(mod, fld).
"""

LOAD_INSTANCE_FIELDS = """
_(meth, to, base, fld) <-
	Reachable(meth), LoadInstanceField(base, fld, to, meth).
"""

LOAD_STATIC_FIELDS = """
_(meth, to, cls, fld) <-
	Reachable(meth), LoadStaticField(fld, to, meth), Field:DeclaringClass[fld] = cls.
"""

STORE_INSTANCE_FIELDS = """
_(meth, base, fld, from) <-
	Reachable(meth), StoreInstanceField(from, base, fld, meth).
"""

STORE_STATIC_FIELDS = """
_(meth, cls, fld, from) <-
	Reachable(meth), StoreStaticField(from, fld, meth), Field:DeclaringClass[fld] = cls.
"""

LOAD_ARRAYS = """
_(meth, to, base) <-
	Reachable(meth), LoadArrayIndex(base, to, meth).
"""

STORE_ARRAYS = """
_(meth, base, from) <-
	Reachable(meth), StoreArrayIndex(from, base, meth).
"""

RETURNS = """
_(meth, var) <-
	Reachable(meth), ReturnVar(var, meth).
"""


SPECIAL_INV = """
_t(meth, invo) <-
	Reachable(meth), SpecialMethodInvocation:In(invo, meth).

_(meth, invo, index, base) -> MethodSignatureRef(meth), MethodInvocationRef(invo), int[32](index), VarRef(base).

_(meth, invo, -1, base) <-
	_t(meth, invo), SpecialMethodInvocation:Base[invo] = base.

_(meth, invo, index, actual) <-
	_t(meth, invo), ActualParam[index, invo] = actual.

_(meth, invo, -2, ret) <-
	_t(meth, invo), AssignReturnValue[invo] = ret.
"""

VIRTUAL_INV = """
_t(meth, invo) <-
	Reachable(meth), VirtualMethodInvocation:In(invo, meth).

_(meth, invo, index, base) -> MethodSignatureRef(meth), MethodInvocationRef(invo), int[32](index), VarRef(base).

_(meth, invo, -1, base) <-
	_t(meth, invo), VirtualMethodInvocation:Base[invo] = base.

_(meth, invo, index, actual) <-
	_t(meth, invo), ActualParam[index, invo] = actual.

_(meth, invo, -2, ret) <-
	_t(meth, invo), AssignReturnValue[invo] = ret.
"""

STATIC_INV = """
_t(meth, invo) <-
	Reachable(meth), StaticMethodInvocation:In(invo, meth).

_(meth, invo, index, base) -> MethodSignatureRef(meth), MethodInvocationRef(invo), int[32](index), VarRef(base).

_(meth, invo, index, actual) <-
	_t(meth, invo), ActualParam[index, invo] = actual.

_(meth, invo, -2, ret) <-
	_t(meth, invo), AssignReturnValue[invo] = ret.
"""

STATIC_INV_NO_VARS = """
_(meth, invo) <-
	Reachable(meth), StaticMethodInvocation:In(invo, meth),
	!AssignReturnValue[invo] = _, !ActualParam[_, invo] = _.
"""



VAR_POINTS_TO = """
_(meth, var, heap) <-
	Reachable(meth), Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var).

_(meth, var, dummy) <-
	Reachable(meth), Var:DeclaringMethod(var, meth), !VarPointsTo(_, _, _, var),
	MainMethodArgsArray(dummy).
"""

VAR_POINTS_TO_COUNTS = """
_(meth, var, 0) <-
	Reachable(meth), Var:DeclaringMethod(var, meth), !VarPointsTo(_, _, _, var).

_(meth, var, cnt) <- _c[meth, var] = cnt.

_t(meth, var, heap) <-
	Reachable(meth), Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var).

_c[meth, var] = cnt <- agg<<cnt = count()>> _t(meth, var, _).
"""

"""
Group separately for >1 VP but with exactly the same type
VAR_POINTS_TO_COUNTS =
_(var, 0) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), !VarPointsTo(_, _, _, var).

_(var, cnt) <- _c[var] = cnt, cnt = 1.
_(var, cnt) <- _c[var] = cnt, cnt >= 2, _tc[var] >= 2.
_(var, cnt2) <- _c[var] = cnt, cnt >= 2, _tc[var] = 1, cnt2 = -1 * cnt.

_t(var, heap) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var).

_c[var] = cnt <- agg<<cnt = count()>> _t(var, _).

_tt(var, type) <-
	meth = "{0}", Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var), HeapAllocation:Type[heap] = type.

_tc[var] = cnt <- agg<<cnt = count()>> _tt(var, _).
"""

FLD_POINTS_TO = """
_(meth, fld, base, baseHeap, heap) <-
	Reachable(meth),
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	InstanceFieldPointsTo(_, heap, fld, _, baseHeap).

_(meth, fld, base, baseHeap, dummy) <-
	Reachable(meth),
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!InstanceFieldPointsTo(_, _, fld, _, baseHeap),
	MainMethodArgsArray(dummy).
"""

FLD_POINTS_TO_COUNTS = """
_(meth, baseHeap, fld, 0) <-
	Reachable(meth),
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!InstanceFieldPointsTo(_, _, fld, _, baseHeap).

_(meth, baseHeap, fld, cnt) <- _c[meth, baseHeap, fld] = cnt.

_t(meth, baseHeap, fld, heap) <-
	Reachable(meth),
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	InstanceFieldPointsTo(_, heap, fld, _, baseHeap).

_c[meth, baseHeap, fld] = cnt <- agg<<cnt = count()>> _t(meth, baseHeap, fld, _).
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

STRING_CONSTANTS = """
_(heap) <- StringConstant(heap), !HeapAllocation:Merge[heap] = _.
"""
