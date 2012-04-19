import sys
import os
import directoryIndex

def buildSelectionDiv(pyFile):
    result = "<div class = \"pathObj\">\n"
    stack = []
    parent = pyFile.parent
    while parent != None:
        stack.append(parent)
        parent = parent.parent
    parent = pyFile.parent
    for p in stack[::-1]:
        result += buildPathDiv(p)
    result += buildListingDiv(pyFile)
    result += "</div>\n"
    return result

def buildPathDiv(path):
    result = "<div class = \"path\">\n"

    result += "<div class = \"directory dirselected\">"+ path.name.split("/")[-1] + "/"+"</div>\n"
    if path.parent != None:
        for p in path.parent.dirs:
            if p is path:
                pass
            else:
                result += "<div class = \"directory\">"+ p.name.split("/")[-1] + "/"+"</div>\n"
    result += "</div>\n"
    return result

def buildListingDiv(pyFile):
    path = pyFile.parent
    result = "<div class = \"path\">\n"
    for direc in path.dirs:
        result += "<div class = \"directory\">"+ direc.name.split("/")[-1] +"/"+"</div>\n"
    for fi in path.pyFiles:
        if fi is pyFile:
            result += "<div class = \"file selected\">"+fi.filename.split("/")[-1]+"</div>\n"
        else:
            result += "<div class = \"file\">"+fi.filename.split("/")[-1]+"</div>\n"
    result += "</div>\n"
    return result

if __name__ == "__main__":
    root =  sys.argv[1]
    pyFilename = os.path.abspath(sys.argv[2])
    rootDir = directoryIndex.Directory(root)
    index = rootDir.getSearchable()
    pyFile = index[pyFilename]
    print buildSelectionDiv(pyFile)
