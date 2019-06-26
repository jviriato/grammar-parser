#!/usr/bin/env python3
import argparse
from Grammar import Grammar
def main():
    grammar_path = 'gramatica_exemplo_1.txt'
    with open(grammar_path, 'r') as gf:
        grammar = gf.readline().rstrip()
    g = Grammar(grammar)
    g.validateGrammar()
    # word = i
    # nput('Digite a palavra a ser validada: ')
    word = "accc"
    g.recognize(word)
if __name__ == "__main__":
    main()
