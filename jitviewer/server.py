from flask import Flask
import flask
import sys
import gatherinfo
import buildHTML
import selectHTML
import base64


class Server:
    def __init__(self, logFile, rootFolder):
        self.listing = gatherinfo.PopulatedListing(logFile,rootFolder)


    def index(self):
        return buildHTML.buildPage(self.listing.index[self.listing.default])

    def loop(self):
        fileName = flask.request.args['file']
        if fileName == 'default':
            pyFile = self.listing.index[self.listing.default]
        else:
            pyFile = self.listing.index[base64.b64decode(fileName)] #decode
        loopID = int(flask.request.args['loopID'])
        d = {"html": buildHTML.buildInnerTable(pyFile,loopID), "heat": buildHTML.buildHeatMap(pyFile,loopID)}
        return flask.jsonify(d)

    def expansion(self):
        print flask.request.args
        fileName = flask.request.args['file']
        if fileName == 'default':
            pyFile = self.listing.index[self.listing.default]
        else:
            pyFile = self.listing.index[base64.b64decode(fileName)] #decode
        loopID = int(flask.request.args['loopID'])
        lineNo = int(flask.request.args['lineNo'])
        chunkNo = int(flask.request.args['chunkNo'])

        print loopID
        d = {"html": buildHTML.buildExpansion(pyFile,loopID,lineNo,chunkNo)}
        return flask.jsonify(d)

    def getDirectory(self):
        directory = flask.request.args['directory']
        directory = base64.b64decode(directory)
        aDir = self.listing.indexDir[directory]
        selectionDiv = selectHTML.buildSelectionDiv(aDir)
        d = {'html': selectionDiv}
        return flask.jsonify(d)

    def getFile(self):
        filename = flask.request.args['file']
        filename = base64.b64decode(filename)
        pyFile = self.listing.index[filename]
        selectionDiv = selectHTML.buildSelectionDiv(pyFile)
        loopsDiv =  buildHTML.buildLoopSelector(pyFile,0)
        tableDiv =  buildHTML.buildTable(pyFile,0)
        heatDiv = "<div id=\"heatContainer\">"+buildHTML.buildHeatMap(pyFile,0)+"</div>\n"
        fileDiv = loopsDiv +"<br/>\n" + heatDiv + tableDiv
        d = {'path': selectionDiv,'select': buildHTML.buildSelectedBanner(pyFile),
                'file':fileDiv}
        return flask.jsonify(d)




def main():
    app = Flask(__name__)
    logfile, rootFolder = sys.argv[1:3]
    server = Server(logfile, rootFolder)
    app.route("/")(server.index)
    app.route("/loop")(server.loop)
    app.route("/expansion")(server.expansion)
    app.route("/directory")(server.getDirectory)
    app.route("/getFile")(server.getFile)
    app.run("0.0.0.0",debug=True)

if __name__ == "__main__":
    main()

