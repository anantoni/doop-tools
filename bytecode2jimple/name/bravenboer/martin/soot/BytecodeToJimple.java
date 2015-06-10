package name.bravenboer.martin.soot;

import java.io.File;
import java.io.FileInputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.HashSet;
import java.util.HashMap;
import java.util.Set;

import soot.ClassProvider;
import soot.EntryPoints;
import soot.PhaseOptions;
import soot.Printer;
import soot.Scene;
import soot.SootClass;
import soot.SootMethod;
import soot.SootResolver;
import soot.MethodOrMethodContext;


public class BytecodeToJimple {

    public static enum Mode {
        INPUTS, CALLGRAPH, FULL;
    }

    private static Mode _mode = null;
    private static List<String> _inputs = new ArrayList<String>();
    private static List<String> _libraries = new ArrayList<String>();
    private static String _outputFile = null;
    private static String _outputDir = null;

    private static int shift(String[] args, int index) {
        if(args.length == index + 1) {
            System.err.println("error: option " + args[index] + " requires an argument");
            System.exit(1);
        }

        return index + 1;
    }

    public static void main(String[] args) {
        try {
            if(args.length == 0) {
                System.err.println("usage: bytecode2jimple [options] file...");
                System.exit(0);
            }

            for(int i = 0; i < args.length; i++) {
                if(args[i].equals("--full") || args[i].equals("-full")) {
                    if(_mode != null) {
                        System.err.println("error: duplicate mode argument");
                        System.exit(1);
                    }

                    _mode = Mode.FULL;
                }
                else if(args[i].equals("--cg") || args[i].equals("-cg")) {
                    if(_mode != null) {
                        System.err.println("error: duplicate mode argument");
                        System.exit(1);
                    }

                    _mode = Mode.CALLGRAPH;
                }
                else if(args[i].equals("-o")) {
                    i = shift(args, i);
                    _outputFile = args[i];
                }
                else if(args[i].equals("-d")) {
                    i = shift(args, i);
                    _outputDir = args[i];
                }
                else if(args[i].equals("-l")) {
                    i = shift(args, i);
                    _libraries.add(args[i]);
                }
                else if(args[i].equals("-lsystem") || args[i].equals("--lsystem")) {
                    String javaHome = System.getProperty("java.home");
                    _libraries.add(javaHome + File.separator + "lib" + File.separator + "rt.jar");
                    _libraries.add(javaHome + File.separator + "lib" + File.separator + "jce.jar");
                }
                else if(args[i].equals("-h") || args[i].equals("--help") || args[i].equals("-help")) {
                    System.err.println("usage: bytecode2jimple [options] file...");
                    System.err.println("options:");
                    System.err.println("  -full           Generate Jimple files by full transitive resolution");
                    System.err.println("  -o <file>       Write Jimple to file (only if not -full).");
                    System.err.println("  -d <directory>  Specify where to generate jimple files.");
                    System.err.println("  -l <archive>    Find classes in jar/zip archive.");
                    System.err.println("  -lsystem        Find classes in default system classes.");
                    System.err.println("  -h, -help,      Print this help message.");
                    System.exit(0);
                }
                else {
                    if(args[i].charAt(0) == '-') {
                        System.err.println("error: unrecognized option: " + args[i]);
                        System.exit(0);
                    }
                    else {
                        _inputs.add(args[i]);
                    }
                }
            }

            if(_mode == null) {
                _mode = Mode.INPUTS;
            }

            run();
        }
        catch(Exception exc) {
            exc.printStackTrace();
        }
    }

    private static void run() throws Exception {
        NoSearchingClassProvider provider = new NoSearchingClassProvider();

        for(String arg : _inputs) {
            if(arg.endsWith(".jar") || arg.endsWith(".zip")) {
                provider.addArchive(new File(arg));
            }
            else {
                provider.addClass(new File(arg));
            }
        }

        for(String lib: _libraries) {
            provider.addArchiveForResolving(new File(lib));
        }

        soot.SourceLocator.v().setClassProviders(Collections.singletonList((ClassProvider) provider));

        if(_mode == Mode.FULL || _mode == Mode.CALLGRAPH) {
            soot.options.Options.v().set_full_resolver(true);
        }
        soot.options.Options.v().setPhaseOption("jb", "use-original-names:true");

        Scene scene = Scene.v();
        Collection<SootClass> classes = new ArrayList<SootClass>();
        for(String className : provider.getClassNames()) {
            scene.loadClass(className, SootClass.SIGNATURES);
            SootClass c = scene.loadClass(className, SootClass.BODIES);
            c.setApplicationClass();
            classes.add(c);
        }

        scene.loadNecessaryClasses();
        if(_mode == Mode.CALLGRAPH) {
            HashMap<String, String> opt = new HashMap<String, String>();
            opt.put("verbose","true");
            opt.put("propagator","worklist");
            opt.put("simple-edges-bidirectional","false");
            opt.put("rta","enabled");
            opt.put("set-impl","double");
            opt.put("double-set-old","hybrid");
            opt.put("double-set-new","hybrid");



            soot.jimple.spark.SparkTransformer.v().transform("", opt);
            soot.jimple.toolkits.callgraph.CallGraphBuilder builder =
                new soot.jimple.toolkits.callgraph.CallGraphBuilder(scene.getPointsToAnalysis());
            builder.build();
            scene.getReachableMethods().update();

            Set<SootClass> set = new HashSet<SootClass>();
            Iterator<? extends MethodOrMethodContext> iterator = scene.getReachableMethods().listener();
            while(iterator.hasNext()) {
                SootMethod method = (SootMethod) iterator.next();
                System.err.println("class: " + method.getDeclaringClass());
                set.add(method.getDeclaringClass());
            }
            classes = set;
        }

        if(_mode == Mode.FULL) {
            classes = scene.getClasses();
        }

        write(classes);
    }

    /**
     * Write the output.
     */
    private static void write(Collection<SootClass> classes) throws Exception {
        for(SootClass c : classes) {
            Iterator<SootMethod> methodIt = c.methodIterator();
            while (methodIt.hasNext()) {
                SootMethod m = methodIt.next();
                if( m.isConcrete() ) {
                    m.retrieveActiveBody();
                }
            }
        }

        PrintWriter writer = null;
        if(_outputFile != null) {
            if(classes.size() == 1) {
                writer = new PrintWriter(new File(_outputFile));
            }
            else {
                System.err.println("error: cannot output multiple Jimple files to one -o file");
                System.exit(1);
            }
        }
        else {
            if(classes.size() == 1 && _outputDir == null) {
                writer = new PrintWriter(System.out);
            }
        }

        if(writer != null && classes.size() == 1) {
            for(SootClass c : classes) {
                write(writer, c);
            }
        }
        else if(_outputDir != null) {
            for(SootClass c : classes) {
                File f = new File(_outputDir, c.getName() + ".jimple");
                write(new PrintWriter(f), c);
            }
        }
        else {
            System.err.println("error: multiple Jimple files to generate, please specify an output directory.");
            System.exit(1);
        }
    }

    /**
     * Write util.
     */
    private static void write(PrintWriter writer, SootClass c) {
        Printer.v().printTo(c, writer);
        writer.flush();
        writer.close();

        if(writer.checkError()) {
            throw new RuntimeException("uknown error during writing to PrintWriter");
        }
    }
}
