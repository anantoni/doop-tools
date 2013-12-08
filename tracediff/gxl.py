import os, subprocess

class Probe:
    _JARDIR  = os.path.dirname(__file__)
    _JARPATH = os.path.join(_JARDIR, 'gxlutil.jar')

    def __init__(self, trace):
        self._trace = trace

    def calledges(self):
        results = []
        command = "java -jar {0} {1}".format(self._JARPATH, self._trace)

        p = subprocess.Popen(
            command, shell = True, 
            stdout = subprocess.PIPE, 
            stderr = subprocess.STDOUT)

        for line in p.stdout.readlines()[1:]:
            results.append(tuple(line.strip().split(" ===> ")))

        p.wait()
        return results

    @staticmethod
    def transform(signature):
        rec, meth = signature.split(": ")
        simplename, delim, args = meth.partition('(')
        trans = [rec, ': ', simplename, '(']
        dim = 0
        ref = False
        
        assert args[-1] == ')'

        for i in args[:-1]:
            if ref:
                if i == ';':   ref = False
                elif i == '/': trans.append('.')
                else:          trans.append(i)
                if i != ';': continue
            else:
                if   i == 'L': ref = True
                elif i == '[': dim += 1
                elif i == 'I': trans.append("int")
                elif i == 'S': trans.append("short")
                elif i == 'J': trans.append("long")
                elif i == 'F': trans.append("float")
                elif i == 'D': trans.append("double")
                elif i == 'Z': trans.append("boolean")
                elif i == 'B': trans.append("byte")
                elif i == 'C': trans.append("char")
                else:
                    raise ValueError(i, signature, "".join(trans))
                if i == '[' or i == 'L':
                    continue
            for i in range(dim):
                trans.append('[]')
                dim = 0
            trans.append(',')
        if trans[-1] == ',':
            trans[-1] = ')'
        else:
            assert trans[-1] == '('
            trans.append(')')
        return "".join(trans)
