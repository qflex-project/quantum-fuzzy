import sys
import Interpretador

if len(sys.argv) < 2:
	print ("Argumentos insuficientes")
	sys.exit()

interpretador = Interpretador.Interpretador()
interpretador.parseOperator(sys.argv[1])