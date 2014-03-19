import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.HashSet;

import probe.CallEdge;
import probe.CallGraph;
import probe.GXLWriter;
import probe.ObjectManager;
import probe.ProbeMethod;

/**
 * A filter converting method traces into a GXL representation of the dynamic call graph.
 */
public class Trace2GXL {
    
    public static void main(String[] args) throws Exception {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String line = "";
        
        try {
            while ((line = in.readLine()) != null) {
                String[] fields = line.split("\\t");
                if (!"CALL".equals(fields[0]))
                    throw new IllegalArgumentException("Expected line prefixed by \"CALL\"");
                ProbeMethod calledMethod = getProbeMethod(fields[1], fields[2], fields[3]);
                if ("ROOT".equals(fields[4])) {
                    entryPoints.add(calledMethod);
                } else {
                    ProbeMethod callingMethod = getProbeMethod(fields[4], fields[5], fields[6]);
                    callEdges.add(new CallEdge(callingMethod, calledMethod));
                }
            }
        } catch (Exception e) {
            throw new Exception(line, e);
        }
        
        CallGraph callGraph = new CallGraph();
        callGraph.entryPoints().addAll(entryPoints);
        callGraph.edges().addAll(callEdges);
        
        new GXLWriter().write(callGraph, System.out);
    }
    
    /**
     * @return A sanity-checked probe method. We make sure that there are no clashes
     * with co-variant return types in method signatures.
     */
    private static ProbeMethod getProbeMethod(String classSignature, String methodName, String methodSignature) throws Exception {
        ProbeMethod probeMethod = getBuggyProbeMethod(classSignature, methodName, methodSignature);
        String uniqueMethodSignature;
        if ((uniqueMethodSignature = uniqueMethodSignatures.get(probeMethod)) == null)
           uniqueMethodSignatures.put(probeMethod, methodSignature);
        else if (!methodSignature.equals(uniqueMethodSignature))
           System.err.println(probeMethod.toString() + "\t" + methodSignature + "\t" + uniqueMethodSignature);
        return probeMethod;
    }
    
    private static HashMap<ProbeMethod, String> uniqueMethodSignatures = new HashMap<ProbeMethod, String>();
    
    /**
     * Returns a method as currently required by ProBe, i.e., ignoring the
     * return type.
     * 
     * This is a bug in ProBe.
     */
    private static ProbeMethod getBuggyProbeMethod(String classSignature, String methodName, String methodSignature) throws Exception {
        return ObjectManager.v().getMethod(
                ObjectManager.v().getClass(toProbeClassName(classSignature)),
                methodName,
                toProbeMethodSignature(methodSignature));
    }
    
    private static String toProbeClassName(String classSignature) throws Exception {
        if (!classSignature.startsWith("L"))
            throw new IllegalArgumentException("Expected class type, got " + classSignature);
        return classSignature.substring(1, classSignature.length() - 1).replace('/', '.');
    }
    
    private static String toProbeMethodSignature(String methodSignature) throws Exception {
        return methodSignature.substring(methodSignature.indexOf("(") + 1, methodSignature.indexOf(")"));
    }
    
    private static HashSet<ProbeMethod> entryPoints = new HashSet<ProbeMethod>();
    
    private static HashSet<CallEdge> callEdges = new HashSet<CallEdge>();
}

