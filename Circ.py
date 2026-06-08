# COMANDO: python runCirc.py PORTA
# python runCirc.py AND

from math import pi as Pi
from math import sqrt as sqrt
from math import floor
from cmath import exp
import genCirc
import numpy
import re as regex
 
from sympy import *
from sympy.interactive import init_printing
from sympy import latex, pi, sin, asin, Integral, Matrix, Rational
from sympy.abc import x, y, N, mu, r, tau

from genCirc import x1 as x1
from genCirc import y1 as y1
from genCirc import N as N

"""
#
# ---Comandos--- ("Identifcador","paramentro 1", ...,"paramentro n")      #Nao existe espacos
	
# 	PauliX
# Identifcador: 	p
# Parametros:		qubit da operacao
# Exemplo:		p,3			--Aplica a transformacao PauliX no qubit 3

# 	PauliZ
# Identifcador: 	z
# Parametros:		qubit da operacao
# Exemplo:		z,3			--Aplica a transformacao PauliZ no qubit 3


# 	C-Not 
# Identifcador:	c
# Parametros:		primeiro qubit de controle, segundo qubit alvo
# Exemplo:		c,4,5		--Aplica a Toffoli tendo como controle o qubit 4 e como alvo o qubit 5


# 	Toffoli 
# Identifcador:	t
# Parametros:		primeiro qubit de controle, segundo qubit de controle, qubit alvo
# Exemplo:		t,4,5,6		--Aplica a Toffoli tendo como controle os qubits 3 e 4, e como alvo o qubit 6

# 	Measure1 (medida de um qubit)
# Indetificador:	m
# Parametros:		qubit a ser medido, valor em que sera medido (1 ou 0)
# Exemplo:		m,7,1		--Mede o qubit 7 com valor 1

# 	Measure2 (medida de multiplos qubits)
# Indetificador:	m2
# Parametros:		qubits a serem medidos
# Exemplo:		m,5,6		--Mede o qubit 5 e o 6 ao mesmo tempo


# 	Prints
# Indetificador:	pr
# Parametros:		tipo de print a ser feito(pos, pr, m)
# 					pos - printa as posicoes nao nulas apos as operacoes que foram realizadas ate o momento
# 					pv 	- printa as posicoes nao nulas e seus valores
# 					m 	- printa a equacao da ultima medida feita (colocar no wolfram alpha para melhor visualizacao)
# Exemplo:		pr,m 		-- Printa a equacao da ultima medida realizada

# ---FIM COMANDOS---

# ---Como montar um lista de comandos---

# comandos = ["Comando 1","Comando 2, ...,"Comandos n"]		--- lista com n comandos (nao existe espaco entre os comandos e a virgula)

# Exemplo:

# xor_tsn = ["p,1", "p,2", "t,1,2,3", "t,4,5,6", "p,3", "p,6", "t,3,6,7", "m,7,1", "pr,pv","pr,m"]
# --- XOR T,S,N sendo executada e ao final eh printado as posicoes nao nulas e seus valores e tbm a equacao da medida do ultimo qubit (7) em 1

#
"""

