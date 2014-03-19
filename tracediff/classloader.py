from stats import Refinement

class ClassLoaderRefinement(Refinement):
    def __init__(self, conn):
        Refinement.__init__(self)

    def prune_edge(self, (s,t)):
		# loadClass is invoked by the VM when a class needs to be loaded and
		# checkPackageAccess is invoked after loading the class
		return t in ('java.lang.ClassLoader: loadClass(java.lang.String)',
                     'java.lang.ClassLoader: checkPackageAccess(java.lang.Class,java.security.ProtectionDomain)')

    def report(self):
        pass
