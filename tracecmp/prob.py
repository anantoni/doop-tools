import subprocess

class Probe:
    def __init__(self, jar):
        self._jar = jar

    def __run__(self, opt, gxl, entrypoints):
        results = []
        command = "java -jar {0} {1} -{2}".format(self._jar, gxl, opt)
        
        if entrypoints:
            command.append("-e")

        # print command

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in p.stdout.readlines()[1:]:
            results.append(tuple(map(Probe.transform, line.strip().split(" ===> "))))

        p.wait()
        return results

    def a2a(self, gxl, entrypoints=False):
        return self.__run__("a2a", gxl, entrypoints)
    
    def a2l(self, gxl, entrypoints=False):
        return self.__run__("a2l", gxl, entrypoints)

    def l2a(self, gxl, entrypoints=False):
        return self.__run__("l2a", gxl, entrypoints)

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
