from Grammar import Grammar
import re
class DFA:
    def __init__(self, states, start_state, accept_state):
        self.states = states
        self.start_state = start_state
        self.accept_state = accept_state
    
    def accepts(self, s):
        state = self.start_state
        accepting = self.accept_state
        transitions = self.states
        for c in s:
            state = transitions[state][c]
        return state in accepting
    
    def convertGrammar(self, grammar):
        nao_terminais = grammar.nonTerminalSymbols
        transitions = []
        states = {}
        for simbolo in nao_terminais:
            regras = grammar.getSymbolRules(simbolo)
            transitions = self.convertRulesToTransitions(regras)
            states[simbolo] = dict(transitions)
        print(states)

    def convertRulesToTransitions(self, regras):
        transitions = []
        for r in regras:
            prod_rule = r[0]
            esq = re.sub('[A-Z]', '', r[1])
            dire = re.sub('[a-z&]', '', r[1])
            if esq is '&':
                dire = prod_rule
            if dire is '':
                dire = 'FINAL_STATE'
            transitions.append((esq, dire))
        return transitions