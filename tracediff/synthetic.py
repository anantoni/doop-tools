import java, stats

class Refinement(stats.Refinement):
    def __init__(self, classpath):
        stats.Refinement.__init__(self)
        self.env = java.Env(classpath)
        self.pruned = set()

    def prune_class(self, klass):
        if not klass in self.env:
            self.pruned.add(klass)
            return True
        return False

    def report(self):
        for klass in self.pruned:
            print "Synthetic:", klass
