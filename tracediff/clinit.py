from stats import Refinement

class ClassInitRefinement(Refinement):
    def __init__(self, conn):
        Refinement.__init__(self)
        self.initialized = conn.initialized_classes()

    def prune_edge(self, (s,t)):
        rec, meth = t.split(": ")
        simplename, delim, args = meth.partition('(')
        return simplename == '<clinit>' and rec in self.initialized

    def report(self):
        pass
