Testar a expressão regular: https://regex101.com/r/KjhYVv/6

Para testar uma GR, deve-se colocar num arquivo, onde a primeira linha contém a especificação da Gramática.
Exemplo:
```
G = ({S, A}, {a, b, c}, S, {S->aS, S->bA, A->&, A->cA})
Gera o equivalente à a*bc* 
``` 

**&** é o símbolo terminal
