from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import sys

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
sourceFile = sys.argv[1]
sourcelines = open(sourceFile,"r").readlines()
for source in sourcelines	:
    if source.strip() != "":
        print "            <tr>"
        print "                <td class=\"python\">"
        print highlight(source, PythonLexer(), HtmlFormatter())
        print "                </td><td class=\"ircode\">NOT JITTED</td>"
        print "            </tr>"
print "        </table>"
print "    </body>"
print "</html>"
