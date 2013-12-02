import java.util.*;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.IOException;
import java.io.PrintWriter;

import probe.CallEdge;
import probe.CallGraph;
import probe.GXLReader;
import probe.ProbeClass;
import probe.ProbeMethod;

public class GxlPrinter
{
    private final PrintWriter writer;
    private final ProbeElementTextifier textifier;

    public GxlPrinter(PrintWriter writer)
    {
        this.writer = writer;
        this.textifier = new ProbeElementTextifier();
    }

    public void print(CallGraph callgraph)
    {
        for (Iterator it = callgraph.edges().iterator(); it.hasNext();)
        {
            CallEdge edge = (CallEdge) it.next();

            ProbeMethod source = edge.src();
            ProbeMethod dest = edge.dst();

            writer.println(
                textifier.textifyMethod(source) + 
                " ===> " + 
                textifier.textifyMethod(dest));

            writer.flush();
        }
    }

    public static void main(String[] args) throws IOException
    {
        String fileName = args[0];
        GxlPrinter printer = new GxlPrinter(new PrintWriter(System.out));

        try (InputStream stream = new FileInputStream(fileName))
        {
            CallGraph callgraph = new GXLReader().readCallGraph(stream);
            
            printer.print(callgraph);
        }        
    }
}
