#!/usr/bin/env python3
import argparse
import re
def doRegex(grammar):
    pattern = r"(G\s*=\s*\()(\s*{\s*([A-Z]\s*,\s*)*[A-Z]+\s*})\s*,\s*({\s*([a-z]\s*,\s*)*[a-z]+\s*})\s*,\s*([A-Z]{1})\s*,\s*(\s*{\s*(([A-Z]\s*->\s*&\s*|\s*[A-Z]\s*->\s*[a-z]*\s*[A-Z]?)\s*,*)*\s*}\s*)(\))$"
    search = re.search(pattern, grammar)
    print('Símbolos não terminais: ' + search.group(2))
    print('Símbolos terminais: ' + search.group(4))
    print('Símbolo inicial: ' + search.group(6))
    print('Transformações: ' + search.group(7))
def main():
    # parser = argparse.ArgumentParser(description='Process a Regular Grammar.')   
    # parser.add_argument('grammar', help='The grammar. Example: "" ') 
    # args = parser.parse_args()
    # grammar = args.grammar
    grammar = "G = ( {S , A}, {a, b, c}, S, {S->aS,S->bA,A->&,A->cA})"
    doRegex(grammar)
if __name__ == "__main__":
    main()