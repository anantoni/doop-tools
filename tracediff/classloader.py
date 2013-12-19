from stats import Refinement

class ClassLoaderRefinement(Refinement):
    def __init__(self, conn):
        Refinement.__init__(self)

    def prune_edge(self, (s,t)):
        rec, _ = t.split(": ")
        return rec == 'java.lang.ClassLoader'

    def report(self):
        pass
