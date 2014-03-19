import stats

class Refinement(stats.Refinement):
    def __init__(self, conn):
        stats.Refinement.__init__(self)
        self.reachable = conn.methods(reachable = True)

    def prune_edge(self, (s,t)):
        return not s in self.reachable

    def report(self):
        pass
