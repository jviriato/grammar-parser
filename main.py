#!/usr/bin/env python3
import argparse
from Grammar import Grammar
def main():
    # parser = argparse.ArgumentParser(description='Process a Regular Grammar.')   
    # parser.add_argument('grammar', help='The grammar. Example: "" ') 
    # args = parser.parse_args()
    # grammar = args.grammar
    grammar = "G = ( {S , A}, {a, b, c}, V, {S->aS,S->bA,A->&,A->cA})"
    g = Grammar(grammar)
    g.printRegex()
    g.validateGrammar()
if __name__ == "__main__":
    main()