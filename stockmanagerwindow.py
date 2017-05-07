from PyQt4 import QtCore, QtGui, Qt
from ui_stockmanager import Ui_MainWindow
from commfunctions import * 

class StockManagerWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Set up the user interface from Designer.
        self.setupUi(self)
        
##        # Connect up the buttons.
##        self.connect(self.okButton, QtCore.SIGNAL("clicked()"),
##                     self, QtCore.SLOT("accept()"))
##        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"),
##                     self, QtCore.SLOT("reject()"))

        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.printTable)
        self.connect(self.tellingListWidget, QtCore.SIGNAL("itemSelectionChanged()"), self.showData)
        self.connect(self.markAsCountedButton, QtCore.SIGNAL("clicked()"), self.markAsCounted)
        self.connect(self.actionNieuwe_telling, QtCore.SIGNAL("clicked()"), self.newTelling)

    def newTelling(self):
        print "starting new telling"
    
    def markAsCounted(self):
        if self.tellingTabWidget.currentIndex()==1:
            selection = self.tableWidget2.selectedItems()
            if len(selection)>0:
                allrows={}
                rowindices=[]
                for s in selection:
                    rowindices.append(s.row())
                rowindices=self.uniqifyList(rowindices)
                self.tableWidget1.setSortingEnabled(0)
                self.tableWidget2.setSortingEnabled(0)
                for r in rowindices:
                    prodid=self.tableWidget2.item(r,0).text()
                    name=self.tableWidget2.item(r,1).text()
                    q=self.tableWidget2.item(r,2).text()
                    allrows[prodid]=q
                    # add to counted table
                    #row=self.tableWidget1.rowCount()
                    #self.tableWidget1.setRowCount(row+1)
                    #self.tableWidget1.setItem(row+1,0,QtGui.QTableWidgetItem(prodid))
                    #self.tableWidget1.setItem(row+1,1,QtGui.QTableWidgetItem(name))
                    #self.tableWidget1.setItem(row+1,2,QtGui.QTableWidgetItem(str(float(q))))
                    #self.tableWidget1.setItem(row+1,3,QtGui.QTableWidgetItem(str(float(q))))
                    #self.tableWidget1.setItem(row+1,4,QtGui.QTableWidgetItem("today"))                    					
                # which telling is selected?
                item = self.tellingListWidget.currentItem()
                telling = item.text()[0:6]
                markProductsAsCounted(telling,allrows)
                # remove the items from the table
                for r in rowindices:
                    self.tableWidget2.setRowHidden(r,1)
                self.tableWidget2.setSortingEnabled(1)
                self.tableWidget2.sortItems(0)
                self.tableWidget2.resizeColumnsToContents()				
                self.tableWidget1.setSortingEnabled(1)
                self.tableWidget1.sortItems(0)
                self.tableWidget1.resizeColumnsToContents()

    def uniqifyList(self,seq):                
        # Not order preserving 
        keys = {} 
        for e in seq: 
            keys[e] = 1 
        return keys.keys()
    
    def showData(self):
        self.setCursor(QtCore.Qt.WaitCursor)
        # which telling is selected?
        item = self.tellingListWidget.currentItem()
        telling = item.text()[0:6]
        #counted products
        self.tableWidget1.setSortingEnabled(0)
        self.setCountedProductList(getTelling(str(telling)))
        self.tableWidget1.setSortingEnabled(1)
        self.tableWidget1.sortItems(0)
        self.tableWidget1.resizeColumnsToContents()
        #missed products
        self.tableWidget2.setSortingEnabled(0)
        self.setMissedProductList(getMissedProducts(str(telling)))
        self.tableWidget2.setSortingEnabled(1)
        self.tableWidget2.sortItems(0)
        self.tableWidget2.resizeColumnsToContents()
        self.setCursor(QtCore.Qt.ArrowCursor)
        
    def setTellingList(self,tellinglist):
        for telling in tellinglist:
            st=telling.id+'\n'+telling.datecreation+' -> '+telling.datechange
            item=QtGui.QListWidgetItem(st,self.tellingListWidget)

   
            
    def setCountedProductList(self,productlist):
        # first, clear the table
        self.tableWidget1.clearContents()
        for i in range(0,self.tableWidget1.rowCount()):
            self.tableWidget1.removeRow(i)
        # fill in the data
        row=0
        for product in productlist:
            # create row
            self.tableWidget1.setRowCount(row+1)
            # populate
            item1=QtGui.QTableWidgetItem(product.id)
            self.tableWidget1.setItem(row,0,QtGui.QTableWidgetItem(product.id))
            self.tableWidget1.setItem(row,1,QtGui.QTableWidgetItem(product.name))
            self.tableWidget1.setItem(row,2,QtGui.QTableWidgetItem(str(self.toFloat(product.quantity_original))))
            self.tableWidget1.setItem(row,3,QtGui.QTableWidgetItem(str(self.toFloat(product.quantity_new))))
            self.tableWidget1.setItem(row,4,QtGui.QTableWidgetItem(product.datechange))
            row=row+1
            
    def setMissedProductList(self,productlist):
        # first, clear the table
        self.tableWidget2.clearContents()
        for i in range(0,self.tableWidget2.rowCount()):
            self.tableWidget2.removeRow(i)
        # fill in the data
        row=0
        for product in productlist:
            # create row
            self.tableWidget2.setRowCount(row+1)
            # populate
            item1=QtGui.QTableWidgetItem(product.id)
            self.tableWidget2.setItem(row,0,QtGui.QTableWidgetItem(product.id))
            self.tableWidget2.setItem(row,1,QtGui.QTableWidgetItem(product.name))
            self.tableWidget2.setItem(row,2,QtGui.QTableWidgetItem(str(self.toFloat(product.quantity_original))))
            row=row+1

    def toFloat(self,f):
        try:
            return float(f)
        except ValueError,e:
            return 0.0
            
    def printTable(self):
        # which table is selected
        index = self.tellingTabWidget.currentIndex()
        if index==0:
            self.printCountedTable()
        else:
            self.printMissedTable()
        
    def printCountedTable(self):
        linesperpage=50
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
##        printer.setOutputFileName("print.pdf")
##        printer.setFullPage(1)
##        printer.setPageSize(printer.A4)
        printDialog= QtGui.QPrintDialog(printer,self);
        res  = printDialog.exec_()
        if (res == QtGui.QDialog.Accepted):
