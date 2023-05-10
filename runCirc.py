import sys
import Circ

if len(sys.argv) < 2:
	print ("Argumentos insuficientes")
	sys.exit()

circ = Circ.Circ()

operator = sys.argv[1]
circuit = circ.fuzzySquare.get(operator)

if circuit == None:
	print ("Operador não encontrado", operator)
	sys.exit()

circ.executeCirc(circuit)

#print (circ.toLatex(circuit[1]))

