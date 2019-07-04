from Grammar import Grammar
import re
class Automata:
    def __init__(self, states = None, start_state = None, accept_state = None):
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
        # print(regras)
        # print(transitions)
        # print(states)
        self.states = states

    def convertER(self):
        print("Creating Regular Expression:\n")
        self.ER_states = self.states
        self.verifyInitialStates()
        self.verifyAcceptStates()
        self.concatenateAcceptStates()
        #self.printDFA(self.ER_states)
        #print(self.start_state)
        initial = self.ER_states[self.start_state][0]
        #print(initial)
        #ER = self.deleteStates(self.start_state, self.ER_states[self.start_state][0])
        initial = ('', self.start_state)
        while(len(self.ER_states) != 2 and self.ER_states[self.start_state][0][1] not in self.getAcceptStates(self.ER_states)):
            #self.printDFA(self.ER_states)
            self.deleteStates('', initial)
            #print("==================================")

        self.ER = self.ER_states[self.start_state][0][0]
        self.ER = self.ER.replace('()*', '')
        self.ER = self.ER.replace('||', '|')
        self.ER = self.ER.replace('&&', '&')
        #self.ER = self.ER.replace('&', '')
        self.ER = self.ER[1:-1].replace('(&)', '')
    
    def deleteStates(self, last, production):
        ##print("\nDeleting Intermediate States (",last ,")")
        er = ''
        dfa = self.ER_states
        #self.printDFA(states)
        ##print("\t(Current)", last, " -> ", production)
        current = production[1]
        ##print("Current: ", current, " - Last: ", last)
        accept_state = self.getAcceptStates(self.ER_states)
        is_next_state_final = False
        for states in dfa[current]:
            next_transition = states[1]
            ##print(current, ':')
            ##print("  filho:", next_transition)
            for next_states in dfa[next_transition]:
                if(next_transition != current):
                    ##print("      Filhos de", next_transition, next_states)
                    if(next_states[1] in accept_state):
                        is_next_state_final = True
        #self.printDFA(dfa)
        if(is_next_state_final):
            ##print("Existe um estado final a frente")
            for states in dfa[current]:
                #print("states:", states[1])
                
                if(states[1] != current):
                    global_er = '('
                    recursion_er = ''
                    for next_states in dfa[states[1]]:
                        if(states[1] == next_states[1]):
                            recursion_er += '(' + next_states[0] + ')*'
                    #recursion_er += ')*'
                    new_accept = ''
                    closed_loop = False
                    for next_states in dfa[states[1]]:
                        ##print("Deleting:",states[1])
                        ##print("  ",states[1], "->", next_states)
                        #if(states[1] == next_states[1]):
                            #print("recursion")
                            #a = 5
                            #recursion_er = next_states[0] + '*'
                        #else:
                        if(states[1] != next_states[1] and last != states[1]):
                            next_er = next_states[0]
                            new_accept = next_states[1]
                            ##print("\tConcatenating: ", states, next_states)
                            ##print("\tNew Transition state: ", new_accept)
                            new_er = states[0] + recursion_er+ next_er
                            #new_tuple = (new_er, new_accept)
                            #new_tuple = tuple(new_tuple)
                            #print("  ", new_tuple)
                            global_er += new_er
                            ##print("\tResult: ", global_er)
                            global_er += '|'
                            ##print("\tParcial ER: ", global_er)
                            #break;
                        elif(last == states[1]):
                            new_accept = current
                            global_er += next_states[0]
                            closed_loop = True
                            
                    #new_tuple = (global_er[:-1], next_states[1])
                    if(closed_loop):
                        ##print("Detected Closed Loop")
                        new_tuple = (global_er, new_accept)
                        new_tuple = tuple(new_tuple)
                        id = dfa[current].index(states)
                        dfa[current][id] = new_tuple
                        
                    else:
                        new_tuple = (global_er[:-1]+ ')', new_accept)
                        new_tuple = tuple(new_tuple)
                        id = dfa[current].index(states)
                        dfa[current][id] = new_tuple
                        del dfa[states[1]]
                    ##print("Global ER:", global_er)
        else:
            ##print("Itera mais a fundo")
            for states in dfa[current]:
                ##print("Iterator:", current, states)
                if(current != states[1] and last != states[1]):
                    self.deleteStates(current, states)
        self.ER_states = dfa
        #self.printDFA(self.ER_states)

        
    
    def concatenateAcceptStates(self):
        new_dfa = self.ER_states
        print("Concatenating Accept States")
        accept_states = self.getAcceptStates(new_dfa)
        #print(accept_states)
        length = len(new_dfa)
        new_accept_state = 'F' + str(length)
        new_dfa[new_accept_state] = [('&', 'FINAL_STATE')]
        for states in accept_states:
            state = list(new_dfa[states][0])
            state[1] = new_accept_state
            state = tuple(state)
            #print(state)
            new_dfa[states] = []
            new_dfa[states].append(state)
            

    def verifyAcceptStates(self):
        new_dfa = self.ER_states
        print("Verifying Accept States")
        accept_states = self.getAcceptStates(new_dfa)
        #self.printDFA(new_dfa)
        #print(accept_states)
        for simbolo in accept_states:
            #print(new_dfa[simbolo])
            for index in new_dfa[simbolo]:
                #print(index)
                new_tuple = list(index)
                length = len(new_dfa)
                #print("size: ", length)
                if(new_tuple[1] == 'FINAL_STATE'):
                    new_simbolo = 'F' + str(length)
                    new_dfa[new_simbolo] = [('&', 'FINAL_STATE')]
                    new_tuple[1] = new_simbolo
                    #new_tuple[2] = 'NO'
                id = new_dfa[simbolo].index(index)
                new_dfa[simbolo][id] = tuple(new_tuple)

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
        #self.printAutomata(self.ER_states)

    def printDFA(self, states):
      print("Current DFA:")
      for simbolo in states:
          print(simbolo, "->", states[simbolo])

    def convertRulesToTransitions(self, regras):
        transitions = []
        for r in regras:
            prod_rule = r[0]
            isFinal = 'NO'
            esq = re.sub('[A-Z]', '', r[1])
            dire = re.sub('[a-z&0-9]', '', r[1])
            if esq is '&':
                dire = 'FINAL_STATE'
                isFinal = 'YES'
            if dire is '':
                dire = 'FINAL_STATE'
                isFinal = 'YES'
            #transitions.append((esq, dire, isFinal))
            transitions.append((esq, dire))
        return transitions
