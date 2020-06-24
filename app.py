import os
import re
import sys
from PyQt5 import QtWidgets

import design

class CalculatorApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
	storedNumbers = ('', '')
	storedOp = ''
	lastOpEqual = False

	def __init__(self):
		super().__init__()
		self.setupUi(self)

		# 1,2,3
		self.oneButton.clicked.connect(self.setData('1'))
		self.twoButton.clicked.connect(self.setData('2'))
		self.threeButton.clicked.connect(self.setData('3'))

		# 4,5,6
		self.fourButton.clicked.connect(self.setData('4'))
		self.fiveButton.clicked.connect(self.setData('5'))
		self.sixButton.clicked.connect(self.setData('6'))

		# # 7,8,9,0
		self.sevenButton.clicked.connect(self.setData('7'))
		self.eightButton.clicked.connect(self.setData('8'))
		self.nineButton.clicked.connect(self.setData('9'))
		self.zeroButton.clicked.connect(self.setData('0'))

		# # operations
		self.plus.clicked.connect(self.setOp('+'))
		self.minus.clicked.connect(self.setOp('-'))
		self.multiple.clicked.connect(self.setOp('*'))
		self.divide.clicked.connect(self.setOp('/'))
		self.calc.clicked.connect(self.calculateHandler)
		self.reset.clicked.connect(self.resetOp)

	def setData(self, number):
		def dataHandler():
			if self.lastOpEqual:
				self.lastOpEqual = False
				self.storedNumbers = ('', '')

			currentNumber = self.result.text()
			if re.search('^\s', currentNumber):
				currentNumber = '0'


			if float(currentNumber) == 0.0:
				if number == '0':
					return
				else:
					currentNumber = number
			
			if self.storedOp == '':
				currentNumber = self.storedNumbers[0] + number
				self.storedNumbers = (currentNumber, '')
			else:
				currentNumber = self.storedNumbers[1] + number
				self.storedNumbers = (self.storedNumbers[0], currentNumber)

			self.result.setText(currentNumber)

		return dataHandler

	def setOp(self, operation):
		def opHandler():
			self.lastOpEqual = False

			if self.storedOp != '' and self.storedNumbers[0] and self.storedNumbers[1]:
				self.calculate(operation) 

			self.storedOp = operation

		return opHandler

	def calculate(self, operation=''):
		if self.storedOp == '' or not self.storedNumbers[0] or not self.storedNumbers[1]:
			return
		currentNumber = self.result.text()
		numberOne = float(self.storedNumbers[0])
		numberTwo = float(self.storedNumbers[1])
		result = 0

		if self.storedOp == '+':
			result = numberOne + numberTwo
		elif self.storedOp == '-':
			result = numberOne - numberTwo
		elif self.storedOp == '*':
			result = numberOne * numberTwo
		elif self.storedOp == '/':
			if (numberTwo == 0.0):
				self.result.setText("Division by zero")
				self.storedNumbers = ('', '')
				self.storedOp = ''
				return
			else:
				result = numberOne / numberTwo

		self.result.setText(str(result))
		if operation:
			self.storedNumbers = (str(result), '')
		else:
			self.storedNumbers = (str(result), '')

		self.storedOp = ''

	def resetOp(self):
		self.storedNumbers = ('', '')
		self.storedOp = ''
		self.result.setText('0')

	def calculateHandler(self):
		self.lastOpEqual = True
		self.calculate()

def main():
	print("Started")
	app = QtWidgets.QApplication(sys.argv)
	app.setStyle("Fusion")
	window = CalculatorApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()
