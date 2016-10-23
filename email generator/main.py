import sys
##import MySQLdb
from PyQt4 import QtCore, QtGui, uic, QtSql
from PyQt4.QtSql import QSqlTableModel, QSqlQueryModel,QSqlDatabase
from datetime import datetime
from htmlGen import generateTemplate
from listfiles import importFiles

# from htmlGen import generateTemplate
# from listfiles import importFiles
 
qtCreatorFile = "crm.ui" # Enter gui file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


clickedRow = 0
clickedCol = 0

 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):


    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
#
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        
##        db.setDatabaseName('db_complete.sqlite')
        db.setHostName("localhost")
        db.setDatabaseName("db_complete.sqlite")
        db.setUserName("root")
        db.setPassword("")
        dbOpenStr = 'Database open = ' + str(db.open())

        drivers = QSqlDatabase.drivers ()
        print (drivers)

        
        print (db.lastError().text())


        self.msgLabel.setText(dbOpenStr)
##            print ('db open = ' + str(db.open()))
        
        #set timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.displayTime)
##        self.timer.timeout.connect(self.isDirtyDisplay)
        self.timer.start()

        #set table model for db
        self.projectModel = QSqlTableModel()
        self.projectModel.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.projectModel.setTable("leady")
        self.projectModel.select()
        self.projectView = self.tableView
        self.projectView.setModel(self.projectModel)
        self.projectView.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.projectView.setSortingEnabled(True)
        self.projectView.resizeColumnsToContents ()

        #proxy model which task is to block first column edition (ID column)
        self.proxy = ProxyModel(self)
        self.proxy.setSourceModel(self.projectModel)
        self.projectView.setModel(self.proxy)
        self.projectView.model().setColumnReadOnly(0, True)

        self.projectView.clicked.connect(self.viewClicked)
       
        #connect buttons and signals
        self.submitButton.clicked.connect(self.submitButtonEvt)
        self.addButton.clicked.connect(self.addButtonEvt)
        self.exitButton.clicked.connect(self.exitButtonEvt)
        self.revertButton.clicked.connect(self.revertButtonEvt)
        self.removeButton.clicked.connect(self.removeButtonEvt)
        self.generateButton.clicked.connect(self.generateButtonEvt)
        self.searchButton.clicked.connect(self.searchButtonEvt)
        self.addtodbButton.clicked.connect(self.addtodbButtonEvt)

		#search engine starts query after any text change in search text field
        self.searchInput.textChanged.connect(self.searchButtonEvt)

        #delegate - not really implemented yet
        deleg = delegate()
        self.projectView.setItemDelegate(deleg)
        
        self.projectView.show()

        
        #init comboboxes
        tabFiles = importFiles('tabele')        
        tempFiles = importFiles('szablony')
        self.chooseTable.addItems(tabFiles)
        self.chooseTemplate.addItems(tempFiles)
        #init stopka
        user = ['John Doe', 'Jane Doe', 'Agnes Doe']
        self.chooseStopka.addItems(user)

    def addtodbButtonEvt(self):
        dataIn = self.rowInput.toPlainText()
        dataSep = dataIn.split()
        print (dataSep)
        global windoww
        windoww = testApp()
        windoww.show()
        self.close()

        #bajzel i niepotrzebne zmienne o chuj tu chodzi
    def viewClicked(self,modelIndex):
        modell = modelIndex.model()
        global clickedRow, clickedCol
        clickedRow=modelIndex.row()
        clickedCol=modelIndex.column()
        if hasattr(modell, 'mapToSource'):
        # We are a proxy model
            modelIndex = modell.mapToSource(modelIndex)

        self.data = []
        
        for column in range(modell.columnCount()):
          datum = self.projectModel.record(clickedRow).field(column).value()
          self.data.append(datum)

    def searchButtonEvt(self):
        text = str(self.searchInput.text())
        text = text.split()
