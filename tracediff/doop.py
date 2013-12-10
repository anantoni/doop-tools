import blox
from queries import *

class Connector:
    def __init__(self, workspace):
        self._conn = blox.Connector(workspace)

    def __query(self, queryString, **kwargs):
        return self._conn.query(queryString, **kwargs)

    @classmethod
    def canonicalize(cls,signature):
        """
        Canonicalizes a signature by removing its return type
        """
        rec, meth = signature.split(": ")
        simplename, delim, args = meth.partition('(')
        return rec + ': ' + simplename.rpartition(' ')[2] + '(' + args

    @classmethod
    def __parse_edge(cls, line):
        return tuple(cls.canonicalize(x) for x in line[1:-1].split(">, <"))

    @classmethod
    def __parse_method(cls, line):
        return cls.canonicalize(line[1:-1])

    def classes(self):
        return self.__query(CLASSES)

    def initialized_classes(self):
        return self.__query(INITIALIZED_CLASSES)

    def calledges(self):
        return map(self.__parse_edge, self.__query(CALL_EDGES))

    def calledges(self, _from, _to):
        for x in (_from, _to):
            if x not in ('app', 'lib'):
                raise ValueError()
        if _from == 'app':
            q = APP_TO_APP if _to == 'app' else APP_TO_LIB
        else:
            q = LIB_TO_APP if _to == 'app' else LIB_TO_LIB
        return map(self.__parse_edge, self.__query(q))

    def methods(self, app_only = False, reachable = False):
        if not reachable:
            q = APP_METHODS if app_only else METHODS
        else:
            q = REACHABLE_APP_METHODS if app_only else REACHABLE_METHODS
        return set(map(self.__parse_method, self.__query(q)))

    def nulls(self):
        return map(self.__parse_edge, self.__query(NULLS, toprint = "_n"))
