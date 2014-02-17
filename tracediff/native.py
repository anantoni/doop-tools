import stats

class Refinement(stats.Refinement):
    def __init__(self, conn):
        stats.Refinement.__init__(self)
        self.native = conn.native_methods()
        self.pruned_methods = set()

    def prune_method(self, meth):
        # Then, check for missing method
        if meth in self.native:
            self.pruned_methods.add(meth)
            return True
        return False

    def report(self):
        for meth in self.pruned_methods:
            print "Native <method>:     ", meth
