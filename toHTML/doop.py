import blox
from queries import *

class Connector:
	def __init__(self, workspace):
		self._conn = blox.Connector(workspace)

	def __query(self, queryString, **kwargs):
		return self._conn.query(queryString, **kwargs)


	def modifiers(self, method):
		return self.__query(MODIFIERS.format(method))

	def formals(self, method):
		return self.__query(FORMALS.format(method))

	def locals(self):
		return self.__query(LOCALS, toprint = "_")

	def allocations(self):
		return self.__query(ALLOCATIONS)

	def assigns(self):
		return self.__query(ASSIGNS)

	def casts(self):
		return self.__query(CASTS)

	def fldModifiers(self, method):
		return self.__query(FLD_MODIFIERS.format(method))

	def loadInstanceFields(self):
		return self.__query(LOAD_INSTANCE_FIELDS)

	def loadStaticFields(self):
		return self.__query(LOAD_STATIC_FIELDS)

	def storeInstanceFields(self):
		return self.__query(STORE_INSTANCE_FIELDS)

	def storeStaticFields(self):
		return self.__query(STORE_STATIC_FIELDS)

	def loadArrays(self, method):
		return self.__query(LOAD_ARRAYS.format(method))

	def storeArrays(self, method):
		return self.__query(STORE_ARRAYS.format(method))


	def specialInv(self, method):
		return self.__query(SPECIAL_INV.format(method), toprint = "_")

	def virtualInv(self, method):
		return self.__query(VIRTUAL_INV.format(method), toprint = "_")

	def staticInv(self, method):
		return self.__query(STATIC_INV.format(method), toprint = "_")

	def staticInvNoVars(self, method):
		return self.__query(STATIC_INV_NO_VARS.format(method), toprint = "_")

	def returns(self, method):
		return self.__query(RETURNS.format(method))


	def varPointsTo(self, method):
		return self.__query(VAR_POINTS_TO.format(method), toprint = "_")

	def varPointsToCounts(self, method):
		return self.__query(VAR_POINTS_TO_COUNTS.format(method), toprint = "_")


	def fldPointsTo(self, method):
		return self.__query(FLD_POINTS_TO.format(method), toprint = "_")

	def fldPointsToCounts(self, method):
		return self.__query(FLD_POINTS_TO_COUNTS.format(method), toprint = "_")


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

