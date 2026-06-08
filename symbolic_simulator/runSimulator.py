import sys
from sympy.abc import x, y, z, N
import Simulator

simulator = Simulator.Simulator()

#simulator.createState(1, [1])

#simulator.createState(3, [x,x,0])
#                        [2,1,0]

simulator.createState(5, [x,x,0,y,0])
#                        [4,3,2,1,0]
simulator.printNonZeroPosState()

#simulator.createState(6, [0,0.90,0.70,0,0.60,0.25])
#                         [   5,   4,3,   2,   1,0]
print ("#######")

#------------------------------------
#Toffoli:
#simulator.executeCircuit("C-X,0-1,2")
#C-X,3-1,2,0 -> Applies X gate on qubit 3 if qubits 1 and 2 are 1 and 0 respectively
#o qubit 0 é o ultimo da lista, menos significativo
#qubit 1 é o y e qubit 2 é o x
#------------------------------------
# C-NOT:
#"C-X,CONTROLE-ALVO"
#simulator.executeCircuit("C-X,0-1")
# se qubit 0 tem valor 1, aplica X no qubit 1
#simulator.executeCircuit("C-X,1-0") 
# se qubit 1 tem valor 1, aplica X no qubit 0
#------------------------------------


#η2-necessity Circuit
#simulator.executeCircuit("C-X,0-1,2")
#ρ[2]-possibility Circuit
#simulator.executeCircuit("X,1;C-X,0-1,2")

#p_-Circuit
#simulator.executeCircuit("C-X,0-1,2;C-X,2-0;C-X,1-0")

# Circuito modal: x^2 é armazenado no qubit 3, realiza a CRaizQuadrada entre qubit y e filho, e depois CRaizQuadrada pai^2 e filho
# ρ[2]-Circuit in the PP-P interactivity
#simulator.executeCircuit("X,3;C-X,2-4,3;C-X,0-2;C-X,0-1")

# η2-necessity circuit and histogram for PP-P interactivity
simulator.executeCircuit("C-X,2-4,3;C-X,0-2;C-X,0-1")

# pp-p interactivity
#simulator.executeCircuit("C-X,0-1;C-X,0-2")

# pp-p interactivity com not
#simulator.executeCircuit("X,2;C-X,0-1;C-X,0-2")
#simulator.executeCircuit("X,1;C-X,0-1;C-X,0-2")
#simulator.executeCircuit("X,2;X,1;C-X,0-1;C-X,0-2")

#simulator.printNonZeroPosState()
#simulator.printPosState()

print ("####### Measure #######")
simulator.measure([0], True)
# python runSimulator.py