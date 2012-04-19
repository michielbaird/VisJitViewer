#!/usr/bin/env python

import sys
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView

def main():
    if len(sys.argv) == 2:
        url = sys.argv[1]
        title = url
    elif len(sys.argv) == 3:
        url = sys.argv[1]
        title = sys.argv[2]
    else:
        print >> sys.stderr, "Usage: qwebview.py URL [title]"
        return 2

    app = QApplication(sys.argv)
    web = QWebView()
    web.resize(1320, 1000)
    web.setWindowTitle(title)
    web.load(QUrl(url))
    web.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