#        if 1:
            painter = QtGui.QPainter(printer)
            painter.begin(printer)
            #rowsize=printer.PdmHeight*20
            resolution=printer.resolution()
            rowsize=resolution/5
            offset=resolution/4
            yoffset=3*rowsize
            # draw headers
            boldFont = QtGui.QFont("Times", 12, QtGui.QFont.Bold);
            normalFont = QtGui.QFont("Times", 9, QtGui.QFont.Normal);
            painter.setFont(boldFont)
            painter.drawText(offset,yoffset,"Id")
            painter.drawText(offset+resolution*1,yoffset,"Productnaam")
            painter.drawText(offset+resolution*5,yoffset,"Origineel")
            painter.drawText(offset+resolution*6,yoffset,"Geteld")
            painter.drawText(offset+resolution*7,yoffset,"Datum")
            # draw line
            pen=QtGui.QPen()
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawLine(offset/2,yoffset+(rowsize/2),offset+resolution*8,yoffset+(rowsize/2))
            # draw data
            painter.setFont(normalFont)
            linecounter=0
            selection = self.tableWidget1.selectedIndexes()
            if len(selection)>0:
                allrows=[]
                for s in selection:
                    allrows.append(s.row())
                allrows.sort()
                rows=allrows[0::5]
                while(linecounter<len(rows)):
                    for row in range(0,linesperpage):
                        index=(rows[linecounter])
                        painter.drawText(offset,yoffset+rowsize*(row+2),self.tableWidget1.item(index,0).text())
                        painter.drawText(offset+resolution*1,yoffset+rowsize*(row+2),self.tableWidget1.item(index,1).text())
                        painter.drawText(offset+resolution*5,yoffset+rowsize*(row+2),self.tableWidget1.item(index,2).text())
                        painter.drawText(offset+resolution*6,yoffset+rowsize*(row+2),self.tableWidget1.item(index,3).text())
                        painter.drawText(offset+resolution*7,yoffset+rowsize*(row+2),self.tableWidget1.item(index,4).text())
                        linecounter=linecounter+1
                        if(linecounter>=len(rows)):
                            break
                    if(linecounter>=len(rows)):
                            break
                    printer.newPage()
            else:
                while(linecounter<self.tableWidget1.rowCount()):
                    for row in range(0,linesperpage):
                        painter.drawText(offset,yoffset+rowsize*(row+2),self.tableWidget1.item(linecounter,0).text())
                        painter.drawText(offset+resolution*1,yoffset+rowsize*(row+2),self.tableWidget1.item(linecounter,1).text())
                        painter.drawText(offset+resolution*5,yoffset+rowsize*(row+2),self.tableWidget1.item(linecounter,2).text())
                        painter.drawText(offset+resolution*6,yoffset+rowsize*(row+2),self.tableWidget1.item(linecounter,3).text())
                        painter.drawText(offset+resolution*7,yoffset+rowsize*(row+2),self.tableWidget1.item(linecounter,4).text())
                        linecounter=linecounter+1
                        if(linecounter>=self.tableWidget1.rowCount()):
                            break
                    if(linecounter>=self.tableWidget1.rowCount()):
                            break
                    printer.newPage()
            painter.end()

    def printMissedTable(self):
        linesperpage=50
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
##        printer.setOutputFileName("print.pdf")
##        printer.setFullPage(1)
##        printer.setPageSize(printer.A4)
        printDialog= QtGui.QPrintDialog(printer,self);
        res  = printDialog.exec_()
        if (res == QtGui.QDialog.Accepted):
