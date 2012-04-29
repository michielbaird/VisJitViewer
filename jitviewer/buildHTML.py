import gatherinfo
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import flask
import sys
import os
import selectHTML
import base64


def buildHeader():
    return file("templates/header.html","r").read()

def buildFooter():
    return file("templates/footer.html","r").read()

def buildSelectedBanner(pyFile):
    return "<br/><div id=\"name\"><strong>File:</strong> %s</div><br/>\n" % pyFile.filename.split("/")[-1]

def buildLoopSelector(pyFile, selected):
    result = "<div id=\"loops\">\n"
    result += "Loops: "
    for i, loop in enumerate(pyFile.loops):
        if i == selected:
            result += "<div class=\"loop selected\" id=\"%d\" onClick=\"loop(%d)\">%d</div>\n" % (i,i,i+1)
        else:
            result += "<div class=\"loop\" id=\"%d\" onClick=\"loop(%d)\">%d</div>\n" % (i,i,i+1)
    result += "</div><br/>\n"
    return result

def buildInnerTable(pyFile,loop):
    result = "            <tr>\n"
    result += "                <th>Python</th><th>IR CODE</th>\n"
    result += "            </tr>\n"
    fileName = pyFile.filename
    if len(pyFile.loops) > loop:
        for i,source in enumerate(pyFile.loops[loop]):
            if source[1].strip() != "":
                result +=  "            <tr>\n"
                if source[2] != None:
                    result +=  "                <td class=\"python\">\n"
                    result += highlight(source[1], PythonLexer(), HtmlFormatter())
                    result += "                </td><td class=\"ircode\">\n"
                    for j,chunk in enumerate(source[2]):
                        result += ("<a  onClick=\"expansion(%d,%d,%d)\">" % (loop,i,j)) + chunk[0] + "</a>" + "<br/>\n"
                    result += "</td></tr><tr><td class=\"expandin\" id=\"line%d\" colspan=\"2\" style=\"display:None;\">" % i
                else:
                    result +=  "                <td class=\"python grey\">\n"
                    result += "<pre>" + source[1] + "</pre>\n"
                    result += "                </td><td class=\"ircode grey\">\n"
                    result += "NOT JITTED\n"
                result += "                </td>\n"
                result += "            </tr>\n"
    else:
        result +=  "                <td class=\"python grey\">\n"
        result += "<pre>" + file(fileName).read() + "</pre>\n"
        result += "                </td><td class=\"ircode grey\">\n"
        result += "NOT JITTED\n"
        result += "                </td>\n"
        result += "            </tr>\n"
    return result


def buildTable(pyFile,loop):
    result = "        <table id=\"main\">\n"
    result += buildInnerTable(pyFile,loop)
    result += "        </table>\n"
    return result

def buildExpansion(pyFile,loop,line, chunk):
    result = "<table id=\"expand\">\n"

    chunk_repr,r_chunk,selected_ops = pyFile.loops[loop][line][2][chunk]
    result += "<tr><th colspan=\"2\">%s</th></tr>\n" % chunk_repr
    for i,(op,asm) in enumerate(selected_ops):
        if asm != None:
            asmID = "%dA%dA%dA%s"  % (loop,line,chunk,i)
            asmID2 = "%dB%dB%dB%s"  % (loop,line,chunk,i)
            result += "<tr><td class=\"plus\" id=\"%s\" onClick=\"viewAsm(\'%s\',\'%s\')\">+</td><td>%s</td></tr>\n" % (asmID2,asmID,asmID2,op)
            result += "<tr class=\"asm\" id=\"%s\" style=\"display : None;\"><td class=\"empty\"></td><td><pre>%s</pre></td></tr>\n" % (asmID,asm)
        else:
            result += "<tr><td class=\"noasm\"></td><td>%s</td></tr>\n" % op
    result += "</table>\n"
    return result

def buildPage(pyFile,selected=0):
    result = buildHeader()
    result += "<div id=\"pathContainer\">\n"
    result += selectHTML.buildSelectionDiv(pyFile)
    result += "</div>\n"
    result += "<div id=\"bannerContainer\">\n"
    result += buildSelectedBanner(pyFile)
    result += "</div>\n"
    result += "<div id=\"fileContainer\">\n"
    result += buildLoopSelector(pyFile, selected)
    result += buildTable(pyFile,selected)
    result += "</div>\n"
    result += buildFooter()
    return result



if __name__ == "__main__":
    logfile, rootFolder, selected,output = sys.argv[1:5]
    listing = gatherinfo.PopulatedListing(logfile,rootFolder)
    pyFile = listing.index[os.path.abspath(selected)]
    fout = file(output, "w")
    fout.write(buildPage(pyFile))
    fout.close()
