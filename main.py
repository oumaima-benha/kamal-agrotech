import os
import pywhatkit
import sys
from ui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from PyQt5 import QtSql
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

class form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('products.db')
        self.model = QtSql.QSqlTableModel()
        self.model.setTable('products')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,"id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,"name")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "description")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "expiration_date")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal,"price")
        self.ui.tableWidget.setModel(self.model)
        self.ui.pushButton.clicked.connect(self.addToDb)
        self.show()
        self.ui.pushButton_2.clicked.connect(self.updaterow)
        self.ui.pushButton_3.clicked.connect(self.delrow)
        self.i = self.model.rowCount()
        self.ui.lcdNumber.display(self.i)

        self.onlyInt = QtGui.QIntValidator()
        self.ui.lineEdit_3.setValidator(self.onlyInt)
        self.ui.pushButton_4.clicked.connect(self.search)


    def addToDb(self):
        self.model.insertRows(self.i,1)
        self.model.setData(self.model.index(self.i,1),self.ui.lineEdit.text())
        self.model.setData(self.model.index(self.i, 2), self.ui.lineEdit_2.text())
        self.model.setData(self.model.index(self.i,4), self.ui.lineEdit_3.text())
        self.model.setData(self.model.index(self.i,3), self.ui.dateEdit.text())
        self.model.submitAll()
        self.i += 1
        self.ui.lcdNumber.display(self.i)

    def delrow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            self.model.removeRow(self.ui.tableWidget.currentIndex().row())
            self.i -= 1
            self.model.select()
            self.ui.lcdNumber.display(self.i)
        else:
            QMessageBox.question(self,'Message', "Please select a row would you like to delete", QMessageBox.Ok)
            self.show()

    def updaterow(self):
        if self.ui.tableWidget.currentIndex().row() > -1:
            record = self.model.record(self.ui.tableWidget.currentIndex().row())    
            if(record.value("quantity") == 0):
                product = record.value("name")
                msg = "The product {} is no longer in stock"
                number = os.environ["PHONE_NUMBER"]
                pywhatkit.sendwhatmsg_instantly(number, msg.format(product), 60, True)        
            record.setValue("name",self.ui.lineEdit.text())
            record.setValue("description",self.ui.lineEdit_2.text())
            record.setValue("experiation_date", self.ui.dateEdit.text())
            record.setValue("price", self.ui.lineEdit_3.text())
        else:
            QMessageBox.question(self,'Message', "Please select a row would you like to update", QMessageBox.Ok)
            self.show()

    def search(self):
        text = self.ui.lineEdit_5.text()        
        self.model.setFilter("name like '%" + str(text) + "%'")
        self.model.select()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = form()
    sys.exit(app.exec_())