#        if 1:
            painter = QtGui.QPainter(printer)
            painter.begin(printer)
            #rowsize=printer.PdmHeight*20
            resolution=printer.resolution()
            rowsize=resolution/5
            offset=resolution/4
            yoffset=3*rowsize
            # draw headers
            boldFont = QtGui.QFont("Times", 12, QtGui.QFont.Bold);
            normalFont = QtGui.QFont("Times", 9, QtGui.QFont.Normal);
            painter.setFont(boldFont)
            painter.drawText(offset,yoffset,"Id")
            painter.drawText(offset+resolution*1,yoffset,"Productnaam")
            painter.drawText(offset+resolution*5,yoffset,"In stock")
            # draw line
            pen=QtGui.QPen()
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawLine(offset/2,yoffset+(rowsize/2),offset+resolution*8,yoffset+(rowsize/2))
            # draw data
            painter.setFont(normalFont)
            linecounter=0
            
            selection = self.tableWidget2.selectedIndexes()
            if len(selection)>0:
                allrows=[]
                for s in selection:
                    allrows.append(s.row())
                allrows.sort()
                rows=allrows[0::3]
                while(linecounter<len(rows)):
                    for row in range(0,linesperpage):
                        index=(rows[linecounter])
                        painter.drawText(offset,yoffset+rowsize*(row+2),self.tableWidget2.item(index,0).text())
                        painter.drawText(offset+resolution*1,yoffset+rowsize*(row+2),self.tableWidget2.item(index,1).text())
                        painter.drawText(offset+resolution*5,yoffset+rowsize*(row+2),self.tableWidget2.item(index,2).text())
                        linecounter=linecounter+1
                        if(linecounter>=len(rows)):
                            break
                    if(linecounter>=len(rows)):
                            break
                    printer.newPage()
                            
            else:
                while(linecounter<self.tableWidget2.rowCount()):
                    for row in range(0,linesperpage):
                        painter.drawText(offset,yoffset+rowsize*(row+2),self.tableWidget2.item(linecounter,0).text())
                        painter.drawText(offset+resolution*1,yoffset+rowsize*(row+2),self.tableWidget2.item(linecounter,1).text())
                        painter.drawText(offset+resolution*5,yoffset+rowsize*(row+2),self.tableWidget2.item(linecounter,2).text())
                        linecounter=linecounter+1
                        if(linecounter>=self.tableWidget2.rowCount()):
                            break
                    if(linecounter>=self.tableWidget2.rowCount()):
                            break
                    printer.newPage()

            painter.end()
