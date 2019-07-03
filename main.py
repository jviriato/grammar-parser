#!/usr/bin/env python3
import argparse
from Grammar import Grammar
from Automata import Automata

def main():
    parser = argparse.ArgumentParser(
        description='Argumentos para entrada de arquivo e palavra')
    parser.add_argument('-f','--filename', help='Input filename', required=False)
    parser.add_argument('-w','--word', help='Input word', required=False)
    args = parser.parse_args()

    if args.filename:
        grammar_path = args.filename
    else:
        grammar_path = 'gramatica_exemplos/gramatica_exemplo_loop.txt'
    with open(grammar_path, 'r') as gf:
        grammar = gf.readline().rstrip()
    g = Grammar(grammar)
    g.validateGrammar()

    if args.word:
        word = args.word
    else:
        word = input('Digite a palavra a ser validada: ')

    ehValido = g.recognize(word)
    if ehValido:
        dfa = Automata(start_state = g.startSymbol)
        dfa.convertGrammar(g)
        dfa.convertER()
        print('A ER gerada é: ')
        print(dfa.ER)

if __name__ == "__main__":
    main()
