# Quantum-Fuzzy
O projeto Quantum-Fuzzy busca unir as áreas de Lógica Fuzzy e Computação Quântica, através das propriedades e características que as unem, onde apresentam a incerteza de modos distintos. Analisando os conectivos existentes da Lógica Fuzzy, o projeto Quantum-Fuzzy busca demonstrar com um viés matemático a interpretação destas operações entre Conjuntos Fuzzy utilizando bits e registradores quânticos.

# Arquivos
## ./runCirc
O arquivo é responsável por receber o símbolo do operador de uma expressão, com a finalidade de gerar o circuito quântico do algoritmo. É utilizado a classe circ para realizar a análise do parâmetro, assim possibilitando a descrição dos circuitos.

### Para executar
python runCirc.py PORTA
python runCirc.py AND

### ./Circ
Contém a definição da classe circ, que será utilizada para analisar a entrada passada como argumento e gerar o circuito. Com a chamada do método "get" é possível verificar a expressão que foi recebida. Posterioramente o método "executeCirc" análisa todas os qubits possíveis e seus respectivos estados, utilizando o método "parserPos", que gera todas as posições de memórias possíveis considerando a representação total da expressão, e  o método "parserVal", que gera todos os estados possíveis. 

O método "execute" realiza as transformações quânticas considerando a expressão que foi recebida como argumento, análisando as posições de memórias da expressão e em quais posições as transformações quânticas atuam. 

## ./runInterpretador
O arquivo é responsável por receber o símbolo do operador de uma expressão, a fim de realizar a análise, obtento o resultado da avaliação da expressão matemáticamente, considerando parâmetros genéricos. Primeiramente é verificado se foi passado como argumento uma operação que foi previamente descrita, e em seguida, é utilizado a classe Interpretador. O método "toLatex" gera uma representação em latex do circuito que foi descrito, apresentando a evolução temporal que do algoritmo.

### ./Interpretador
A classe interpretador avalia a expressão que foi recebida. O método "func" obtém a expressão que representa o conectivo. Logo após é chamado o método "parserExp", onde o método "parserString" filtra a string original e separa os argumentos, e o método "func" avalia as operações que compõe a expressão. Logo após é substituido os argumentos "x" e "y" por "f_A" e "f_B", representando o grau de pertinência nos Conjuntos Fuzzy A e B. No retorno da função é obtido 3 representações, sendo duas incorporadas para o código latex, e a original resultante após a aplicação de todas as etapas.

## symbolic_simulator 
### ./Gates
Possuí a construção das portas quânticas do simulador simbólico.

### ./runSimulator
Definição do circuito quântico para o simulador simbólico.

#### Para executar
python runSimulator.py