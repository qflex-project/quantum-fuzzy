from math import pi as Pi
from math import sqrt as sqrt
from cmath import exp
import numpy
from sympy import *
from sympy.interactive import init_printing
from sympy import latex, pi, sin, asin, Integral, Matrix, Rational
from sympy.abc import x, y, mu, r, tau

class Interpretador:
	def __init__(self):
		init_printing(order = 'grlex')

		self.VARS = ["x","y"]
		self.MAX = 5

		self.TAM = 1
		for i in self.VARS:
			self.TAM *= self.MAX
		self.TAM += 1

		self.operadores = {}

		self.operadores["E+"] = "S(T(N(x),y),T(x,N(y)))"
		self.operadores["Ex"] = "T(S(x,y),N(T(x,y)))"
		self.operadores["D+"] = "T(S(N(x),y),S(x,N(y)))"
		self.operadores["Dx"] = "S(T(x,y),N(S(x,y)))"

		self.operadores["Ie"] = "E-(x,S(N(x),N(y)))"
		self.operadores["Je"] = "D-(x,T(N(x),N(y)))"

		self.operadores["If"] = "E*(x,N(T(x,y)))"
		self.operadores["Jf"] = "D*(x,N(S(x,y)))"

		self.operadores["Is"] = "S(N(x),E+(N(x),y))"
		self.operadores["Js"] = "T(N(x),D+(N(x),y))"

		self.operadores["It"] = "E-(N(x),T(x,y))"
		self.operadores["Jt"] = "D-(N(x),S(x,y))"

	def parseOperator(self, string):
		op = self.operadores[string]
		if op == None:
			return {}
		
		expressions = self.parserExp(op)
		for exp in expressions:
			print (exp, "\t", expressions[exp])

	def parserExp(self, string, values = None):
		baseExp = self.parserString(string)
		exp = baseExp

		if values != None:
			exp = exp.replace("x", values[0])
			exp = exp.replace("y", values[1])

		expanded = expand(exp)
		lat = latex(expanded)

		lat2 = lat.replace("x", "f_A(x)")
		lat2 = lat2.replace("y", "f_B(x)")

		return { "normal": exp, "expand": expanded, "latex1": lat, "latex2": lat2}

	def parserString(self, string):
		if (len(string) == 1):
			return string[0]
		if (len(string) == 0):
			return ""

		f = string[0:string.find('(')]
		args = string[(string.find('(')+1):(len(string)-1)]
		arg1 = ""
		arg2 = ""

		if f[0] != 'N':
			count = 0
			i = 0
			while i < len(args):
				if (args[i] == '('):
					count += 1
				elif(args[i] == ')'):
					count -= 1
				elif (args[i] == ',' and count == 0):
					arg1 = args[0:i]
					arg2 = args[(i+1):]
					i = len(args)
				i+=1
		else:
			arg1 = args

		#print (f, " ", arg1, " ", arg2)

		return self.func(f, self.parserString(arg1), self.parserString(arg2))
		

	def func(self, f, x, y):
		#print (f, " ", x, " ", y)
		exp = ""

		if f[0] == 'N':
			exp = "(1-x)"
		elif f[0] == 'T':
			exp = "x*y"
		elif f[0] == 'S':
			exp = "(x+y-x*y)"
		elif f[0] == 'E':
			if f[1] == '-':
				exp = "(x+y-2*x*y)"
			elif f[1] == '+':
				exp = "(x+y-3*x*y+x*y^2+x^2*y-x^2*y^2)"
			elif f[1] == '*':
				exp = "(x+y-x*y-x*y^2-x^2*y+x^2*y^2)"
			else:
				print ("Argumento Invalido")
		elif f[0] == 'D':
			if f[1] == '-':
				exp = "(1-x-y+2*x*y)"
			elif f[1] == '+':
				exp = "(1-x-y+3*x*y-x*y^2-x^2*y+x^2*y^2)"
			elif f[1] == '*':
				exp = "(1-x-y+x*y+x*y^2+x^2*y-x^2*y^2)"
			else:
				print ("Argumento Invalido")

		else:
			print ("Argumento Invalido")

		exp = self.replaceXY(exp, x, y)
		
		return exp

	def replaceXY(self, exp, x ,y):
		i = 0
		tx = len(x)
		ty = len(y)

		while i < len(exp):
			d = 1
			if exp[i] == 'x':
				exp = exp[0:i] + x + exp[i+1:len(exp)]
				d = tx
			elif exp[i] == 'y':
				exp = exp[0:i] + y + exp[i+1:len(exp)]
				d = ty
			i += d

		return exp
