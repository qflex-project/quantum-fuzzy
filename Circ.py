from math import pi as Pi
from math import sqrt as sqrt
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
# Parametros:		primeiro qubit de controle, segundo qubit de controle, qubit alvo
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
		#valores iniciais dos qubits
		entrada = "x1,x2,y1,y2,0,0"

		self.fuzzy = {}
		self.intFuzzy = {}

		#teste = [6, ["pr,pv", "t,1,2,3", "p,2", "t,1,2,4", "p,1", "t,1,2,6", "p,2", "t,1,2,5", "p,1", "m2,3", "m2,4", "m2,5", "m2,6"], "(1-x1-x2),(1-y1-y2),0,0,0,0"]
		#teste = [7, ["pr,pv", "t,1,2,3", "p,4", "p,5", "t,4,5,6", "p,4", "p,5", "p,6", "p,3", "t,3,6,7", "m2,3", "m2,6", "m2,7", "m2,7,6", "m2,7,3"], "x1,x2,0,x1,x2,0,0"]
		teste = [6, ["pr,pos", "t,1,3,5", "pr,pos", "p,2", "p,4", "pr,pos", "t,2,4,6", "pr,pos", "p,6", "pr,pos", "m2,5", "m2,6"], entrada]

		AND		= [6, ["pr,pv", "t,1,3,5", "pr,pv", "p,2", "p,4", "t,2,4,6", "p,2", "p,4", "p,6", "pr,pv", "m2,5", "m2,6"], entrada]
		OR		= [6, ["pr,pos", "p,1", "p,3", "pr,pos", "t,1,3,5", "pr,pos", "p,1", "p,3", "p,5", "pr,pos", "t,2,4,6", "pr,pos", "m2,5", "m2,6"], entrada]
		IMP		= [6, ["pr,pos", "p,2", "p,3", "pr,pos", "t,2,3,5", "pr,pos", "p,2", "p,3", "p,5", "pr,pos", "t,1,4,6", "pr,pos", "m2,5", "m2,6"], entrada]
		COIMP	= [6, ["pr,pos", "t,2,3,5", "pr,pos", "p,1", "p,4", "pr,pos", "t,1,4,6", "pr,pos", "p,1", "p,4", "p,6", "pr,pos", "m2,5", "m2,6"], entrada]
		DIF		= [6, ["pr,pos", "t,1,4,5", "pr,pos", "p,2", "p,3", "pr,pos", "t,2,3,6", "pr,pos", "p,2", "p,3", "p,6", "pr,pos", "m2,5", "m2,6"], entrada]
		CODIF 	= [6, ["pr,pos", "p,1", "p,4", "pr,pos", "t,1,4,5", "pr,pos", "p,1", "p,4", "p,5", "pr,pos", "t,2,3,6", "pr,pos", "m2,5", "m2,6"], entrada]

		BI_IMP	= [10, ["pr,pv", "p,2", "p,3", "t,2,3,5", "p,2", "p,3", "p,5", "pr,pos", "p,1", "p,4", "t,1,4,6", "p,1", "p,4", "p,6", "pr,pos", "t,5,6,9", "pr,pos", "t,1,4,7", "p,7", "pr,pos", "t,2,3,8", "p,8", "pr,pos", "t,7,8,10", "p,10", "pr,pos", "m2,9", "m2,10"], "x1,x2,y1,y2,0,0,0,0,0,0"]
		
		E_PLUS	= [7, ["p,1", "t,1,2,5", "p,1", "p,2", "t,1,2,6", "p,2", "p,5", "p,6", "t,5,6,7", "p,5","p,6","p,7","m2,5","m2,6","m2,7"], "x,y,x,y,0,0,0"]
		#E_INT_PLUS = [14, ["t,2,5,9", "t,3,8,10", "p,9","p,10", "t,9,10,11", "p,9","p,10","p,11", "t,1,6,12", "p,4", "p,7", "t,4,7,13", "p,4", "p,7", "p,13", "t,12,13,14", "m2,11", "m2,14"], "x1,x2,x1,x2,y1,y2,y1,y2,0,0,0,0,0,0"]

		E_INT_PLUS = [8, ["t,2,3,7", "pr,pv", "t,1,4,8", "pr,pv", "p,7", "p,8", "t,7,8,5", "p,7", "p,8", "p,5", "pr,pv", "t,1,4,8", "pr,pv", "t,2,3,7", "pr,pv", "p,2", "p,3", "t,2,3,7", "p,2", "p,3", "p,7", "pr,pv", "p,1", "p,4", "t,1,4,8", "p,1", "p,4", "p,8", "pr,pv", "t,7,8,6", "pr,pv", "p,1", "p,4", "p,8", "t,1,4,8", "p,1", "p,4", "pr,pv", "p,2", "p,3", "p,7", "t,2,3,7", "p,2", "p,3", "pr,pv", "m2,5", "m2,6"], "x1,x2,y1,y2,0,0,0,0"]
		
		E_INT_PLUS_2 = [8, ["pr,pv", "t,2,3,7", "t,1,4,8", "pr,pv", "p,7", "p,8", "t,7,8,5", "p,7", "p,8", "p,5", "pr,pv", "t,1,4,8", "t,2,3,7", "pr,pv", "p,2", "p,3", "t,2,3,7", "p,2", "p,3", "p,7", "p,1", "p,4", "t,1,4,8", "p,1", "p,4", "p,8", "pr,pv", "t,7,8,6", "pr,pv", "p,1", "p,4", "p,8", "t,1,4,8", "p,1", "p,4", "p,2", "p,3", "p,7", "t,2,3,7", "p,2", "p,3", "pr,pv", "m2,5", "m2,6"], "x1,x2,y1,y2,0,0,0,0"]

		E_INT_TIMES = [8, ["pr,pv","p,1", "p,3", "t,1,3,7", "p,1", "p,3", "p,7", "pr,pv", "p,2", "p,4", "t,2,4,8", "p,2", "p,4", "p,8", "pr,pv", "t,7,8,5", "pr,pv", "p,2", "p,4", "p,8", "t,2,4,8","p,2", "p,4", "pr,pv", "p,1", "p,3", "p,7", "t,1,3,7", "p,1", "p,3", "pr,pv", "t,2,4,7", "pr,pv", "t,1,3,8", "pr,pv", "p,7", "p,8", "t,7,8,6", "p,6", "p,7", "p,8", "pr,pv", "t,1,3,8", "pr,pv", "t,2,4,7", "pr,pv", "m2,5", "m2,6"], "x1,x2,y1,y2,0,0,0,0"]

		E_INT_TIMES_2 = [8, ["pr,pv","p,1", "p,3", "t,1,3,7", "p,1", "p,3", "p,7", "p,2", "p,4", "t,2,4,8", "p,2", "p,4", "p,8", "pr,pv", "t,7,8,5", "pr,pv", "p,2", "p,4", "p,8", "t,2,4,8","p,2", "p,4", "p,1", "p,3", "p,7", "t,1,3,7", "p,1", "p,3", "pr,pv", "t,2,4,7", "t,1,3,8", "pr,pv", "p,7", "p,8", "t,7,8,6", "p,6", "p,7", "p,8", "pr,pv", "t,1,3,8", "t,2,4,7", "pr,pv", "m2,5", "m2,6"], "x1,x2,y1,y2,0,0,0,0"]

		OP_FUZZY = [3,["pr,pv", "p,1", "p,2", "pr,pv", "t,1,2,3", "pr,pv", "p,1", "p,2","p,3", "pr,pv", "m2,3"], "x,y,0"]

		XOR_INT_PLUS = [10, ["pr,pv", "t,2,3,5", "pr,pv", "t,1,4,6", "pr,pv", "p,5", "p,6", "t,5,6,9", "p,5", "p,6", "p,9", "pr,pv", "p,1", "p,4", "t,1,4,7", "p,1", "p,4", "p,7", "pr,pv", "p,2", "p,3", "t,2,3,8", "p,2", "p,3", "p,8", "pr,pv", "t,7,8,10", "pr,pv", "m,9,1", "pr,m", "m,10,1", "pr,m"], "x_1,x_2,y_1,y_2,0,0,0,0,0,0"]

		XOR_INT_TIMES = [10, ["pr,pv", "p,1", "p,3", "t,1,3,5", "p,1", "p,3", "p,5", "pr,pv", "p,2", "p,4", "t,2,4,6", "p,2", "p,4", "p,6", "pr,pv", "t,5,6,9", "pr,pv", "t,2,4,7", "pr,pv", "t,1,3,8", "pr,pv", "p,7", "p,8", "t,7,8,10","p,7", "p,8", "p,10", "pr,pv", "m,9,1", "pr,m", "m,10,1", "pr,m"], "x_1,x_2,y_1,y_2,0,0,0,0,0,0"]

		TESTE = [9, ["p,1", "p,3", "t,4,5,6", "t,7,9,8"], "0,0,0,0,0,0,0,0,0"]

		#self.toLatexCirc(XOR_INT_TIMES)

		#self.toLatexCircGeneric(TESTE)

		print (self.executeGen(OP_FUZZY))
		#print (self.toLatex(XOR_INT_TIMES[1]))

	def toLatexCircGeneric(self, circuito):
		circ = [6, [["H,0,1,2,3,4,5"], ["X,0,1,2,3,4,5"],["C,0,1,2,3,4,5"],["X,0,1,2,3,4,5"],["H,0,1,2,3,4,5"]], "0,0,0,0,0,0"]

		qubits = circ[0]
		qts = circ[1]
		var = circ[2].split(",")

		l = [0]*qubits

		col = 0
		y = 1.0
		x = 1.1

		print ("\\centerline{")
		print ("\\begin{tikzpicture}[thick]")
		print ("\\tikzstyle{operator} = [draw,fill=white,minimum size=1.4em]")
		print ("\\tikzstyle{bullet} = [fill,shape=circle,minimum size=5pt,inner sep=0pt]")
		print ("\\tikzset{XOR/.style={draw,circle,append after command={")
		print ("\t\t\t[shorten >=\pgflinewidth, shorten <=\pgflinewidth,]")
		print ("\t\t\t(\\tikzlastnode.north) edge (\\tikzlastnode.south)")
		print ("\t\t\t(\\tikzlastnode.east) edge (\\tikzlastnode.west)")
		print ("\t\t}")
		print ("\t}")
		print ("}")
		print ("\\tikzstyle{surround} = [fill=blue!10,thick,draw=black,rounded corners=2mm]")


		print ("% Qubits")
		for i in range(0, qubits):
			print ("\\node at ({},{})\t(q{}_{})\t{{}};".format(x/2, y*(-i), i+1, col))

		col += 1
		for qt in qts:
			for gate in qt:
				op = gate[0]
				arg = [int(i) for i in gate[2:].split(",")]

				print ("%\n% Column {}".format(col))
				if op != "C":
					for n in arg:
						print ("\\node[operator] (q{}_{}) at ({},{}) {{{}}} edge [-] (q{}_{});".format(n+1, col, col*x, y*(-n), op , n+1, l[n]))
						l[n] = col
				else:
					l_arg = arg[-1]
					arg = arg[:len(arg)-1]
					for a in arg:
						print ("\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(a+1, col, col*x, y*(-a), a+1, l[a]))
						l[a] = col
					
					
					print ("\\node[XOR]    (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(l_arg+1, col, col*x, y*(-l_arg), l_arg+1, l[l_arg]))
					l[l_arg] = col

					for i in range(0, len(arg)-1):
						print ("\\draw[-]      (q{}_{}) -- (q{}_{});".format(arg[i]+1, col, arg[i+1]+1, col))
					print ("\\draw[-]      (q{}_{}) -- (q{}_{});".format(arg[-1]+1, col, l_arg+1, col))

			col+=1

		print ("%")
		#col -=1
		for q in range (0, len(l)):
			i = l[q]
			#if (i < col):
			print ("\\node[] at ({},{}) {{}} edge [-] (q{}_{});".format(col*x-x/2, y*(-q), q+1, i))
		print ("%")


		#print ("\\node at ({},{}) {{\\footnotesize{{T{}}}}};".format(0, y, 0))
		#for t in range(1, col):
		#	print ("\\draw[dashed] ({},{}) -- ({},{});".format(x*t - x/2, y/2, x*t - x/2, -y*len(l) + y/2))
		#	print ("\\node at ({},{}) {{\\footnotesize{{T{}}}}};".format(x*t, y, t))
		#print ("%")
#		print ("\\draw[dashed] ({},{}) -- ({},{});".format(x*col - x/2, y/2, x*col - x/2, -y*len(l) + y/2))
#		print ("\\node at ({},{}) {{\\footnotesize{{T{}}}}};".format(x*col - x/2, -y*len(l)+ y/4, col-1))

		print ("\\end{tikzpicture}")
		print ("}\n}")


	def toLatexCirc(self, circ):
		qubits = circ[0]
		latexCirc = self.toLatex(circ[1])
		expr = reversed(latexCirc.split(" \circ "))
		var = circ[2].split(",")

		print (latexCirc)
		print (expr)

		l = [0]*qubits

		print ("qubits", qubits, len(l))

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
			output = output + "\\node at (0,{})\t(q{}_{})\t{{$\\lvert {} \\rangle$}};".format(y*(-i), i+1, col, var[i])

		col += 1
		for c in expr:
			op = c[0]

			temp = regex.findall(r'\d+', c)
			arg = list(map(int, temp))

			if op == "N":
				output = output + "%\n% Column {}".format(col)
				for n in arg:
					output = output + "\n\\node[operator] (q{}_{}) at ({},{}) {{X}} edge [-] (q{}_{});".format(n, col, col*x, y*(-n), n+1, l[n-1])
					l[n-1] = col
				col+=1
			if op == "T":
				output = output + "%\n% Column {}".format(col)

				output = output + "\n\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(arg[0], col, col*x, y*(-arg[0]), arg[0]+1, l[arg[0]-1])
				l[arg[0]-1] = col
				output = output + "\n\\node[bullet] (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(arg[1], col, col*x, y*(-arg[1]), arg[1]+1, l[arg[1]-1])
				l[arg[1]-1] = col
				output = output + "\n\\node[XOR]    (q{}_{}) at ({},{}) {{}} edge [-] (q{}_{});".format(arg[2], col, col*x, y*(-arg[2]), arg[2]+1, l[arg[2]-1])
				l[arg[2]-1] = col

				output = output + "\n\\draw[-]      (q{}_{}) -- (q{}_{});".format(arg[0]+1, col, arg[1]+1, col)
				output = output + "\n\\draw[-]      (q{}_{}) -- (q{}_{});".format(arg[1]+1, col, arg[2]+1, col)

				col+=1

		#\draw[dashed] (2.25,0.25) -- (2.25,-7);
		#\node at (2.25,-7.25) {\footnotesize{T1}};

		output = output + "%"
		#col -=1
		for q in range (0, len(l)):
			i = l[q]
			#if (i < col):
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
		output = output + "\n}\n}"

		return output


	def toLatex(self, expr):
		formula = []
		n_list = []
		for c in expr:
			s = c.split(',')
			if s[0] == "p":
				n_list.append(s[1])
			elif len(n_list) > 0:
				j = ",".join(sorted(n_list))
				formula.append("N_{"+j+"}")
				n_list = []
			if s[0] == "t":
				j = ",".join(s[1:3])
				formula.append("\\tof^{"+j+"}_{"+ s[3]+"}")
		return (" \circ ".join(reversed(formula)))
			

	def executeGen(self, circuito):
		m = circuito[0]
		c = circuito[1]
		q = circuito[2].split(",")

		pos = self.parserPos(q, 0)
		val = self.parserVal(q, pos)
		
		pos = self.execute(pos, val, c)

		ret = self.parserPosVal(pos, val)

		#print (simplify("(" + val[0] + "+" + val[2] + "+" + val[8] + ")/(1-x1*y1)"))

		#print (ret[0], "\n\n")
		#print (ret[1])
		

	def printMemory(self, values, d , partial):
		partial0 = partial * values[d][0]
		partial1 = partial * values[d][1]

		if (d == len(values)-1):
			print (partial0, ", ", partial1, ", ",)
		else:
			self.printMemory(values, d+1, partial0)
			self.printMemory(values, d+1, partial1)

	def printPos(self, positions):
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

			e = e.replace("*","")
			e = e.replace("x","f_A")
			e = e.replace("y","f_B")

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

			if par[0] == "p":
				pos = self.pauliX(pos, int(par[1])-b)
			elif par[0] == "z":
				pos, val = self.pauliZ(pos, val, int(par[1])-b)			
			elif par[0] == "c":
				pos = self.cnot(pos, int(par[1])-b, int(par[2])-b)
			elif par[0] == "t":
				pos = self.toffoli(pos, int(par[1])-b, int(par[2])-b, int(par[3])-b)
			elif par[0] == "t00":
				pos = self.toffoli00(pos, int(par[1])-b, int(par[2])-b, int(par[3])-b)
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
