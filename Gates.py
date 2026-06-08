from math import pi as Pi
from math import sqrt as sqrt
from cmath import exp
import numpy
from sympy import *
from sympy.interactive import init_printing
from sympy import latex, pi, sin, asin, Integral, Matrix, Rational
from sympy.abc import x, y, N, mu, r, tau

x1 = [1,[], "x1"]
x2 = [1,[], "x2"]
y1 = [1,[], "y1"]
y2 = [1,[], "y2"]
N = [1,[], "N"]

x = [1,[], "x"]
y = [1,[], "y"]

class Gates:
	def __init__(self):
		self.gatesList = {}
		self.addGate("Id", [[1, 0], [0, 1]])
		self.addGate("H", [[1/sqrt(2), 1/sqrt(2)], [1/sqrt(2), -1/sqrt(2)]])
		self.addGate("X", [[0, 1], [1, 0]])
		self.addGate("Z", [[1, 0], [0, -1]])
		self.addGate("Y", [[0, 1*I], [-1*I, 0]])
		self.addGate("V", [[(1 + sqrt(-1))/2, (-1 + sqrt(-1))/2], [(-1 + sqrt(-1))/2, (1 + sqrt(-1))/2]])

	def addGate(self, name, matrix):
		circ = self.gatesList.get(name)
		if circ != None:
			print ("Operador já existe", name)
			return

		self.gatesList[name] = matrix

	def getGate(self, name):
		return self.gatesList.get(name)
