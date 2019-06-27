import re
from Word import Word


class Grammar:
    def __init__(self, grammar_to_parse):
        self.regex = self.doRegex(grammar_to_parse)
        self.startSymbol = self.setStartSymbol()
        self.terminalSymbols = self.setSymbols(self.regex.group(4))
        self.nonTerminalSymbols = self.setSymbols(self.regex.group(2))
        self.rules = self.setRules(self.regex.group(7))

    #  Aqui ocorre o parse da gramática fornecida pelo usuário
    def doRegex(self, grammar_to_parse):
        pattern = r"(G\s*=\s*\()(?P<nao_terminais>\s*{\s*([A-Z]\s*,\s*)*[A-Z]+\s*})\s*,\s*(?P<terminais>{\s*([a-z0-9]\s*,\s*)*[a-z0-9]+\s*})\s*,\s*(?P<start_symbol>[A-Z]{1})\s*,\s*(?P<prod_rules>\s*{\s*([A-Z]{1}->(&|[a-z0-9]+[A-Z]?|[A-Z]{1})\s*,*\s*)+\s*}\s*)(\))$"
        search = re.search(pattern, grammar_to_parse)
        return search
    
    # Print da regex
    def printRegex(self):
        print('Símbolos não terminais: ' + self.regex.group('nao_terminais'))
        print('Símbolos terminais: ' + self.regex.group('terminais'))
        print('Símbolo inicial: ' + self.regex.group('start_symbol'))
        print('Transformações: ' + self.regex.group('prod_rules'))

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
                raise ValueError('Símbolo inicial nao está nos Símbolos não terminais')
            validation, s = self.checkIfAlphabetExistsInRules()
            if validation is False:
                raise ValueError(
                    'Símbolo "{}" presente nas regras não existe em nenhum conjunto de símbolos'.format(s))
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
                symbolRules.append((k, v))
        return symbolRules

    def printStats(self, word):
        print('\t' * word.value + 'A palavra a ser reconhecida é: {}'.format(word.word))
        print('\t' * word.value + 'A Parsing word é: {}'.format(word.parsing_word))
        print('\t' * word.value + 'Ela tem este símbolo: {}'.format(word.prod_rule))
        #print('\t' * word.value + 'E estas regras: {}'.format(word.relevantRules()))
        #print('\t' * word.value + 'Os filhos dessa palavra são: {}'.format(word.children))
        print('\t' * word.value + 'Nível: ' + str(word.value))
        if word.isValid():
          print('\t' * word.value + "Valid Word")
        else:
          print('\t' * word.value + 'Os filhos de {}: '.format(word.word))

    def hasTerminal(self):
        for (l,r) in self.rules:
            if '&' in r:
                return True


    def recognize(self, w):
        self.printRegex()
        print('Palavra a ser reconhecida: ' + w)
        if self.hasTerminal():
            w += '&'
        word = Word(w, self.startSymbol, self.rules, value=0, parsing_word = self.startSymbol)
        path = self.bfs(word)
        for p in path:
            print(p)
        if not path[-1].isValid():
            print('Símbolo \'{}\' não encontrado em nenhuma regra de produção: {}'.format(path[-1].word[1], path[-1].relevantRules()))

    def bfs(self, word):
        queue = [word]
        path = []
        for state in queue:
            # print(state)
            if state.isValid():
                path = self.buildPath(state)
                break
            queue.extend(state.getChildren())
        if len(path) == 0:
            path = self.findError(queue)
        return path

    def findError(self, queue):
        erro = queue[0]
        for state in queue:
            if state.value > erro.value:
                erro = state
        return self.buildPath(erro)

    def buildPath(self, state):
        path = [state]
        while state.parent:
            path.insert(0, state.parent)
            state = state.parent
        return path