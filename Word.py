import re
class Word:
    def __init__(self, word, prod_rule, rules, value, parsing_word, parent = None, children = []):
        self.word = word
        self.parent = parent
        self.prod_rule = prod_rule
        self.parsing_word = parsing_word
        self.rules = rules
        self.value = value
        self.children = self.getChildren()
    """Pega apenas as regras pertinentes ao símbolo de produção
    """
    def relevantRules(self):
        rules_defined = []
        for l, r in self.rules:
            if self.prod_rule in l:
                rules_defined.append((l,r))
        return rules_defined
    

    def isValid(self):
      if not self.word.strip() and not self.parsing_word[-1].isupper():
          return True

    def getValidRules(self,rules):
        w = self.word
        valid_rules = []
        for l, r in rules:
            if w.startswith(re.sub('[A-Z]', '', r)):
                valid_rules.append((l,r))
        return valid_rules
    """Define os filhos desta palavra
    """
    def getChildren(self):
        children = []
        rules = self.relevantRules()
        valid_rules = self.getValidRules(rules)
        for i, (prod, regra) in enumerate(valid_rules):
            terminais = re.sub('[A-Z]', '', regra)
            nao_terminal = re.sub('[a-z&0-9]', '', regra)    
            new_word = self.word[len(terminais):]
            prod_rule = nao_terminal
            new_parsing_word = self.word[:len(terminais)]
            children.append(Word(new_word,prod_rule,self.rules, self.value + 1, re.sub('[A-Z]', '', self.parsing_word) + new_parsing_word + prod_rule, self))
        return children

    def __repr__(self):
        tab = '\t' * self.value
        return (('\tEntrada: {}\nRegra de Produção: {}\nPalavra Parseada: {}\n').format(self.word, self.prod_rule, self.parsing_word))
    def __str__(self):
        tab = '\t' * self.value
        return (('{tab}Entrada: {}\n{tab}Regra de Produção: {}\n{tab}Palavra Parseada: {}\n{tab}{}').format(self.word, self.prod_rule, self.parsing_word, 'Válido' if self.isValid() else '', tab=tab))
