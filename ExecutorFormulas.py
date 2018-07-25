#!/usr/bin/python
# -*- coding: latin-1 -*-

'''
Created on 22 de jul de 2018

@author: ryan
'''
import sys

# Private Version of myFormula
from formulas import myFormula

# Comercial Version file funcoes.py
#from funcoes import myFormula

from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
from types import FunctionType

class ExecutorFormulas(QtGui.QMainWindow):

    def __init__(self):
        super(ExecutorFormulas, self).__init__()
        uic.loadUi('GUI_v01.ui', self)
        self.show()
        
        # Debug Components
        self.btnDebug.clicked.connect(self.showDebug)
        self.aMenuDebug.triggered.connect(self.isChecked)
        self.btnDebug.setEnabled(0)
        
        # Defining button events to callback
        self.btnClear.clicked.connect(self.clear)
        self.btnCalc.clicked.connect(self.calcular)
        self.btnConvert.clicked.connect(self.converter)

        # Set disabled fields before function to be chosen é
        self.btnConvert.setEnabled(0)
        self.rb1.setEnabled(0)
        self.rb2.setEnabled(0)
        self.rb3.setEnabled(0)

        # Create objFormulas from "import formulas" file formulas.py (Class myFormula)
        self.objFormulas = myFormula()
        #self.objFormulas = FormulasMatematicas()
        
        self.comboBox.addItem("Selecione uma formula...")
        self.myFunctions = self.methods(myFormula)
        #self.myFunctions = self.methods(FormulasMatematicas)

        # Loop to check all functions on myFunctions Class but __init__, *GetEnum, Convert and __methods
        # and include it to the comboBox field
        for func in self.myFunctions:
            if func == "__init__" or "GetEnum" in func or "Convert" in func or "__" in func:
                continue
            self.comboBox.addItem(func)

        #Defining selected field and changeIndex event to the callback
        self.comboBox.setCurrentIndex(0)
        self.comboBox.currentIndexChanged.connect(self.novaFormula)

        #Definindo controles e objetos:
        self.varis = []
        self.varislen = 0
        self.unity = []
        self.activeUnity = 0
        self.Enum = ""
        self.result = ""
    

    '''
    Callback for Menu debug when it (check|uncheck)
    '''
    def isChecked(self):
        if self.aMenuDebug.isChecked():
            self.textEdit.setText("Habilitando debug")
            self.btnDebug.setEnabled(1)
        else:
            self.textEdit.setText("Desabilitando debug")
            self.btnDebug.setEnabled(0)

        pass

    '''
    Function to collect the selected unity
    '''
    def unidades(self):
        
        if self.rb1.isChecked():
            self.activeUnity = self.rb1.text()
        elif self.rb2.isChecked():
            self.activeUnity = self.rb2.text()
        else:
            self.activeUnity = self.rb3.text()
    
    '''
    Function to collect all the variables in the line edit
    return false if some mandatory variable is empty
    '''
    def variaveis(self):
        
        #TODO: To analyse if all mandatory variables are 
        #int/float numbers and not string (return false if string are found)

        if(self.varislen == 3): 
            self.x = self.leVar1.text()
            self.y = self.leVar2.text()
            self.z = self.leVar3.text()
            
            if (self.x == "" or self.y == "" or self.z == ""):
                return False
            
        if(self.varislen == 2): 
            self.x = self.leVar1.text()
            self.y = self.leVar2.text()
            
            if (self.x == "" or self.y == "" ):
                return False
        
        if(self.varislen == 1): 
            self.x = self.leVar1.text()
            
            if (self.x == "" ):
                return False
        
        return True
        
    '''
    Callback for Calcular button when it got pressed
    '''
    def calcular(self):
        
        # If variaveis() returns false, show up dialog error for unvalid variables
        if(not self.variaveis()):
            self.showdialog("Por favor, insira os dados solicitados.", self.varis)
            return
        
        # Check and set unity
        self.unidades()
 
        #Build up the string to be evalued to call selected formula
        func = "self.objFormulas.%s" % self.comboBox.currentText()

        # If unity was defined we're going to return activeUnity to the Formula method
        if len(self.unity) > 0:
            aUnity = ", self.activeUnity"
        else:
            aUnity = ""
        
        # Include variable arguments to the string to be evalued 
        if self.varislen == 3:
            func += "(self.x, self.y, self.z %s)" % aUnity
        elif(self.varislen == 2):
            func += "(self.x, self.y %s)" % aUnity
        else:
            func += "(self.x %s)" % aUnity
 
        if self.aMenuDebug.isChecked(): 
            print func
            strshow, self.result = eval(func)
            self.showResult(strshow + "\nResultado = %.2f" % self.result)
        else:

            # Executing the formula calculation under try/except error handling mechanism
            # If some error happens during this block the except will handle the error
            try:
                # Execute the string as regular function call via eval()
                strshow, self.result = eval(func)
       
                # Print out the result from the executed formula
                self.showResult(strshow + "\nResultado = %.2f" % self.result)

            except:
                self.showdialog("Erro Inesperado (Cags in run) durante execução da formula. Verifique a implementacao da formula.", sys.exc_info()[0])
    
        
    '''
    Callback for Convert button when it got pressed
    '''
    def converter(self):

        if self.result == "":
            self.textEdit.setText("Sem 'Result' na memoria.")
            return

        # Get actual Unity
        unit = self.activeUnity

        # Update unity selected
        self.unidades()

        # Get the new selected unity
        unitToConvert = self.activeUnity


        if "Converter" in dir(self.objFormulas):
            # Call the Convert method to process de unity conversion
            # Should have the case implemented
            result = self.objFormulas.Converter(self.result, unit, unitToConvert)
            self.textEdit.setText("Convertendo:\nResultado %.2f %s para %s\n%.2f %s" % \
                                (self.result,unit, unitToConvert, result, unitToConvert))
        else:
            self.showdialog("Funcao Converter nao disponivel. Verifique a implementacao da funcao de conversao.", ["self.objFormulas.Converter", "Missing"] )
            result = 0
        
        self.result = result

    '''
    Callback for new formula selected on the combobox
    '''
    def novaFormula(self):
    
        # If select the neutral option on the combobox ("Selecione uma formula...")
        if self.comboBox.currentText() == "Selecione uma formula...":
            self.clear()
            return

        #Clean up all fields
        self.clear()

        if self.aMenuDebug.isChecked(): 
            func = "self.objFormulas.%sGetEnum()" % self.comboBox.currentText()
            self.varis, self.Enum, self.unity = eval(func)
            self.varislen = len(self.varis)
            self.lblEnum.setText(self.Enum)
        
            self.setlbl()
            self.setrb()

        else:

            # Executing the formula GetEnum under try/except error handling mechanism
            # If some error happens during this block the except will handle the error
            try:
                func = "self.objFormulas.%sGetEnum()" % self.comboBox.currentText()
                self.varis, self.Enum, self.unity = eval(func)
                self.varislen = len(self.varis)
                self.lblEnum.setText(self.Enum)
        
                self.setlbl()
                self.setrb()
            except:
                self.showdialog("Erro Inesperado (Cags in run) durante execução da GetNum.\
                        Verifique a implementação da função GetNum.", sys.exc_info()[0])

   
    '''
    Function to set all the variables names and labels.
    This function will also disable/enable unused/used var fields
    '''
    def setlbl(self):
        
        # If we have 3 variables for this formula
        if (self.varislen == 3):
            self.lblVar1.setText(self.varis[0])
            self.lblVar2.setText(self.varis[1])
            self.lblVar3.setText(self.varis[2])
            
            self.leVar2.setEnabled(1)
            self.leVar3.setEnabled(1)

         
        # If we have 2 variables for this formula
        elif(self.varislen == 2):
            self.lblVar1.setText(self.varis[0])
            self.lblVar2.setText(self.varis[1])
            
            self.lblVar3.setText("")

            self.leVar2.setEnabled(1)
            self.leVar3.setDisabled(1)
    
        # If we have 1 variables for this formula
        else:
            self.lblVar1.setText(self.varis[0])
            self.lblVar2.setText("")
            self.lblVar3.setText("")
            self.leVar2.setDisabled(1) 
            self.leVar3.setDisabled(1)

    '''
    Function to set all the radio button unity names and labels.
    This function will also disable/enable unused/used unity fields
    '''
    def setrb(self):

        # If we have 3 unities for this formula
        if (len(self.unity) == 3):
            self.rb1.setText(self.unity[0])
            self.rb2.setText(self.unity[1])
            self.rb3.setText(self.unity[2])
            
            self.rb1.setEnabled(1)
            self.rb2.setEnabled(1)
            self.rb3.setEnabled(1)
            self.btnConvert.setEnabled(1)
            

        # If we have 2 unities for this formula
        if (len(self.unity) == 2):
            self.rb1.setText(self.unity[0])
            self.rb2.setText(self.unity[1])
            self.rb3.setText("")

            self.rb1.setEnabled(1)
            self.rb2.setEnabled(1)
            self.rb3.setEnabled(0)
            self.btnConvert.setEnabled(1)
        

        # If we have 1 unities for this formula
        if(len(self.unity) == 1):
            self.rb1.setText(self.unity[0])
            self.rb2.setText("")
            self.rb3.setText("")
            self.rb1.setEnabled(1)
            self.rb2.setEnabled(0)
            self.rb3.setEnabled(0)
            self.btnConvert.setEnabled(0)
            
            
        # If we have no unity for this formula
        if(len(self.unity) == 0):
            self.rb1.setEnabled(0)
            self.rb2.setEnabled(0)
            self.rb3.setEnabled(0)
            self.btnConvert.setEnabled(0)
            

    '''
    Function to clear the variables fields
    '''
    def clear(self):
       
        self.leVar1.setText("")
        self.leVar2.setText("")
        self.leVar3.setText("")
        
        self.textEdit.setText("")

        self.result = ""
        self.unity = 0
    
    '''
    Function to print the output to the user at the textEdit
    '''
    def showResult(self, strshow):
        self.textEdit.setText("%s" % strshow )
        
    '''
    Function to show the error when processing the formula
    '''
    def showdialog(self, message, details):

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setText(message)
        msg.setInformativeText("Detalhes")
        msg.setWindowTitle("Erro de Dados")
        msg.setDetailedText("Detalhes do erro:\n%s" % details)
        msg.setStandardButtons(QMessageBox.Cancel)
    
        msg.exec_()
   
    '''
    Function to show the debug status
    '''
    def showDebug(self):
        
        #self.unidades()
        
        debug = "Var1 = %s |Var2 = %s |Var3 = %s\nFunc = %s | Unidade = %s\nVaris %s\nUnity %s\nResult %s" % \
                (self.leVar1.text(),self.leVar2.text(), self.leVar3.text(), 
                 self.comboBox.currentText(), self.activeUnity,
                 self.varis, self.unity, self.result) 
        self.textEdit.setText(debug)
        #self.textEdit.setText(self.lineEdit.text())
        #self.textEdit.setText(self.lineEdit.text())        

    '''
    Function to check all the methods (functions) in a class
    '''
    def methods(self, cls):
        return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]


#Main function to start the program
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myApp = ExecutorFormulas()
    sys.exit(app.exec_())
    
