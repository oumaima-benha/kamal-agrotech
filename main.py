import os
import pywhatkit
import sys
from ui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView, QWidget
from PyQt5 import QtSql
from PyQt5 import QtCore
from PyQt5 import QtGui

class MainForm(QMainWindow):
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
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,"Désignation")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,"Catégorie")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "N° d\'homologation")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Composition")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal,"Emballage")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal,"Prix d\'achat")     
        self.model.setHeaderData(6, QtCore.Qt.Horizontal,"Prix de vente")     
        self.model.setHeaderData(7, QtCore.Qt.Horizontal,"Quantité")     


        self.ui.tableWidget.setModel(self.model)        
        self.ui.AddPushButton.clicked.connect(self.addToDb)
        self.show()
        self.ui.SellingPrice_lineEdit.returnPressed.connect(self.addToDb)
        self.show()
        self.ui.UpdatePushButton.clicked.connect(self.updaterow)
        self.ui.DeletePushButton.clicked.connect(self.delrow)
        self.i = self.model.rowCount()
        self.ui.lcdNumber.display(self.i)

        self.onlyInt = QtGui.QIntValidator()
        self.ui.PurchasePrice_lineEdit.setValidator(self.onlyInt)
        self.ui.SellingPrice_lineEdit.setValidator(self.onlyInt)

        self.ui.SearchPushButton.clicked.connect(self.search)
        self.ui.Search_lineEdit.returnPressed.connect(self.search)



    def addToDb(self):
        self.model.insertRows(self.i,1)
        self.model.setData(self.model.index(self.i,0),self.ui.Name_lineEdit.text())
        self.model.setData(self.model.index(self.i, 1), self.ui.Category_lineEdit.text())
        self.model.setData(self.model.index(self.i,2), self.ui.Homologation_lineEdit.text())
        self.model.setData(self.model.index(self.i,3), self.ui.Composition_lineEdit.text())
        self.model.setData(self.model.index(self.i,4), self.ui.PackagingQuantity_lineEdit.text())
        self.model.setData(self.model.index(self.i,5), self.ui.PurchasePrice_lineEdit.text())
        self.model.setData(self.model.index(self.i,6), self.ui.SellingPrice_lineEdit.text())

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
            if(record.value("Quantity") == 0):
                product = record.value("Name")
                msg = "The product {} is no longer avalaible in stock"
                number = os.environ["PHONE_NUMBER"]
                pywhatkit.sendwhatmsg_instantly(number, msg.format(product), 60, True)        
            record.setValue("Name",self.ui.Name_lineEdit.text())
            record.setValue("Category",self.ui.Category_lineEdit.text())
            record.setValue("Homologation", self.ui.Homologation_lineEdit.text())
            record.setValue("Composition", self.ui.Composition_lineEdit.text())
            record.setValue("PackagingQuantity", self.ui.PackagingQuantity_lineEdit.text())
            record.setValue("PurchasePrice", self.ui.PurchasePrice_lineEdit.text())
            record.setValue("SellingPrice", self.ui.SellingPrice_lineEdit.text())
        else:
            QMessageBox.question(self,'Message', "Please select a row would you like to update", QMessageBox.Ok)
            self.show()

    def search(self):
        text = self.ui.Search_lineEdit.text()        
        self.model.setFilter("Name like '%" + str(text) + "%'")
        self.model.select()

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        self.ui.LoginButton.clicked.connect(self.check_password)
        self.ui.lineEdit_Password.returnPressed.connect(self.check_password)

    def check_password(self):
        username = os.environ["AGROTECH_USERNAME"]
        password = os.environ["AGROTECH_PASSWORD"]
        if self.ui.lineEdit_Username.text() == username and self.ui.lineEdit_Password.text() == password:
            self.mainForm = MainForm()
            self.mainForm.show()
            self.close()
        else:
            QMessageBox.question(self,"Erreur d'identification", "Les données entrées sont incorrects", QMessageBox.Ok)
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec_())
    
