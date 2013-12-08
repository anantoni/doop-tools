from stats import Refinement

class NoFactsRefinement(Refinement):
    def __init__(self, conn):
        Refinement.__init__(self)
        self.methods = conn.methods()
        self.classes = conn.classes()
        self.pruned_methods = set()
        self.pruned_classes = set()

    def prune_class(self, klass):
        if not klass in self.classes:
            self.pruned_classes.add(klass)
            return True
        return False

    def prune_method(self, meth):
        # Firstly, check for missing class
        if Refinement.prune_method(self, meth):
            return True
        # Then, check for missing method
        if not meth in self.methods:
            self.pruned_methods.add(meth)
            return True
        return False

    def report(self):
        for klass in self.pruned_classes:
            print "Unknown <class>:  ", klass
        for meth in self.pruned_methods:
            print "Unknown <method>:     ", meth