##        print (text)
        items = len(text)
        query = []

		#create SQL query
        for i in range(items):
            c = ('%' + text[i] + '%')
            statement = """(Sektor LIKE '%s' OR Strona LIKE '%s' OR Poz LIKE '%s' OR Poprawa_str LIKE '%s' OR email LIKE '%s' OR tel LIKE '%s' OR Imie_i_nazwisko LIKE '%s' OR Zasięg LIKE '%s' OR Zainteresowanie LIKE '%s' OR Komentarz LIKE '%s')""" % (c,c,c,c,c,c,c,c,c,c)
            query.append(statement)

        query = ' AND '.join(query)

        self.projectModel.setFilter(query)


    def displayTime(self):
        currentTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')        
        self.timeDisp.setText(currentTime)
        
    def exitButtonEvt(self):
        sys.exit(app.exec_())

    def submitButtonEvt(self):
        ok = self.projectModel.submitAll()
        self.msgLabel.setText('Data submitted: ' + str(ok))
        

    def revertButtonEvt(self):
        ok = self.projectModel.revertAll()
        self.msgLabel.setText('Reverted changes ')
##        print ('Reverted changes: ' + str(ok))

    def addButtonEvt(self):
        rowCnt = self.projectModel.rowCount()
        self.projectModel.insertRows(rowCnt,1)
        self.msgLabel.setText('Row added ')
        
    def removeButtonEvt(self,clickedIndex):
        rowI = self.row
        self.projectModel.removeRow(rowI)
        self.msgLabel.setText('Row removed: ')

    def generateButtonEvt(self):
        if self.offerPos.isChecked():
            posFlag = True
        else:
            posFlag = False
        if self.offerSite.isChecked():
            siteFlag = True
        else:
            siteFlag = False
        if self.addPromo.isChecked():
            promoFlag = True
        else:
            promoFlag = False

        cena = self.cenaInput.text()
        konkur = self.konkurInput.text()
        wyszuk = self.wyszukInput.text()
        keywords = self.keywordsInput.toPlainText()
        
        d = {'cena' : cena,'konkur' : konkur, 'wyszuk' : wyszuk, 'keywords' : keywords}

        print (d['keywords'])
            
        strr = ''
        tytul = (self.titleInput.text())
        tytul = str(tytul)
        promoText = (self.promoInput.toPlainText())
        files = [str(self.chooseTable.currentText()),str(self.chooseTemplate.currentText())]
        userOn = str(self.chooseStopka.currentText())
        strr = generateTemplate(self.data,promoFlag,promoText,tytul,userOn,files,d)
        self.genOut.setText(strr)


# class used to implement coloured fields and other visual effects. Not really implemented yet
class delegate(QtGui.QItemDelegate):                
    def __init__(self,parent = None):
        super(delegate,self).__init__(parent)
##        self.selectionmodel = parent.selectionModel()
        

    def paint(self, painter, option, index):

            r = option.rect
##            painter.save() 
            mainColor = QtGui.QColor(255,255,0)
            mainLight = mainColor.light(175)
            
##            if self.myCellReadOnly(index.row(), index.column()):
            if (index.row() == clickedRow) and (index.column() == clickedCol):
                painter.fillRect(r, mainLight)
                painter.drawText(r, QtCore.Qt.AlignCenter,
                                 str(index.model().data(index)))
            else:
                QtGui.QItemDelegate.paint(self, painter, option, index)
##            painter.restore()

# class testApp(QtGui.QMainWindow, Ui_TestWindow):
    # def __init__(self):
        # QtGui.QMainWindow.__init__(self)
        # Ui_TestWindow.__init__(self)
        # self.setupUi(self)

        # self.twojastaraButton.clicked.connect(self.twojastaraEvt)

    # def twojastaraEvt(self):
        # global window
        # window = MyApp()
        # window.show()
        # self.close()

class ProxyModel(QtGui.QIdentityProxyModel):
    def __init__(self, parent=None):
        super(ProxyModel, self).__init__(parent)
        self._columns = set()

    def columnReadOnly(self, column):
        return column in self._columns

    def setColumnReadOnly(self, column, readonly=True):
        if readonly:
            self._columns.add(column)
        else:
            self._columns.discard(column)

    def flags(self, index):
        flags = super(ProxyModel, self).flags(index)
        if self.columnReadOnly(index.column()):
            flags &= ~QtCore.Qt.ItemIsEditable
        return flags



if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    global window
    window = MyApp()
    window.show()


    ##########
    sys.exit(app.exec_())
