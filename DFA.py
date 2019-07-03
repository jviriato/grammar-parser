from Grammar import Grammar
import re
class DFA:
    def __init__(self, states, start_state, accept_state):
        self.states = states
        self.ER_states = []
        self.start_state = start_state
        self.accept_state = accept_state
        self.ER = ''
    
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
        #self.printDFA(states)
        self.states = states

    def convertER(self):
        self.ER_states = self.states
        self.verifyInitialStates()
        self.verifyAcceptStates()
        self.printDFA(self.ER_states)
        ER = self.deleteStates(self.start_state, self.ER_states[self.start_state][0])
        self.ER = ER[1:]
    
    def deleteStates(self, last, production):
        print("\nDeleting Intermediate States (",last ,")")
        er = ''
        states = self.ER_states
        #self.printDFA(states)
        print("\t(Current)", last, " -> ", production)
        current = production[1]
        #print("atual: ", current, " - last: ", last)
        accept_state = self.getAcceptStates(self.ER_states)
        
        if(current == accept_state[0]):
            #print("Estado final ", production[0])
            if(production[0] != '&'):
                return production[0]
            return ''
        elif(last == current):
            #print("teste", production)
            length = len(production[0])
            if(length > 1):
                return '(' + production[0] + ')*'
            else:
                return production[0] + '*'
                
        er += '('
        
        self.lookAhead(current)
        #self.printDFA(self.ER_states)

        for transitions in states[current]:
            #print(last, "->", transitions)
            #print("deleteStates(", current,", ", transitions, ")")
            new_er = self.deleteStates(current, transitions)
            if(new_er != ''):
                new_er += '|'
            er += new_er
            print("\tER parcial:", er)
        return  production[0] + er[:-1]+ ')'
     
    def lookAhead(self, current):
        print("\nLook Ahead for Closed Loops")
        states = self.ER_states
        #print("atual: ", current)
        accept_state = self.getAcceptStates(self.ER_states)
        for transitions in states[current]:
            next_state = transitions[1]
            #print("next: ", next_state) 
            if(next_state != current):
                for back_transitions in states[next_state]:
                    if(back_transitions[1] == current):
                        print("\tClosed Loop Detected on Transition: ", next_state, "-> ", back_transitions)
                        next_transition = states[next_state]
                        if(len(next_transition[:-1]) == 0):
                            #print("estado vazio")
                            #print(transitions)
                            looped_er = transitions[0] + back_transitions[0]
                            print("\tlooped ER: ", looped_er)
                            next_transition = states[current]
                            print(next_transition)
                            next_transition.remove(transitions)
                            print(next_transition)
                            next_transition.append([looped_er, current])
                            print(next_transition)
                        else:
                            looped_er = back_transitions[0] + transitions[0]
                            print("\tlooped ER: ", looped_er)
                            next_transition.remove(back_transitions)
                            next_transition.append([looped_er, next_state])
                    else:
                        print("\tNo Closed Loop Detected on Transition ", next_state, "->", back_transitions)



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
                new_dfa[simbolo][id] = tuple(new_tuple)

        new_dfa['F'] = [('&', 'FINAL_STATE')]
        #self.printDFA(new_dfa)
        self.ER_states = new_dfa
	

        

    def getAcceptStates(self, states):
        accept_states = []
        for simbolo in states:
            for transitions in states[simbolo]:
              if(transitions[1] == 'FINAL_STATE'):
                  accept_states.append(simbolo)
        #print("Accept States: ", accept_states)
        return accept_states

    def verifyInitialStates(self):
        print("Verifying Initial States")
        create_new_start_state = False
        for simbolo in self.states:
            #print(simbolo, "->", self.states[simbolo])
            for transitions in self.states[simbolo]:
              #print(transitions)
              if(transitions[1] == self.start_state):
                print("Exist Edge to Initial State")
                create_new_start_state = True
        if(create_new_start_state):
            #self.ER_states[self.start_state + '1'] = ([('&', self.start_state, 'NO')])
            self.ER_states[self.start_state + '1'] = ([('&', self.start_state)])
            self.start_state = self.start_state + '1'
        #self.printDFA(self.ER_states)

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
