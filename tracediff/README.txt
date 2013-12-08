For usage, run:
$ ./tracediff.py -h

This tool will try to compare the dynamic callgraph (trace argument)
with the static callgraph as produced by Doop (workspace argument).

The two arguments should be compatible with each other, i.e.,
they should have been produced by analyzing the same program, 
otherwise the results will not have any meaningful value.

The -cp option, if provided,  should include every class of the 
aforementioned program. This will try to prune out the ``noise'' due
to synthetic classes.

The program output will be statistics on missing edges, i.e., edges
present in the dynamic and not in the static callgraph.

The statistics will be printed in series corresponding to consecutive
transformations that try to prune out some missing edges, such as
those involving synthetic classes, methods reachable via reflection 
only, and so on. This process tries to minimize the missing edges set,
so that it becomes easier to investigate the recall problem.
