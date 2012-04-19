from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import logParser
import sys

logFile = sys.argv[1]
mySources = logParser.getMySources(logFile)
#print mySources
mySource = mySources[2]

print "<!doctype HTML>"
print "<html>"
print "    <head>"
print "        <title>PyPy Jit Viewer</title>"
print "        <link rel=\"stylesheet\" type=\"text/css\" href=\"design1.css\" />"
print "        <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />"
print "    </head>"
print "    <body>"
print "        <table id=\"main\">"
print "            <tr>"
print "                <th>Python</th><th>IR CODE</th>"
print "            </tr>"
for source in mySource:
    if source[1].strip() != "":
        print "            <tr>"
        print "                <td class=\"python\">"
        if source[2] != None:
            print highlight(source[1], PythonLexer(), HtmlFormatter())
        else:
            print "<pre>" + source[1] + "</pre>"
        print "                </td><td class=\"ircode\">"
        if source[2] != None:
            #print source[2]
            for chunk in source[2]:
                print "<a href=\"#\">" + chunk[0] + "</a>" + "<br/>"
        else:
            print "NOT JITTED"
        print "                </td>"
        print "            </tr>"
        print "            <tr><td colspan=\"2\">LOLOLOL</td></tr>"
print "        </table>"
print "    </body>"
print "</html>"
