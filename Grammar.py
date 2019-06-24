import re
from Word import Word

class Grammar:
    def __init__(self, grammar_to_parse):
        self.regex = self.doRegex(grammar_to_parse)
        self.startSymbol = self.setStartSymbol()
        self.terminalSymbols = self.setSymbols(self.regex.group(4))
        self.nonTerminalSymbols = self.setSymbols(self.regex.group(2))
        self.rules = self.setRules(self.regex.group(7))
    # Aqui ocorre o parse da gramática fornecida pelo usuário
    def doRegex(self, grammar_to_parse):
        pattern = r"(G\s*=\s*\()(\s*{\s*([A-Z]\s*,\s*)*[A-Z]+\s*})\s*,\s*({\s*([a-z]\s*,\s*)*[a-z]+\s*})\s*,\s*([A-Z]{1})\s*,\s*(\s*{\s*([A-Z]{1}->(&|[a-z]+[A-Z]?|[A-Z]{1})\s*,*\s*)+\s*}\s*)(\))$"
        search = re.search(pattern, grammar_to_parse)
        return search

    def printRegex(self):
        print('Símbolos não terminais: ' + self.regex.group(2))
        print('Símbolos terminais: ' + self.regex.group(4))
        print('Símbolo inicial: ' + self.regex.group(6))
        print('Transformações: ' + self.regex.group(7))

    # Setters
    def setStartSymbol(self):
        return self.regex.group(6)

    def setSymbols(self, regex):
        return re.sub('{|}| ', '', regex).split(',')

    # Primeiro, remove os caracteres inúteis.
    # Cada elemento separado por vírgula é colocado numa lista
    # Então, separa o que está à esquerda de -> com o que está à direita.
    # Transforma isto numa lista de listas.
    # Por fim, transforma a lista interna em um dicionário
    def setRules(self, regex):
        return list(map(lambda l: tuple(l), list(map(lambda s: s.split('->'), re.sub('{|}| ', '', regex)
                                 .split(',')))))

    # Validações da Gramática
    def validateGrammar(self):
        try:
            validation = self.validateStartSymbol()
            if validation is False:
                raise ValueError('Start Symbol not in Non-Terminal Symbols')
            validation, s = self.checkIfAlphabetExistsInRules()
            if validation is False:
                raise ValueError('Símbolo "{}" presente nas regras não existe em nenhum conjunto de símbolos'.format(s))
        except ValueError as e:
            exit(str(e))

    def validateStartSymbol(self):
        return self.startSymbol in self.nonTerminalSymbols

    def validateRules(self):
        return self.checkIfAlphabetExistsInRules()

    def checkIfAlphabetExistsInRules(self):
        for key, value in self.rules:
            for c in value:
                validation = self.checkIfCharExists(c)
                if validation is False:
                    return False, c
            if key not in self.nonTerminalSymbols:
                return False, key
        return True, ''

    # Verifica se o caractere nas transformações está presente na lista de 
    # terminais, não terminais ou se é o caractere final '&'
    def checkIfCharExists(self, char):
        return (char in self.nonTerminalSymbols or
                char in self.terminalSymbols or
                char is '&')

    def getSymbolRules(self, char):
        symbolRules = []
        for k, v in self.rules:
            if k is char:
                symbolRules.append((k,v))
        return symbolRules

    def printStats(self, word, parsing_word, prod_rule):
        print('\nA palavra atual: {}'.format(word))
        print('A palavra parseada: {}'.format(parsing_word))
        # print('O cabeçote está em \'{}\''.format(cabecote))
        print('A próxima regra de produção é: ' + prod_rule)
            
    def recognize(self, w):
        word = Word(w, self.startSymbol, self.rules)
        print('A palavra a ser reconhecida é: {}'.format(word.word))
        print('Ela tem este símbolo: {}'.format(word.prod_rule))
        print('E estas regras: {}'.format(word.relevantRules()))
        print('Os filhos dessa palavra são: {}'.format(word.children))
        print('')
        print('A palavra a ser reconhecida é: {}'.format(word.children[0].word))
        print('Ela tem este símbolo: {}'.format(word.children[0].prod_rule))
        print('E estas regras: {}'.format(word.children[0].relevantRules()))
        print('Os filhos dessa palavra são: {}'.format(word.children[0].children))
        print('')
        print('A palavra a ser reconhecida é: {}'.format(word.children[1].word))
        print('Ela tem este símbolo: {}'.format(word.children[1].prod_rule))
        print('E estas regras: {}'.format(word.children[1].relevantRules()))
        print('Os filhos dessa palavra são: {}'.format(word.children[1].children))