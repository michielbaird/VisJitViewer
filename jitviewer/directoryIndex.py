import sys
import os

class Directory:
    def __init__(self, directory,parent=None):
        self.name = os.path.abspath(directory)
        self.parent = parent
        self.dirs = []
        self.pyFiles = []
        for child in os.listdir(self.name):
            path = os.path.join(self.name,child)
            if os.path.isdir(path) and child[0] != ".":
                self.dirs.append(Directory(path,self))
            elif child[0] != "." and child.split(".")[-1] == "py":
                self.pyFiles.append(PyFile(path,self))


    def hasDirs(self):
        return len(self.dirs) != 0

    def __str__(self):
        children = [ "\n".join(["->" + i for i in  str(x).split("\n")])  for x in self.dirs]
        header = self.name
        for pyfile in self.pyFiles:
            header += "\n" + str(pyfile)
        if self.hasDirs():
            return header + "\n" + "\n".join(children)
        else:
            return header

    def getSearchable(self):
        index = {}
        for name, pyFile in self._getFileList():
            index[name] = pyFile
        return index

    def getSearchableDir(self):
        index = {}
        for name, pyFile in self._getDirList():
            index[name] = pyFile
        return index


    def _getFileList(self):
        fileList = [ (x.filename, x) for x in self.pyFiles]
        for direc in self.dirs:
            fileList.extend(direc._getFileList())
        return fileList

    def _getDirList(self):
        dirList = [ (self.name, self)]
        for direc in self.dirs:
            dirList.extend(direc._getDirList())
        return dirList

    def __repr__(self):
        return self.name.split("/")[-1]



class PyFile:
    def __init__(self, filename, parent):
        self.filename = filename
        self.parent = parent
        self.loops = []
    def __str__(self):
        return self.filename

    def addLoop(self,loop):
        self.loops.append(loop)



def buildFileIndex(directory):
    pass



if __name__ == "__main__":
    print str(Directory(sys.argv[1]))

