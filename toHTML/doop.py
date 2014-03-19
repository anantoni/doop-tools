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

	def locals(self, method):
		return self.__query(LOCALS.format(method), toprint = "_")

	def allocations(self, method):
		return self.__query(ALLOCATIONS.format(method))

	def assigns(self, method):
		return self.__query(ASSIGNS.format(method))

	def casts(self, method):
		return self.__query(CASTS.format(method))

	def fldModifiers(self, method):
		return self.__query(FLD_MODIFIERS.format(method))

	def loadInstanceFields(self, method):
		return self.__query(LOAD_INSTANCE_FIELDS.format(method))

	def loadStaticFields(self, method):
		return self.__query(LOAD_STATIC_FIELDS.format(method))

	def storeInstanceFields(self, method):
		return self.__query(STORE_INSTANCE_FIELDS.format(method))

	def storeStaticFields(self, method):
		return self.__query(STORE_STATIC_FIELDS.format(method))

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

