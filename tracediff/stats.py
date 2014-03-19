class Statistics:
    def __init__(self):
        self.a2a = []
        self.a2l = []
        self.l2a = []
        self.l2l = []

    @classmethod
    def from_doop(cls, conn):
        stats = cls()
        stats.a2a = conn.calledges(_from = 'app', _to = 'app')
        stats.a2l = conn.calledges(_from = 'app', _to = 'lib')
        stats.l2a = conn.calledges(_from = 'lib', _to = 'app')
        stats.l2l = conn.calledges(_from = 'lib', _to = 'lib')
        stats.nulls = conn.nulls()
        return stats

    @classmethod
    def fieldmapping(cls, app_callback):
        f = lambda n : 'a' if app_callback(n) else 'l'
        return lambda (s,t): '{0}2{1}'.format(f(s), f(t))

    @classmethod
    def from_trace(cls, probe, conn):
        cb = conn.methods(app_only = True).__contains__
        stats = cls()
        stats.edgesetof = cls.fieldmapping(cb)
        for e in probe.calledges():
            getattr(stats, stats.edgesetof(e)).append(e)
        return stats

    @classmethod
    def difference(cls, x, y):
        stats = cls()
        for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
            xs, ys = getattr(x, tp), getattr(y, tp)
            setattr(stats, tp, [e for e in xs if e not in ys])
        return stats


class Refinement:

    def __init__(self):
        pass

    def __call__(self, oldstats):
        newstats = Statistics()
        for tp in ('a2a', 'a2l', 'l2a', 'l2l'):
            missing = getattr(oldstats, tp)
            pruned  = getattr(newstats, tp)
            for e in missing:
                if not self.prune_edge(e):
                    pruned.append(e)
        return newstats

    def prune_edge(self, (s,t)):
        return self.prune_method(s) or self.prune_method(t)

    def prune_method(self, meth):
        return self.prune_class(meth.split(':')[0])

    def prune_class(self, klass):
        return False

    def report(self):
        raise NotImplementedError("Please Implement this method")
