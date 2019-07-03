### Como usar

Você pode inserir os argumentos (caminho do arquivo e palavra a ser parseada) diretamente pela CLI:
```
usage:   main.py -w [PALAVRA] -f [ARQUIVO.TXT]
Exemplo: main.py -f gramatica_exemplos/gramatica_exemplo_1.txt -w aaaab
optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Input filename
  -w WORD, --word WORD  Input word
```
Os argumentos são opcionais.


Para testar uma GR, deve-se colocar num arquivo, onde a primeira linha contém a especificação da Gramática.
Exemplo:
```
G = ({S, A}, {a, b, c}, S, {S->aS, S->bA, A->&, A->cA})
Gera o equivalente à a*bc* 
``` 

**&** é o símbolo terminal
