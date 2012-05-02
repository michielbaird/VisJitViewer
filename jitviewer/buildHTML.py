import gatherinfo
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import flask
import sys
import os
import selectHTML
import base64
import random


def buildHeader():
    return file("/home/mbaird/git/VisJitViewer/jitviewer/templates/header.html","r").read()

def buildFooter():
    return file("/home/mbaird/git/VisJitViewer/jitviewer/templates/footer.html","r").read()

def buildSelectedBanner(pyFile):
    return "<br/><div id=\"name\"><strong>File:</strong> %s</div><br/>\n" % pyFile.filename.split("/")[-1]

def loopWeight(weight):
    return "<div class=\"weight\" style=\"display: none;\">%.2f</div>" % (weight)

def buildLoopSelector(pyFile, selected):
    result = "<div id=\"loops\">\n"
    result += "Loops: "
    for i, loop in enumerate(pyFile.loops):
        if i == selected:
            result += "<div class=\"loop selected\" id=\"%d\" onClick=\"loop(%d)\">%d%s</div>\n" % (i,i,i+1,loopWeight(random.random()))
        else:
            result += "<div class=\"loop\" id=\"%d\" onClick=\"loop(%d)\">%d%s</div>\n" % (i,i,i+1,loopWeight(random.random()))

    result += "</div><br/>\n"
    return result

def buildHeatMap(pyFile,loop):
    result = "<div class=\"heatmap\">\n"
    length = 0
    if loop < len(pyFile.loops):
        for i,source in enumerate(pyFile.loops[loop]):
            if source[1].strip() != "":
                length += 1
        weight = (100/float(length))
    if loop < len(pyFile.loops):
        for i,source in enumerate(pyFile.loops[loop]):
            if source[1].strip() != "":
                if source[2] != None:
                    result += heatDot(i,random.randint(1,255), weight)
                else:
                    result += heatDot(i, -1, weight)
    else:
        result += heatDot(0,-1, 100.0)
    result += "</div><br/>\n"

    return result


def heatDot(id, span, weight):
    if span != -1:
        return "<div onClick=\"gotoLine(%d)\" class=\"heatdot\" style=\"background: #FF%02x%02x; width: %.16f%%;\"></div>\n" % (id,span, span, weight)
    else:
        return "<div onClick=\"gotoLine(%d)\" class=\"heatdot\" style=\"background: #999999; width: %.16f%%;\"></div>\n" % (id,weight)


def buildInnerTable(pyFile,loop):
    result = "            <tr>\n"
    result += "                <th class=\"first\">Python</th><th>IR CODE</th>\n"
    result += "            </tr>\n"
    fileName = pyFile.filename
    if len(pyFile.loops) > loop:
        for i,source in enumerate(pyFile.loops[loop]):
            if source[1].strip() != "":
                result +=  "            <tr id=\"source%d\">\n" % (i)
                if source[2] != None:
                    result +=  "                <td class=\"python\">\n"
                    result += highlight(source[1], PythonLexer(), HtmlFormatter())
                    result += "                </td><td class=\"ircode\">\n"
                    for j,chunk in enumerate(source[2]):
                        result += ("<a  onClick=\"expansion(%d,%d,%d)\">" % (loop,i,j)) + chunk[0] + "</a>" + "<br/>\n"
                    result += "</td></tr><tr><td class=\"expandin\" id=\"line%d\" colspan=\"2\" style=\"display:None;\">" % i
                else:
                    result +=  "                <td class=\"python grey\">\n"
                    result += "<pre class=\"full\">" + source[1] + "</pre>\n"
                    result += "<pre class=\"brief\">" + source[1].split("\n")[0] + " ..."+ "</pre>"
                    result += "                </td><td class=\"ircode grey\">\n"
                    result += "NOT JITTED\n"
                result += "                </td>\n"
                result += "            </tr>\n"
    else:
        result +=  "                <td class=\"python grey\">\n"
        result += "<pre class=\"full\">" + file(fileName).read() + "</pre>\n"
        result += "<pre class=\"brief\">" + file(fileName).read().split("\n")[0] +" ..." + "</pre>\n"
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
            result += "<tr><td class=\"plus\" id=\"%s\" onClick=\"viewAsm(\'%s\',\'%s\')\">+</td><td class=\"rpy\">%s</td></tr>\n" % (asmID2,asmID,asmID2,op)
            result += "<tr class=\"asm\" id=\"%s\" style=\"display : None;\"><td class=\"empty\"></td><td class=\"lolsm\"><pre>%s</pre></td></tr>\n" % (asmID,asm)
        else:
            result += "<tr><td class=\"noasm\"></td><td class=\"rpy\">%s</td></tr>\n" % op
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
    result += "<div id=\"heatContainer\">\n"
    result += buildHeatMap(pyFile,selected)
    result += "</div>\n"
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
