import sys, socket, time
from PyQt4 import QtGui,QtCore

from stockmanagerwindow import StockManagerWindow
from commfunctions import *

if __name__ == "__main__":
    app=QtGui.QApplication(sys.argv)
    window = StockManagerWindow()
    window.show()
    window.setTellingList(getTellingList())
    app.exec_()
    
