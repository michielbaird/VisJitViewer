import sys
import os
import directoryIndex
import base64

def buildSelectionDiv(pyFile):
    result = "<div class = \"pathObj\">\n"
    stack = []
    if isinstance(pyFile,directoryIndex.PyFile):
        parent = pyFile.parent
    else:
        parent = pyFile
    while parent != None:
        stack.append(parent)
        parent = parent.parent
    if isinstance(pyFile,directoryIndex.PyFile):
        parent = pyFile.parent
    else:
        parent = pyFile
    for p in stack[::-1]:
        result += buildPathDiv(p)
    result += buildListingDiv(pyFile)
    result += "</div>\n"
    return result

def buildPathDiv(path):
    result = "<div class = \"path\">\n"

    result += ("<div class = \"directory dirselected\" onClick=\"selectDirectory('%s')\">" % base64.b64encode(path.name)) + \
            path.name.split("/")[-1] + "/"+"</div>\n"
    if path.parent != None:
        for p in path.parent.dirs:
            if p is path:
                pass
            else:
                result += ("<div class = \"directory\" onClick=\"selectDirectory('%s')\">" % base64.b64encode(p.name)) + \
                     p.name.split("/")[-1] + "/"+"</div>\n"
    result += "</div>\n"
    return result

def buildListingDiv(pyFile):
    if isinstance(pyFile,directoryIndex.PyFile):
        path = pyFile.parent
    else:
        path = pyFile
    result = "<div class = \"path\">\n"
    for direc in path.dirs:
        result += ("<div class = \"directory\" onClick=\"selectDirectory('%s')\">" % base64.b64encode(direc.name)) + \
                direc.name.split("/")[-1] +"/"+"</div>\n"
    for fi in path.pyFiles:
        if fi is pyFile:
            result += "<div class = \"file selected\">"+fi.filename.split("/")[-1]+"</div>\n"
        else:
            result += ("<div class = \"file\" onClick=\"selectFile('%s')\">" % base64.b64encode(fi.filename)) + \
                fi.filename.split("/")[-1]+"</div>\n"
    result += "</div>\n"
    return result

if __name__ == "__main__":
    root =  sys.argv[1]
    pyFilename = os.path.abspath(sys.argv[2])
    rootDir = directoryIndex.Directory(root)
    index = rootDir.getSearchable()
    pyFile = index[pyFilename]
    print buildSelectionDiv(pyFile)
