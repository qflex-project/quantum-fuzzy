import sys
import Circ
import Interpretador

if len(sys.argv) < 2:
	print ("Argumentos insuficientes")
	sys.exit()

circ = Circ.Circ()

operator = sys.argv[1]
#circuit = circ.fuzzySquare.get(operator)
#circuit =circ.intFuzzy.get(operator)
circuit = circ.fuzzy.get(operator)
#circuit = circ.entradaClassica.get(operator)

if circuit == None:
	print ("Operador não encontrado", operator)
	sys.exit()

circ.executeCirc(circuit)
print(circ.toLatexCircFuzzy(operator))
print (circ.toLatex(circuit[1]))

interp = Interpretador.Interpretador()

print( interp.parseOperator(operator) )


# COMANDO: python runCirc.py PORTA
# python runCirc.py AND