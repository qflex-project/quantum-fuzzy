from math import pi as Pi
from math import sqrt as sqrt
from cmath import exp
import genCirc
import numpy

H = [[0.707106781, 0.707106781], \
	[0.707106781, -0.707106781]]
ID = [[1.0, 0.0], [0.0, 1.0]]
X = [[0.0, 1.0], [1.0, 0.0]]

matrix = []

class teste:
	def __init__ (self):
		trans = [H,H,ID,ID,ID]

		self.genMatrix(trans)

	def genMatrix(self, trans):
		linhas = 2**(len(trans))

		for i in range(0,linhas):
			print (i, "\t",)
		print ("\n")

		for i in range(0,linhas):
			matrix.append([])
			self.genLine(trans, numpy.binary_repr(i,len(trans)), 0, 1.0,"")
			print ("\n")
		for i in range(0, len(matrix)):
			print (i, "\t", matrix[i])
			#print ([numpy.binary_repr(i,len(trans)),i], "\t", matrix[i])



	def genLine(self, trans, binary, ind, value, column):
		lis = trans[ind][int(binary[ind])]

		#print (value)
		for i in range(0, len(lis)):
			n_value = value * lis[i]
			if (ind+1 == len(trans)):
				#print (n_value)
				print (format(n_value, '0.1f'), "\t",)
				if (n_value > 0):
					matrix[-1].append(int(column+str(i),2))
				if (n_value < 0):
					matrix[-1].append(-int(column+str(i),2))
					#matrix[-1].append([numpy.binary_repr(int(column + str(i), 2), len(trans)),int(column+str(i),2)])
				#if (n_value < 0):
				#	matrix[-1].append(numpy.binary_repr(int(column + str(i), 2), len(trans))
				#print ("  ",)
				pass
			else:
				self.genLine(trans, binary, ind + 1, n_value, column + str(i))
