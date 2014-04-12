import blox
from queries import *

class Connector:
	def __init__(self, workspace):
		self._conn = blox.Connector(workspace)

	def __query(self, queryString, **kwargs):
		return self._conn.query(queryString, **kwargs)


	def reachable(self):
		return self.__query(REACHABLE)

	def modifiers(self):
		return self.__query(MODIFIERS)

	def formals(self):
		return self.__query(FORMALS)

	def locals(self):
		return self.__query(LOCALS, toprint = "_")

	def allocations(self):
		return self.__query(ALLOCATIONS)

	def assigns(self):
		return self.__query(ASSIGNS)

	def casts(self):
		return self.__query(CASTS)

	def fldModifiers(self):
		return self.__query(FLD_MODIFIERS)

	def loadInstanceFields(self):
		return self.__query(LOAD_INSTANCE_FIELDS)

	def loadStaticFields(self):
		return self.__query(LOAD_STATIC_FIELDS)

	def storeInstanceFields(self):
		return self.__query(STORE_INSTANCE_FIELDS)

	def storeStaticFields(self):
		return self.__query(STORE_STATIC_FIELDS)

	def loadArrays(self):
		return self.__query(LOAD_ARRAYS)

	def storeArrays(self):
		return self.__query(STORE_ARRAYS)

	def returns(self):
		return self.__query(RETURNS)


	def specialInv(self):
		return self.__query(SPECIAL_INV, toprint = "_")

	def virtualInv(self):
		return self.__query(VIRTUAL_INV, toprint = "_")

	def staticInv(self):
		return self.__query(STATIC_INV, toprint = "_")

	def staticInvNoVars(self):
		return self.__query(STATIC_INV_NO_VARS, toprint = "_")


	def varPointsTo(self):
		return self.__query(VAR_POINTS_TO, toprint = "_")

	def varPointsToCounts(self):
		return self.__query(VAR_POINTS_TO_COUNTS, toprint = "_")


	def fldPointsTo(self):
		return self.__query(FLD_POINTS_TO, toprint = "_")

	def fldPointsToCounts(self):
		return self.__query(FLD_POINTS_TO_COUNTS, toprint = "_")


	def staticFldPointsTo(self, method):
		return self.__query(STATIC_FLD_POINTS_TO.format(method), toprint = "_")

	def staticFldPointsToCounts(self, method):
		return self.__query(STATIC_FLD_POINTS_TO_COUNTS.format(method), toprint = "_")


	def arrayPointsTo(self, method):
		return self.__query(ARRAY_POINTS_TO.format(method), toprint = "_")

	def arrayPointsToCounts(self, method):
		return self.__query(ARRAY_POINTS_TO_COUNTS.format(method), toprint = "_")


	def virtualCallGraph(self, method):
		return self.__query(VIRTUAL_CALL_GRAPH.format(method), toprint = "_")

	def virtualCallGraphCounts(self, method):
		return self.__query(VIRTUAL_CALL_GRAPH_COUNTS.format(method), toprint = "_")


	def stringConstants(self):
		return self.__query(STRING_CONSTANTS)

