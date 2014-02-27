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
	MethodSignatureRef(meth), Var:DeclaringMethod(local, meth),
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
	meth = "{0}", MethodSignatureRef(meth),
	Var:DeclaringMethod(var, meth), VarPointsTo(_, heap, _, var).
"""

NULL_VARS = """
_(var, "@") <-
	meth = "{0}", MethodSignatureRef(meth),
	Var:DeclaringMethod(var, meth), !VarPointsTo(_, _, _, var).
"""

VIRTUAL_CALL_GRAPH = """
_(invo, toMeth) <-
	meth = "{0}",
	VirtualMethodInvocation:In(invo, meth), 
	CallGraphEdge(_, invo, _, toMeth).
"""

FLD_POINTS_TO = """
_(fld, base, baseHeap, heap) <-
	meth = "{0}",
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	InstanceFieldPointsTo(_, heap, fld, _, baseHeap).
"""

NULL_FLD_POINTS_TO = """
_(fld, base, baseHeap, "@") <-
	meth = "{0}",
	(LoadInstanceField(base, fld, _, meth) ; StoreInstanceField(_, base, fld, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!InstanceFieldPointsTo(_, _, fld, _, baseHeap).
"""

STATIC_FLD_POINTS_TO = """
_(cls, fld, heap) <-
	meth = "{0}",
	(LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	StaticFieldPointsTo(_, heap, fld), Field:DeclaringClass[fld] = cls.
"""

NULL_STATIC_FLD_POINTS_TO = """
_(cls, fld, "@") <-
	meth = "{0}",
	(LoadStaticField(fld, _, meth) ; StoreStaticField(_, fld, meth)),
	!StaticFieldPointsTo(_, _, fld), Field:DeclaringClass[fld] = cls.
"""

ARRAY_POINTS_TO = """
_(base, baseHeap, heap) <-
	meth = "{0}",
	(LoadArrayIndex(base, _, meth) ; StoreArrayIndex(_, base, meth)),
	VarPointsTo(_, baseHeap, _, base),
	ArrayIndexPointsTo(_, heap, _, baseHeap).
"""

NULL_ARRAY_POINTS_TO = """
_(base, baseHeap, "@") <-
	meth = "{0}",
	(LoadArrayIndex(base, _, meth) ; StoreArrayIndex(_, base, meth)),
	VarPointsTo(_, baseHeap, _, base),
	!ArrayIndexPointsTo(_, _, _, baseHeap).
"""
