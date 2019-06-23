#!/usr/bin/env python3
import argparse
from Grammar import Grammar
def main():
    # parser = argparse.ArgumentParser(description='Process a Regular Grammar.')   
    # parser.add_argument('grammar', help='The grammar. Example: "" ') 
    # args = parser.parse_args()
    # grammar = args.grammar
    # grammar = "G = ( {S , A}, {a, b, c}, S, {S->aS,S->bA,A->&,A->cA})"
    grammar_path = 'gramatica_exemplo_1.txt'
    with open(grammar_path, 'r') as gf:
        grammar = gf.readline().rstrip()
    g = Grammar(grammar)
    g.validateGrammar()

    word = "abccc"
    g.recognize(word)
if __name__ == "__main__":
    main()