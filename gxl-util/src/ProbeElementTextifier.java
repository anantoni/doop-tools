import probe.ProbeClass;
import probe.ProbeMethod;

public class ProbeElementTextifier
{
    public String textifyClass(ProbeClass klass)
    {
        return "" + klass;
    }
    
    public String textifyMethod(ProbeMethod method)
    {
        String cls  = textifyClass(method.cls());
        String name = method.name();
        String sign = textifySignature(method.signature());

        return String.format("%s: %s(%s)", cls, name, sign);
    }

    public String textifySignature(String signature)
    {
        // Zero-argument signature
        if (signature.isEmpty())
            return "";

        char[] s = signature.toCharArray();

        StringBuilder builder = new StringBuilder();

        for(int i = 0; i < s.length; i++)
        {
            int nDim = 0;

            // Skip array brackets
            for (; s[i] == '['; i++)
                nDim++;

            // Reference type
            if (s[i] == 'L') {
                int start = ++i;

                while (s[i] != ';')
                    i++;

                builder.append(s, start, i - start);
            }
            // Primitive type
            else if (s[i] == 'I') { builder.append("int");     }
            else if (s[i] == 'S') { builder.append("short");   }
            else if (s[i] == 'J') { builder.append("long");    }
            else if (s[i] == 'F') { builder.append("float");   }
            else if (s[i] == 'D') { builder.append("double");  }
            else if (s[i] == 'Z') { builder.append("boolean"); }
            else if (s[i] == 'B') { builder.append("byte");    }
            else if (s[i] == 'C') { builder.append("char");    }
            else { throw new IllegalArgumentException();       }

            // Append brackets for arrays
            for (int j = 0; j < nDim; j++)
                builder.append("[]");
            
            builder.append(',');
        }

        // Erase trailing comma
        builder.setLength(builder.length() - 1);

        return builder.toString().replace('/', '.');
    }
}