class Circ:
	def __init__ (self):
		entradaFuzzy = "x,y,0"
		self.fuzzy["AND"] = [3, ["pr,pv", "pr,pos", "t,1,2,3", "pr,pos", "m2,3"], entradaFuzzy]
		self.fuzzy["OR"] = [3, ["pr,pv", "p,1", "p,2", "pr,pos", "t,1,2,3", "p,3", "pr,pos", "m2,3"], entradaFuzzy]
		self.fuzzy["DIF"] = [3, ["pr,pv", "p,2", "pr,pos", "t,1,2,3", "p,2", "pr,pos", "m2,3"], entradaFuzzy]
		self.fuzzy["CoDIF"] = [3, ["pr,pv", "p,1", "pr,pos", "t,1,2,3", "p,1", "p,3", "pr,pos", "m2,3"], entradaFuzzy]
		self.fuzzy["IMPsn"] = [3, ["pr,pv", "p,2", "pr,pos", "t,1,2,3", "p,2", "p,3", "pr,pos", "m2,3"], entradaFuzzy]
		self.fuzzy["CoIMPsn"] = [3, ["pr,pv", "p,1", "pr,pos", "t,1,2,3", "p,1", "pr,pos", "m2,3"], entradaFuzzy]
		self.fuzzy["Possibility"] = [3, ["pr,pv", "pr,pos", "p,2", "pr,pos", "t,1,2,3", "pr,pos", "m2,3"], entradaFuzzy]
		
		entradaImp = "x,x,y,0,0"
		self.fuzzy["IMPql"] = [5, ["pr,pv", "pr,pos", "t,2,3,4", "p,4", "pr,pos", "t1,4,5", "p,5", "pr,pos", "m2,5"], entradaImp]
		self.fuzzy["CoIMPql"] = [5, ["pr,pv", "pr,pos", "p,1", "p,2", "p,3" "t,2,3,4", "p,2", "p,3", "p,4", "pr,pos", "t1,4,5", "p,1", "p,5", "pr,pos", "m2,5"], entradaImp]

		entradaXorMenos = "x,y,0,0,0"
		self.fuzzy["E-"] = [5, ["pr,pv", "pr,pos", "p,1", "t,1,2,3" ,"p,1", "pr,pos", "p,2", "t,1,2,4", "p,2", "pr,pos", "p,3", "p,4", "t,3,4,5", "p,3", "p,4", "p,5" "pr,pos", "m2,5"], entradaXorMenos]
		self.fuzzy["D-"] = [5, ["pr,pv", "pr,pos", "p,2", "t,1,2,3" ,"p,2", "p,3", "pr,pos", "p,1", "t,1,2,4", "p,1", "p,4" "pr,pos", "t,3,4,5", "pr,pos", "m2,5"], entradaXorMenos]

		entradaDuplicada = "x,y,x,y"
		self.fuzzy["E+"] = [7, ["pr,pv", "pr,pos", "p,1", "t,1,2,5", "p,1", "pr,pos", "p,4", "t,3,4,6", "p,4", "pr,pos", "p,5", "p,6", "t,5,6,7", "p,5", "p,6", "p,7", "pr,pos", "m2,7"], entradaDuplicada]
		self.fuzzy["D+"] = [7, ["pr,pv", "pr,pos", "p,2", "t,1,2,5", "p,2", "p,5", "pr,pos", "p,3", "t,3,4,6", "p,3", "p,6", "pr,pos", "t,5,6,7", "pr,pos", "m2,7"], entradaDuplicada]
		self.fuzzy["Ex"] = [7, ["pr,pv", "p,1", "p,2", "t,1,2,5", "p,1", "p,2", "p,5", "t,3,4,6", "p,6", "t,5,6,7", "pr,pos", "m2,7"], entradaDuplicada]
		self.fuzzy["Dx"] = [7, ["pr,pv", "t,1,2,5", "pr,pos", "p,3", "p,4", "t,3,4,6", "p,3", "p,4", "pr,pos", "p,5", "p,6", "t,5,6,7", "p5", "p,6", "p,7", "pr,pos", "m2,7"], entradaDuplicada]
		self.fuzzy["eXorCoIMP-"] = [8, ["pr,pv", "t,1,2,4", "p,3", "p,4", "pr,pos", "t,3,4,5", "p,3", "t,1,2,6", "pr,pos", "t,3,6,7", "p,5", "p,7", "pr,pos", "t,5,7,8", "p,8" , "pr,pos", "m2,7"], entradaDuplicada]
		
		entradaFuzzySquare = "x,x,y,y"
		self.fuzzy["AND"] = [7, ["pr,pv", "pr,pos", "t,1,2,5", "pr,pos", "t,3,4,6", "pr,pos", "t,5,6,7", "pr,pos", "m2,7"], entradaFuzzySquare]
		self.fuzzy["OR"] = [7, ["pr,pv", "pr,pos", "t,1,2,5", "pr,pos", "t,3,4,6", "p,5", "p,6", "pr,pos", "t,5,6,7", "p,5", "p,6", "p,7", "pr,pos", "m2,7"], entradaFuzzySquare]
		self.fuzzy["IMPgn"] = [7, ["pr,pv", "pr,pos", "t,1,2,5", "pr,pos", "p,3", "p,4", "t,3,4,6", "p,3", "p,4", "pr,pos", "t,5,6,7", "p,7", "pr,pos", "m2,7"], entradaFuzzySquare]
		self.fuzzy["COIMPgn"] = [7, ["pr,pv", "pr,pos", "p,1", "p,2", "t,1,2,5", "p,1", "p,2", "pr,pos", "t,3,4,6", "pr,pos", "t,5,6,7", "pr,pos", "m2,7"], entradaFuzzySquare]
		self.fuzzy["Overlap"] = [7, ["pr,pv", "t,1,2,5", "pr,pos", "t,3,4,6", "pr,pos", "t,5,6,7", "pr,pos", "m2,7"], entradaFuzzySquare]
		self.fuzzy["Grouping"] = [7, ["pr,pv", "p,1", "p,2", "t,1,2,5", "p,1", "p,2", "pr,pos", "p,3", "p,4","t,3,4,6", "p,3", "p,4", "pr,pos", "t,5,6,7", "pr,pos", "p,7", "pr,pos", "m2,7"], entradaFuzzySquare]
		self.fuzzy["EGroupingOverlap"] = [11, ["pr,pv", "p,1", "p,2", "t,1,2,5", "p,1", "p,2", "p,3", "p,4", "t,3,4,6", "p,3", "p,4", "t,5,6,7", "p,7", "pr,pos", "t,1,2,8", "t,3,4,9", "t,8,9,10", "pr,pos", "p,10", "t,7,10,11", "pr,pos", "m2,11"], entradaFuzzySquare]
		self.fuzzy["DGroupingOverlap"] = [11, ["pr,pv", "t,1,2,5", "t,3,4,6", "t,5,6,7", "p,7", "pr,pos", "p,1", "p,2", "p,3", "p,4", "t,1,2,8", "t,3,4,9", "t,8,9,10" , "p,1", "p,2", "p,3", "p,4","pr,pos", "p,10", "t,7,10,11", "p,11", "pr,pos", "m2,11"], entradaFuzzySquare]

		entradaIMPGNO = "x,x,x,x,y,y"
		self.fuzzy["IMPqlGNO"] = [11, ["pr,pv", "pr,pos", "t,1,2,7" , "t,3,4,8" , "t,5,6,9" , "t,8,9,10" , "t,7,10,11", "pr,pos", "m2,11"], entradaIMPGNO]
		self.fuzzy["CoIMPqlGNO"] = [11, ["pr,pv", "pr,pos", "p,1", "p,2", "t,1,2,7", "p,1", "p,2", "p,3", "p,4", "t,3,4,8", "p,3", "p,4", "p,5", "p,6",  "t,5,6,9", "p,5", "p,6", "t,8,9,10" , "p,10", "t,7,10,11", "pr,pos", "m2,11"], entradaIMPGNO]

		#circuitos fuzzy intucionista
		entradaIntucionista = "x1,x2,y1,y2"
		self.intFuzzy["AND"]	= [6, ["pr,pv", "t,1,3,5", "pr,pos", "p,2", "p,4", "t,2,4,6", "p,2", "p,4", "p,6", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["OR"]		= [6, ["pr,pv", "p,1", "p,3", "pr,pos", "t,1,3,5", "pr,pos", "p,1", "p,3", "p,5", "pr,pos", "t,2,4,6", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["IMP"]	= [6, ["pr,pv", "p,2", "p,3", "pr,pos", "t,2,3,5", "pr,pos", "p,2", "p,3", "p,5", "pr,pos", "t,1,4,6", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["COIMP"]	= [6, ["pr,pv", "t,2,3,5", "pr,pos", "p,1", "p,4", "pr,pos", "t,1,4,6", "pr,pos", "p,1", "p,4", "p,6", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["DIF"]	= [6, ["pr,pv", "t,1,4,5", "pr,pos", "p,2", "p,3", "pr,pos", "t,2,3,6", "pr,pos", "p,2", "p,3", "p,6", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["CODIF"] 	= [6, ["pr,pv", "p,1", "p,4", "pr,pos", "t,1,4,5", "pr,pos", "p,1", "p,4", "p,5", "pr,pos", "t,2,3,6", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["BI_IMP"]	= [10, ["pr,pv", "p,2", "p,3", "t,2,3,5", "p,2", "p,3", "p,5", "pr,pos", "p,1", "p,4", "t,1,4,6", "p,1", "p,4", "p,6", "pr,pos", "t,5,6,9", "pr,pos", "t,1,4,7", "p,7", "pr,pos", "t,2,3,8", "p,8", "pr,pos", "t,7,8,10", "p,10", "pr,pos", "m2,9", "m2,10"], entradaIntucionista]
		self.intFuzzy["E+"] 	= [8, ["pr,pv", "t,2,3,7", "pr,pos", "t,1,4,8", "pr,pos", "p,7", "p,8", "t,7,8,5", "p,7", "p,8", "p,5", "pr,pos", "t,1,4,8", "pr,pos", "t,2,3,7", "pr,pos", "p,2", "p,3", "t,2,3,7", "p,2", "p,3", "p,7", "pr,pos", "p,1", "p,4", "t,1,4,8", "p,1", "p,4", "p,8", "pr,pos", "t,7,8,6", "pr,pos", "p,1", "p,4", "p,8", "t,1,4,8", "p,1", "p,4", "pr,pos", "p,2", "p,3", "p,7", "t,2,3,7", "p,2", "p,3", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["Ex"] 	= [8, ["pr,pv","p,1", "p,3", "t,1,3,7", "p,1", "p,3", "p,7", "pr,pos", "p,2", "p,4", "t,2,4,8", "p,2", "p,4", "p,8", "pr,pos", "t,7,8,5", "pr,pos", "p,2", "p,4", "p,8", "t,2,4,8","p,2", "p,4", "pr,pos", "p,1", "p,3", "p,7", "t,1,3,7", "p,1", "p,3", "pr,pos", "t,2,4,7", "pr,pos", "t,1,3,8", "pr,pos", "p,7", "p,8", "t,7,8,6", "p,6", "p,7", "p,8", "pr,pos", "t,1,3,8", "pr,pos", "t,2,4,7", "pr,pos", "m2,5", "m2,6"], entradaIntucionista]
		self.intFuzzy["X+"] 	= [10, ["pr,pv", "t,2,3,5", "pr,pos", "t,1,4,6", "pr,pos", "p,5", "p,6", "t,5,6,9", "p,5", "p,6", "p,9", "pr,pos", "p,1", "p,4", "t,1,4,7", "p,1", "p,4", "p,7", "pr,pos", "p,2", "p,3", "t,2,3,8", "p,2", "p,3", "p,8", "pr,pos", "t,7,8,10", "pr,pos", "m,9,1", "pr,m", "m,10,1", "pr,m"], entradaIntucionista]
		self.intFuzzy["Xx"] 	= [10, ["pr,pv", "p,1", "p,3", "t,1,3,5", "p,1", "p,3", "p,5", "pr,pos", "p,2", "p,4", "t,2,4,6", "p,2", "p,4", "p,6", "pr,pos", "t,5,6,9", "pr,pos", "t,2,4,7", "pr,pos", "t,1,3,8", "pr,pos", "p,7", "p,8", "t,7,8,10","p,7", "p,8", "p,10", "pr,pos", "m,9,1", "pr,m", "m,10,1", "pr,m"], entradaIntucionista]
	
	# executa um circuito fuzzy
	def executeFuzzyCirc(self, operator):
		circ = self.fuzzy.get(operator)
		if circ == None:
			print ("Operador não encontrado", operator)
			return
		
		self.executeCirc(circ)
	
	# executa um circuito fuzzy com entradas ao quadrado
	def executeFuzzySquareCirc(self, operator):
		circ = self.fuzzySquare.get(operator)
		if circ == None:
			print ("Operador não encontrado", operator)
			return
		
		self.executeCirc(circ)
	
	# executa um circuito fuzzy intucionista
	def executeIntFuzzyCirc(self, operator):
		circ = self.intFuzzy.get(operator)
		if circ == None:
			print ("Operador não encontrado", operator)
			return
		
		self.executeCirc(circ)

	def executeCirc(self, circuito):
		m = circuito[0]
		c = circuito[1]
		q = circuito[2].split(",")

		for i in range(len(q), m):
			q.append("0")

		pos = self.parserPos(q, 0)
		val = self.parserVal(q, pos)

		pos = self.execute(pos, val, c)

		ret = self.parserPosVal(pos, val)

	def printMemory(self, values, d , partial):
		partial0 = partial * values[d][0]
		partial1 = partial * values[d][1]

		if (d == len(values)-1):
			print (partial0, ", ", partial1, ", ",)
		else:
			self.printMemory(values, d+1, partial0)
			self.printMemory(values, d+1, partial1)

	def printPos(self, positions):
		#print(positions)
		for p in positions:
			print (("".join(p)))

	def printPosVal(self, positions, values):
		r = ""
		for p in range (0, len(positions)):
			print (("".join(positions[p])), values[p])
			r += ("".join(positions[p])) + "," +  values[p] + ";"
		return r

	def parserPosVal(self, pos, val):
		l_pv = []
		for p in range (0, len(pos)):
			e = [val[p], "".join(pos[p])]
			l_pv.append(e)

		r = ["","",""]
		l_pv = self.sort(l_pv)

		for pv in l_pv:
			raiz = ""
			norm = ""
			sp = pv[0].split("*")

			for s in sp:
				p = s.split("^")
				if len(p) == 1:
					raiz += "*" + p[0]
				else:
					norm += "*" + p[0]
					exp = int(p[1])/2
					rest = int(p[1])%2
					
					if (exp>1):
						norm += "^" + str(exp)
					if (rest != 0):
						raiz += "*" + p[0]

			e = ""
			if (norm != ""):
				e = norm[1:]
			if (raiz != ""):
				e += "\sqrt{" + raiz[1:] + "}"

			#print(e)
			e = e.replace("*","")
			e = e.replace("x","f_A")
			e = e.replace("y","f_B")
			if 'H' in e:
				e = e.replace("H","\\frac{1}{\sqrt{2}}(")
				ef = " + " + e + ")" + "|" + pv[1] + "\\rangle"
				#print(ef)
			else:
				ef = " + " + e + "|" + pv[1] + "\\rangle"

			m = int(pv[1][-1])
			r[m] += " + " + e
			r[2] += ef

		return r[0][3:] , r[1][3:], r[2][3:]

	def sort(self, l_pv):
		ret = []
		while len(l_pv) != 0:
			i = 0
			menor = 0
			for pv in l_pv:
				if (int(pv[1]) < int(l_pv[menor][1])):
					menor = i
				i+=1
			n = l_pv[menor]
			ret.append(n)
			l_pv = l_pv[0:menor] + l_pv[(menor+1):len(l_pv)]

		return ret		

	def parserPos(self, f, d):
		pos = []
		v = f[d]

		if (d == len(f) - 1):
			if v == "0":
				pos.append("0")
			elif v == "1":
				pos.append("1")
			else:
				pos.append("0")
				pos.append("1")

		else:
			res = self.parserPos(f, d+1)
			t = []
			if v == "0":
				t.append("0")
			elif v == "1":
				t.append("1")
			else:
				t.append("0")
				t.append("1")

			for p in t:
				for r in res:
					pos.append(p+r)

		if (d == 0):
			temp = pos 
			pos = []
			for p in temp:
				pos.append(list(p))


		return pos

	def parserVal(self, func, pos):
		values = []
		for p in pos:
			v = []
			for i in range(0, len(func)):
				if (func[i] != "0" and func[i] != "1"):
					if (p[i] == "0"):
						v.append("(1-" + func[i] + ")")
					else:
						v.append(func[i])
			values.append(self.ajustaVal(v))

		return values
		
	def ajustaVal(self, value):
		new = ""
		i = 0
		while i < len(value):
			count = 1
			j = i + 1
			while j < len(value):
				if value[i] == value[j]:
					value = value[0:j] + value[(j+1):len(value)]
					count += 1
					j-=1
				j+=1
			new += "*" + value[i]
			if count > 1:
				new += "^" + str(count)
			i+=1
		return new[1:]

	def hadamard(self, positions, values, qubit):
		sqrtvar = 'H'
		for p in range(len(positions)):
			values[p] = str( str(sqrtvar) + values[p] )  # Adicionar "1/2" ao início
		#print(values)
		#print(positions)
		return positions, values

	def pauliX(self, positions, qubit):
		for p in positions:
			if p[qubit] == "0":
				p[qubit] = "1"
			else:
				p[qubit] = "0"

		return positions

	def pauliZ(self, positions, values, qubit):
		for p in range(0, len(positions)):
			if positions[p][qubit] == "1":
				values[p] = "-" + values[p]

		return positions, values

	def cnot(self, positions, control, target):
		for p in positions:
			if p[control] == "1":
				if (p[target] == "0"):
					p[target] = "1"
				else:
					p[target] = "0"

		return positions

	def vGate(self, positions, values, control, target):
		#j = floor((-1)**(1/2))
		j = (-1)**(1/2)
		sqrtvar = [(1+j)/2, (-1+j)/2], [(-1+j)/2, (1+j)/2]
		sqr1 = [(1+j)/2, (-1+j)/2]
		sqr2 = [(-1+j)/2, (1+j)/2]
		
		#Retorna o qubit do alvo
		#for p in range(0, len(positions)):
		#	if positions[p][control] == "1":
		#		print( positions[p][control])
		#		if(positions[p][target] == "1"):
		#			positions[p][target] = str(sqr1)
		#		else:
		#			positions[p][target] = str(sqr2)
  
		#Retorna as amplitudes do qubit alvo
		for p in range(0, len(positions)):
			if positions[p][control] == "1":
					print(positions[p][target])
					print(values[p])
					print(sqrtvar[int(positions[p][target])])
					if(values[p] == "1"):
						values[p] = str((1+j)/2 + (-1+j)/2)
					else:
						values[p] = str((-1+j)/2 + (1+j)/2)
		return positions, values

	def toffoli(self, positions, control1, control2, target):
		for p in positions:
			if p[control1] == "1" and p[control2] == "1":
				if (p[target] == "0"):
					p[target] = "1"
				else:
					p[target] = "0"

		return positions

	def toffoli00(self, positions, control1, control2, target):
		for p in positions:
			if p[control1] == "0" and p[control2] == "0":
				if (p[target] == "0"):
					p[target] = "1"
				else:
					p[target] = "0"

		return positions

	"""
	def toffoli10(self, positions, control1, control2, target):
		for p in positions:
			if p[control1] == "1" and p[control2] == "0":
				if (p[target] == "0"):
					p[target] = "1"
				else:
					p[target] = "0"

		return positions

	def toffoli01(self, positions, control1, control2, target):
		for p in positions:
			if p[control1] == "0" and p[control2] == "1":
				if (p[target] == "0"):
					p[target] = "1"
				else:
					p[target] = "0"

		return positions
	"""

	def measure(self, positions, values, qubit, v):
		if v == 1:
			v = "1"
		elif v == 0:
			v = "0"

		m = ""
		for p in range (0, len(positions)):
			if (positions[p][qubit] == v):
				m += "+" + values[p]
		m = m[1:]
		return m

	def measure2(self, positions, values, qubits):
		m = []
		for i in range(0,len(qubits)):
			qubits[i] = int(qubits[i])

		for i in range(0, pow(2,len(qubits))):
			m.append("")

		if 'H' in values:
			values = values.replace("H","1/√2")

		for p in range (0, len(positions)):
			pos = 0
			for q in qubits:

				pos = pos * 2 + int(positions[p][q-1])
			
			m[pos] += "+" + values[p]

		for i in range(0, pow(2,len(qubits))):
			m[i] = m[i][1:]

		return m

	def execute(self, pos, val, commands):
		b = 1
		m = ""
		for c in commands:
			#print (c)
			par = c.split(',')

			if par[0] == "h":
				pos, val = self.hadamard(pos, val, int(par[1])-b)
			elif par[0] == "p":
				pos = self.pauliX(pos, int(par[1])-b)
			elif par[0] == "z":
				pos, val = self.pauliZ(pos, val, int(par[1])-b)			
			elif par[0] == "c":
				pos = self.cnot(pos, int(par[1])-b, int(par[2])-b)
			elif par[0] == "t":
				pos = self.toffoli(pos, int(par[1])-b, int(par[2])-b, int(par[3])-b)
			elif par[0] == "t00":
				pos = self.toffoli00(pos, int(par[1])-b, int(par[2])-b, int(par[3])-b)
			elif par[0] == "vGate":
				pos, val = self.vGate(pos, val, int(par[1])-b, int(par[2])-b)
			elif par[0] == "m":
				m = self.measure(pos, val, int(par[1])-b, int(par[2]))
			elif par[0] == "m2":
				print ("M :", par[1:] )
				m2 = self.measure2(pos, val, par[1:])
				form = "{0:0" + str(len(par)-1) + "b}"
				for q in range(0,len(m2)):
					if m2[q] != "":
						print (form.format(q), ":", expand(m2[q]))
						print (form.format(q), ":", factor(m2[q]))
				print ("\n########\n")
			elif par[0] == "pr":
				if par[1] == "m":
					#print (m)
					print (expand(m))
					print ("\n########\n")
				elif par[1] == "pos":
					self.printPos(pos)
					print ("\n########\n")
				elif par[1] == "pv":
					pv = self.printPosVal(pos, val)
					#print (pv)
					print ("\n########\n")
		return pos

	# gera um circuito fuzzy em latex
	def toLatexCircFuzzy(self, operator):
		circ = self.fuzzy.get(operator)
		if circ == None:
			print ("Operador não encontrado", operator)
			return None
		
		return self.toLatexCirc(circ)
	
	# gera um circuito fuzzy intucionista em latex
	def toLatexCircIntFuzzy(self, operator):
		circ = self.intFuzzy.get(operator)
		if circ == None:
			print ("Operador não encontrado", operator)
			return
		
		return self.toLatexCirc(circ)

	# converte um circuito para formato latex
	def toLatexCirc(self, circ):
		qubits = circ[0]
		latexCirc = self.toLatex(circ[1])
		latexCirc = latexCirc.replace("\\tof", "T")

		expr = reversed(latexCirc.split(" \circ "))

		var = circ[2].split(",")

		l = [0]*qubits

		col = 0
		y = 0.75
		x = 1.3

		output = '''\\centerline{
\\begin{tikzpicture}[thick]
\\tikzstyle{operator} = [draw,fill=white,minimum size=1.4em]
\\tikzstyle{bullet} = [fill,shape=circle,minimum size=5pt,inner sep=0pt]
\\tikzset{XOR/.style={draw,circle,append after command={
\t\t\t[shorten >=\pgflinewidth, shorten <=\pgflinewidth,]
\t\t\t(\\tikzlastnode.north) edge (\\tikzlastnode.south)
\t\t\t(\\tikzlastnode.east) edge (\\tikzlastnode.west)
\t\t}
\t}
}
\\tikzstyle{surround} = [fill=blue!10,thick,draw=black,rounded corners=2mm]'''

		output = output + "\n\n% Qubits"
		for i in range(0, qubits):
			value = "0"
			if i < len(var):
				value = var[i]
			output = output + "\n\\node at (0,{})\t(q{}_{})\t{{$\\lvert {} \\rangle$}};".format(y*(-i), i+1, col, value)

		col += 1
		for c in expr:
			op = c[0]
			temp = regex.findall(r'\d+', c)
			arg = list(map(int, temp))
			
			if op == "N":
				output = output + "\n% Column {}".format(col)
				for idx in arg:
					output = output + "\n\\node[operator] (q{}_{}) at ({},{}) {{X}} edge [-] (q{}_{});".format(idx, col, col*x, y*(-(idx-1)), idx, l[idx-1])
					l[idx-1] = col
				col+=1

			if op == "h":
				output = output + "\n% Column {}".format(col)
				for idx in arg:
					output = output + "\n\\node[operator] (q{}_{}) at ({},{}) {{H}} edge [-] (q{}_{});".format(idx, col, col*x, y*(-(idx-1)), idx, l[idx-1])
					l[idx-1] = col
				col+=1

			if op == "T":
				output = output + "\n% Column {}".format(col)

				idx1, idx2, idx3 = arg[0], arg[1], arg[2]

				output = output + "\n\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx1, col, col*x, y*(-(idx1-1)), idx1, l[idx1-1])
				l[idx1-1] = col
				output = output + "\n\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx2, col, col*x, y*(-(idx2-1)), idx2, l[idx2-1])
				l[idx2-1] = col
				output = output + "\n\\node[XOR]    (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx3, col, col*x, y*(-(idx3-1)), idx3, l[idx3-1])
				l[idx3-1] = col

				output = output + "\n\\draw[-]      (q{}_{}) -- (q{}_{});".format(idx1, col, idx2, col)
				output = output + "\n\\draw[-]      (q{}_{}) -- (q{}_{});".format(idx2, col, idx3, col)

				col+=1

			if op == "c":
				output = output + "\n% Column {}".format(col)

				idx1, idx2 = arg[0], arg[1]

				output = output + "\n\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx1, col, col*x, y*(-(idx1-1)), idx1, l[idx1-1])
				l[idx1-1] = col
				output = output + "\n\\node[XOR]    (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx2, col, col*x, y*(-(idx2-1)), idx2, l[idx2-1])
				l[idx2-1] = col

				output = output + "\n\\draw[-]      (q{}_{}) -- (q{}_{});".format(idx1, col, idx2, col)

				col+=1
			if op == "vGate":
				output = output + "\n% Column {}".format(col)

				idx1, idx2 = arg[0], arg[1]

				output = output + "\n\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx1, col, col*x, y*(-(idx1-1)), idx1, l[idx1-1])
				l[idx1-1] = col
				output = output + "\n\\node[V]    (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(idx2, col, col*x, y*(-(idx2-1)), idx2, l[idx2-1])
				l[idx2-1] = col

				output = output + "\n\\draw[-]      (q{}_{}) -- (q{}_{});".format(idx1, col, idx2, col)

				col+=1

		#\draw[dashed] (2.25,0.25) -- (2.25,-7);
		#\node at (2.25,-7.25) {\footnotesize{T1}};

		output = output + "\n%"
		for q in range (0, len(l)):
			i = l[q]
			output = output + "\n\\node[] at ({},{}) {{}} edge [-] (q{}_{});".format(col*x-x/2, y*(-q), q+1, i)
		output = output + "\n%"

		output = output + "\n\\node at ({},{}) {{\\footnotesize{{T{}}}}};".format(0, y, 0)
		for t in range(1, col):
			output = output + "\n\\draw[dashed] ({},{}) -- ({},{});".format(x*t - x/2, y/2, x*t - x/2, -y*len(l) + y/2)
			output = output + "\n\\node at ({},{}) {{\\footnotesize{{T{}}}}};".format(x*t, y, t)
		output = output + "\n%"

#		print ("\\draw[dashed] ({},{}) -- ({},{});".format(x*col - x/2, y/2, x*col - x/2, -y*len(l) + y/2))
#		print ("\\node at ({},{}) {{\\footnotesize{{T{}}}}};".format(x*col - x/2, -y*len(l)+ y/4, col-1))

		output = output + "\n\\end{tikzpicture}"
		output = output + "\n}"

		return output

	def toLatex(self, expr):
		formula = []
		n_list = []

		#print(expr)
		for c in expr:
			s = c.split(',')
			#print(s)
			if s[0] == "p":
				n_list.append(s[1])
			elif len(n_list) > 0:
				j = ",".join(sorted(n_list))
				formula.append("N_{"+j+"}")
				n_list = []
			if s[0] == "t":
				j = ",".join(s[1:3])
				formula.append("\\tof^{"+j+"}_{"+ s[3]+"}")
			if s[0] == "h":
				j = ",".join(s[1])
				formula.append("h_{"+j+"}")
			if s[0] == "c":
				j = ",".join(s[1])
				formula.append("c^{"+j+"}_{"+ s[2]+"}")	
			if s[0] == "vGate":
				j = ",".join(s[1])
				formula.append("V^{"+j+"}_{"+ s[2]+"}")	
			#print(formula)
		
		return (" \circ ".join(reversed(formula)))