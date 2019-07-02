from Grammar import Grammar
import re
class DFA:
    def __init__(self, states, start_state, accept_state):
        self.states = states
        self.ER_states = []
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
            #states[simbolo] = dict(transitions)
            states[simbolo] = transitions
        self.printDFA(states)
        self.states = states

    def convertER(self):
        self.ER_states = self.states
        self.verifyInitialStates()
        self.verifyAcceptStates()
        self.deleteStates()

    def deleteStates(self):
        print("Deleting Intermediate States")
        states = self.ER_states
        initial = self.start_state
        accept_state = self.getAcceptStates(self.ER_states)
        for simbol in states:
            if(simbol != initial and simbol not in accept_state):
                self.deleteIntermediateStates(states, simbol)
            
    def deleteIntermediateStates(self, dfa, simbol):
        print("Removing: ", simbol)
        new_state = ''
        state_list = list(dfa)
        print(state_list)
        for state in dfa:
            for transitions in dfa[state]:
                new_state = new_state + '('
                if(state == simbol):
                    if(transitions[1] != simbol):
                        new_state = new_state + transitions[0]
                if(transitions[1] == simbol):
                    print(state, " -> ", transitions)
                    if(state == simbol):
                        print("recursion")
                        new_state = new_state + transitions[0] + '*'
                    else:
                        new_state = new_state + transitions[0]
                new_state = new_state + ')'
        print(new_state)

    def deleteIntermediateStates123123(self):
        print("Deleting Intermediate States")
        states = self.ER_states
        initial = self.start_state
        accept_state = self.getAcceptStates(self.ER_states)
        for transitions in states[initial]:
            print("Initial ", initial, "-> ", transitions)
            to_be_deleted = transitions[1]
            new_state = transitions[0] + '('
            for transitions_next in states[to_be_deleted]:
                print("Next ", to_be_deleted, "-> ", transitions_next)
                new_state = new_state + transitions_next[0]
                
                #states[initial][id] = new_state
                new_state = new_state + '+'
            new_state = new_state[:-1] + ')'
            states[initial].append(new_state)
            print("New State : ", new_state)
            id = states[initial].index(transitions)
            print(id)
            states[initial].pop(id)

            del states[to_be_deleted]

        self.printDFA(states)
        
        

    def verifyAcceptStates(self):
        new_dfa = self.ER_states
        print("Verifying Accept States")
        accept_states = self.getAcceptStates(new_dfa)
        
        for simbolo in accept_states:
            #print(new_dfa[simbolo])
            for index in new_dfa[simbolo]:
                new_tuple = list(index)
                if(new_tuple[1] == 'FINAL_STATE'):
                    new_tuple[1] = 'F'
                    #new_tuple[2] = 'NO'
                id = new_dfa[simbolo].index(index)
                new_dfa[simbolo][id] = new_tuple

            #new_dfa[simbolo].append(('&', 'F', 'NO'))
        #new_dfa['F'] = [('&', 'FINAL_STATE', 'YES')]
        new_dfa['F'] = [('&', 'FINAL_STATE')]
        self.printDFA(new_dfa)
        print(self.getAcceptStates(new_dfa))
        self.ER_states = new_dfa
	

        

    def getAcceptStates(self, states):
        accept_states = []
        for simbolo in states:
            for transitions in states[simbolo]:
              if(transitions[1] == 'FINAL_STATE'):
                  accept_states.append(simbolo)
        print("Accept States: ", accept_states)
        return accept_states

    def verifyInitialStates(self):
        print("Verifying Initial States")
        create_new_start_state = False
        for simbolo in self.states:
            print(simbolo, "->", self.states[simbolo])
            for transitions in self.states[simbolo]:
              print(transitions)
              if(transitions[1] == self.start_state):
                print("Exist Edge to Initial State")
                create_new_start_state = True
        if(create_new_start_state):
            #self.ER_states[self.start_state + '1'] = ([('&', self.start_state, 'NO')])
            self.ER_states[self.start_state + '1'] = ([('&', self.start_state)])
            self.start_state = self.start_state + '1'
        self.printDFA(self.ER_states)

    def printDFA(self, states):
      print("Current States:")
      for simbolo in states:
          print(simbolo, "->", states[simbolo])

    def convertRulesToTransitions(self, regras):
        transitions = []
        for r in regras:
            prod_rule = r[0]
            isFinal = 'NO'
            esq = re.sub('[A-Z]', '', r[1])
            dire = re.sub('[a-z&]', '', r[1])
            if esq is '&':
                dire = 'FINAL_STATE'
                isFinal = 'YES'
            if dire is '':
                dire = 'FINAL_STATE'
                isFinal = 'YES'
            #transitions.append((esq, dire, isFinal))
            transitions.append((esq, dire))
        return transitions
