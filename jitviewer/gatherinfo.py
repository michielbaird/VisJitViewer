import sys
import os
import directoryIndex
import logParser

class PopulatedListing(directoryIndex.Directory):
    def __init__(self,logfile, rootDir):
        directoryIndex.Directory.__init__(self, rootDir)
        sources = logParser.getMySources(logfile)
        self.index = self.getSearchable()
        self.other = []
        for filename,source in sources:
            raw_fn = os.path.abspath(filename)
            pyF = self.index.get(raw_fn,None)
            if pyF != None:
                pyF.addLoop(source)
            else:
                self.other.append(source)

