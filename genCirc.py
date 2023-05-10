from math import pi as Pi
from math import sqrt as sqrt
from cmath import exp
import numpy
from sympy import *
from sympy.interactive import init_printing
from sympy import latex, pi, sin, asin, Integral, Matrix, Rational
from sympy.abc import x, y, N, mu, r, tau

DEBUGG = False

x1 = [1,[], "x1"]
x2 = [1,[], "x2"]
y1 = [1,[], "y1"]
y2 = [1,[], "y2"]
N = [1,[], "N"]

x = [1,[], "x"]
y = [1,[], "y"]

class genCirc:
	def __init__(self):
		pass
		# print ("XOR PLUS")
		# #print ((Ie(x,y))[0])
		# print (If(x,y))
		# print ((E_plus(x,y))[2],"\n\n")

		# print ((D_plus(x,y))[1])
		# print ((D_plus(x,y))[2])


		# print ("\nXOR TIMES")
		# #print ((Ie(x,y))[0])
		# print ((E_times(x,y))[1])
		# print ((E_times(x,y))[2], "\n\n")

		# print ((D_times(x,y))[1])
		# print ((D_times(x,y))[2])


		# result = S(N(x),N(y))
		# print ("E")
		# #print ((Ie(x,y))[0])
		# print ((Ie(x,y))[1])
		# print ((Ie(x,y))[2])

		# #print ((Je(x,y))[0])
		# print ((Je(x,y))[1])
		# print ((Je(x,y))[2])

		# print ("F")
		# #print ((If(x,y))[0])
		# print ((If(x,y))[1])
		# print ((If(x,y))[2])

		# #print ((Jf(x,y))[0])
		# print ((Jf(x,y))[1])
		# print ((Jf(x,y))[2])

		# print ("S")
		# #print ((Is(x,y))[0])
		# print ((Is(x,y))[1])
		# print ((Is(x,y))[2])

		# #print ((Js(x,y))[0])
		# print ((Js(x,y))[1])
		# print ((Js(x,y))[2])

		# print ("T")
		# #print ((It(x,y))[0])
		# print ((It(x,y))[1])
		# print ((It(x,y))[2])

		# #print ((Jt(x,y))[0])
		# print ((Jt(x,y))[1])
		# print ((Jt(x,y))[2])
		

		# print ((E_plus(x,y))[1])
		# print ((E_plus(x,y))[2])
		# print ((E_times(x,y))[1])
		# print ((E_times(x,y))[2])
		# print ((D_plus(x,y))[1])
		# print ((D_plus(x,y))[2])
		# print ((D_times(x,y))[1])
		# print ((D_times(x,y))[2])
		# print ((If(x,y))[1])
		# print ((If(x,y))[2])
		# print ((Is(x,y))[1])
		# print ((Is(x,y))[2])
		# print ((Jf(x,y))[1])
		# print ((Jf(x,y))[2])
		# print ((Js(x,y))[1])
		# print ((Js(x,y))[2])

def T(x, y):
	if (DEBUGG):
		print ("T ", x, " ", y)
	#if not seq:
	a1 = x[0]
	a2 = a1 + y[0]
	s = a2 + 1
	
	nl = []
		
	for c in y[1]:
		partes = c.split(',')
		nc = partes[0]
		partes = partes[1:]
		for p in partes:
			np = str(int(p) + a1)
			nc += "," + np
		nl.append(nc)
	
	c = "t," + str(a1) + "," + str(a2) + "," + str(s)
		
	nl = x[1] + nl + [c]

	le = x[2] + "," + y[2] + ",0"
	
	return [s, nl, le]

def N(x):
	if (DEBUGG):
		print ("N ", x)
	
	l = x[1]
	nc = "p," + str(x[0])
	
	if l!=[]:
		if l[len(l)-1] == nc:
			l = l[0:(len(l)-1)]
		else:
			l = x[1] +[nc]
	else:
		l = x[1] +[nc]
	
	return [x[0],l, x[2]]
	
def S(x,y):
	return N(T(N(x),N(y)))

def E_plus(x,y):
	return S(T(N(x),y),T(x,N(y)))

def E_minus(x,y):
	lc1 = N(T(N(x),N(y)))

	c1 = str(x[0])
	c2 = str(x[0]+y[0])
	a1 = str(lc1[0] + 1)
	a2 = str(lc1[0]+2)
	t1 = "t," + c1 + "," + c2 + "," + a1

	t2 = "t," + str(lc1[0]) + "," + a1 + "," + a2

	lc2 = ["p," + c1, "p," + c2, t1, "p,"+ a1, t2]

	lc = [lc1[0]+2, lc1[1] + lc2, lc1[2] + ",0,0"]

	return lc

def D_minus(x,y):
	lc1 = N(T(x,y))

	c1 = str(x[0])
	c2 = str(x[0]+y[0])
	a1 = str(lc1[0] + 1)
	a2 = str(lc1[0] + 2)
	t1 = "t," + c1 + "," + c2 + "," + a1

	t2 = "t," + str(lc1[0]) + "," + a1 + "," + a2

	lc2 = ["p," + c1, "p," + c2, t1, "p," + a1, t2, "p,"+ a2]

	lc = [lc1[0]+2, lc1[1] + lc2, lc1[2] + ",0,0"]

	return lc
	
def E_times(x,y):
	return T(S(x,y),N(T(x,y)))
	
def D_plus(x,y):
	return T(S(N(x),y),S(x,N(y)))
	
def D_times(x,y):
	return S(T(x,y),N(S(x,y)))

def Ie(x,y):
	return E_minus(x,S(N(x),N(y)))

def Je(x,y):
	return D_minus(x,T(N(x),N(y)))

def If(x,y):
	return E_times(x,N(T(x,y)))
	
def Jf(x,y):
	return D_times(x,N(S(x,y)))

def Is(x,y): 
	return S(N(x),E_plus(N(x),y))

def Js(x,y):
	return T(N(x),D_plus(N(x),y))
	
def It(x,y):
	return E_minus(N(x),T(x,y))

def Jt(x,y):
	return D_minus(N(x),S(x,y))
