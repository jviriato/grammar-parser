import re
class Word:
    def __init__(self, word, prod_rule, rules, parsing_word = '', parent = None, children = []):
        self.word = word
        self.parent = parent
        self.prod_rule = prod_rule
        self.parsing_word = parsing_word
        self.rules = rules
        self.children = self.getChildren()
    
    """Pega apenas as regras pertinentes ao símbolo de produção
    """
    def relevantRules(self):
        rules_defined = []
        for l, r in self.rules:
            if self.prod_rule in l:
                rules_defined.append((l,r))
        return rules_defined
    
    """Define os filhos desta palavra
    """
    def getChildren(self):
        children = []
        rules = self.relevantRules()
        uppercase = re.compile('[A-Z]')
        # \/ remove o símbolo não terminal das transformações
        words = list(map(lambda r: r[1], rules))
        for i, w in enumerate(words):
            if len(w[:-1]) > 0 and w[:-1] in self.word:
                # print('Achei {} na palavra \'{}\'.'.format(w, self.word))
                # print('A regra de {} é {}'.format(w, rules[i]))
                new_word  = self.word[(len(w)-1):]
                new_parsing_word = self.word[:(len(w)-1)] + self.prod_rule
                if uppercase.search(w):
                    prod_rule = uppercase.search(w).group()
                children.append(Word(new_word, prod_rule, self.rules, self.parsing_word + new_parsing_word , self))
        return children

    def __repr__(self):
        return ('({}, {})'.format(self.word, self.prod_rule))
    def __str__(self):
        return ('({}, {})'.format(self.word, self.prod_rule))