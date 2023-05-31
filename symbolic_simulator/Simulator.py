from math import pi as Pi
from math import sqrt as sqrt
from cmath import exp
import numpy
import re as regex
 
import sympy
from sympy import *
from sympy.interactive import init_printing
from sympy import latex, pi, sin, asin, Integral, Matrix, Rational
from sympy.abc import x, y, N, mu, r, tau

"""
# Circuit format	
# Normal Gate -> Gate,Qubit -> Example: H,3 -> Applies Hadamard gate on qubit 3
# Controlled Gate -> C-Gate,TargetQubit-ControlQubits-ControlValues -> Example: C-X,3-1,2-1,0 -> Applies X gate on qubit 3 if qubits 1 and 2 are 1 and 0 respectively
### ControlValues is optional, will be considered as all 1s if not specified
### Can have multiple gates qubits like: X,3,H,4-1,2 -> Applies X gate on qubit 3 and H gate on qubit 4 if qubits 1 and 2 are 1
"""

import Gates

x1 = [1,[], "x1"]
x2 = [1,[], "x2"]
y1 = [1,[], "y1"]
y2 = [1,[], "y2"]
N = [1,[], "N"]

x = [1,[], "x"]
y = [1,[], "y"]

class Simulator:
	def __init__ (self):
		self.gates = Gates.Gates()

		self.state = None
		self.qubits = None

		pass

	def createState(self, numQubits, inputQubits):
		self.numQubits = numQubits
		self.qubits = []
		self.totalPositions = pow(2,self.numQubits)

		for i in range(len(inputQubits), self.numQubits):
			inputQubits.append(0)

		for i in range(0, self.numQubits):
			v0 = sympy.sqrt(1 - inputQubits[i])
			v1 = sympy.sqrt(inputQubits[i])

			self.qubits.append([v0, v1])
		
		self.state = []
		self.resultState = []
		for p in range(0, self.totalPositions):
			value = 1
			binary = [int(i) for i in list(numpy.binary_repr(p, self.numQubits))]
			for q in range(0, self.numQubits):
				value = value * self.qubits[q][binary[q]]
				if value == 0:
					break
			self.state.append(value)
			self.resultState.append(0)

	def getGate(self, name):
		return self.gates.getGate(name)
	
	def executeGate(self, gate, targetQubit, controlQubits = None, controlValues = None):
		posMask = 1 << targetQubit
		nPosMask = ~posMask

		if controlQubits != None:
			controlQubitsMask = 0
			controlValuesMask = 0
			for q in controlQubits:
				controlQubitsMask = controlQubitsMask | (1 << q)
			
			if controlValues != None:
				for q in range(0, len(controlValues)):
					controlValuesMask = controlValuesMask | (controlValues[q] << controlQubits[q])
			else:
				controlValuesMask = controlQubitsMask

			for p in range(0, self.totalPositions):
				if (p & controlQubitsMask) == controlValuesMask:
					l = (p & posMask) >> targetQubit
					p0 = p & nPosMask
					p1 = p0 | posMask

					self.resultState[p] = self.state[p0] * gate[l][0] + self.state[p1] * gate[l][1]
				else:
					self.resultState[p] = self.state[p]
		else:
			for p in range(0, self.totalPositions):
				l = (p & posMask) >> targetQubit
				p0 = p & nPosMask
				p1 = p0 | posMask
				self.resultState[p] = self.state[p0] * gate[l][0] + self.state[p1] * gate[l][1]

		tmp = self.state
		self.state = self.resultState
		self.resultState = tmp
	
	def executeCircuit(self, circuit):
		steps = circuit.split(";")
		for step in steps:
			if step[0] == 'C':	## controlled gate
				parts = step.split("-")
				gatesList = parts[1].split(",")
				controlQubits = [int(i) for i in parts[2].split(",")]
				controlValues = None
				if len(parts) > 3:
					controlValues = [int(i) for i in parts[3].split(",")]

				for g in range(0, len(gatesList), 2):
					gate = self.getGate(gatesList[g])
					targetQubit = int(gatesList[g+1])
					self.executeGate(gate, targetQubit, controlQubits, controlValues)

			else:				## normal gate
				gatesList = step.split(",")
				for g in range(0, len(gatesList), 2):
					gate = self.getGate(gatesList[g])
					targetQubit = int(gatesList[g+1])
					self.executeGate(gate, targetQubit)
	
	def printState(self):
		for p in range (0, len(self.state)):
			print (factor(self.state[p]))

	def printPosState(self):
		for p in range (0, len(self.state)):
			print (numpy.binary_repr(p, self.numQubits), factor(self.state[p]))

	def printNonZeroPosState(self):
		for p in range (0, len(self.state)):
			if self.state[p] != 0:
				print (numpy.binary_repr(p, self.numQubits), factor(self.state[p]))
	
