import gatherinfo
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import sys
import os
import selectHTML


def buildHeader():
    return file("templates/header.html","r").read()

def buildFooter():
    return file("templates/footer.html","r").read()

def buildSelectedBanner(pyFile):
    return "<br/><div id=\"name\"><strong>Name:</strong> %s</div><br/>\n" % pyFile.filename.split("/")[-1]

def buildLoopSelector(pyFile, selected):
    result = "<div id=\"loops\">\n"
    result += "Loops: "
    for i, loop in enumerate(pyFile.loops):
        if i == selected:
            result += "<div class=\"loop selected\">%d</div>\n" % (i+1)
        else:
            result += "<div class=\"loop\">%d</div>\n" % (i+1)
    result += "</div><br/>\n"
    return result

def buildTable(pyFile,loop):
    result = "        <table id=\"main\">\n"
    result += "            <tr>\n"
    result += "                <th>Python</th><th>IR CODE</th>\n"
    result += "            </tr>\n"
    for source in pyFile.loops[loop]:
        if source[1].strip() != "":
            result +=  "            <tr>\n"
            if source[2] != None:
                result +=  "                <td class=\"python\">\n"
                result += highlight(source[1], PythonLexer(), HtmlFormatter())
                result += "                </td><td class=\"ircode\">\n"
            else:
                result +=  "                <td class=\"python grey\">\n"
                result += "<pre>" + source[1] + "</pre>\n"
                result += "                </td><td class=\"ircode grey\">\n"
            if source[2] != None:
                #print source[2]
                for chunk in source[2]:
                    result += "<a href=\"#\">" + chunk[0] + "</a>" + "<br/>\n"
            else:
                result += "NOT JITTED\n"
            result += "                </td>\n"
            result += "            </tr>\n"
    result += "        </table>\n"
    return result

def buildExpansion(pyFile,loop,line, chunk):
    result = "<table id=\"expand\">\n"

    chunk_repr,chunk,selected_ops = pyFile.loops[loop][line][2][chunk]
    result += "<tr><th colspan=\"2\">%s</th></tr>\n" % chunk_repr
    for op,asm in selected_ops:
        result += "<tr><td class=\"plus\">+</td><td>%s</td></tr>\n" % op
        if asm != None:
            result += "<tr style=\"display : None;\"><td class=\"empty\"></td><td><pre>%s</pre></td></tr>\n" % (asm)
    result += "</table>\n"
    return result

def buildPage(pyFile,selected=0):
    result = buildHeader()
    result += selectHTML.buildSelectionDiv(pyFile)
    result += buildSelectedBanner(pyFile)
    result += buildLoopSelector(pyFile, selected)
    result += buildTable(pyFile,selected)
    result += buildFooter()
    return result



if __name__ == "__main__":
    logfile, rootFolder, selected,output = sys.argv[1:5]
    listing = gatherinfo.PopulatedListing(logfile,rootFolder)
    pyFile = listing.index[os.path.abspath(selected)]
    fout = file(output, "w")
    fout.write(buildPage(pyFile))
    fout.close()
