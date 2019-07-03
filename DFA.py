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
        self.concatenateAcceptStates()
        #self.printDFA(self.ER_states)
        #print(self.start_state)
        initial = self.ER_states[self.start_state][0]
        #print(initial)
        #ER = self.deleteStates(self.start_state, self.ER_states[self.start_state][0])
        initial = ('', self.start_state)
        while(len(self.ER_states) != 2 and self.ER_states[self.start_state][0][1] not in self.getAcceptStates(self.ER_states)):
            self.printDFA(self.ER_states)
            print(self.ER_states[self.start_state][0][1])
            print(self.getAcceptStates(self.ER_states))
            self.deleteStates('', initial)
            print("==================================")

        self.ER = self.ER_states[self.start_state][0][0]
        self.ER = self.ER.replace('()*', '')
        self.ER = self.ER.replace('&', '')
    
    def deleteStates(self, last, production):
        print("\nDeleting Intermediate States (",last ,")")
        er = ''
        dfa = self.ER_states
        #self.printDFA(states)
        print("\t(Current)", last, " -> ", production)
        current = production[1]
        print("atual: ", current, " - last: ", last)
        accept_state = self.getAcceptStates(self.ER_states)
        is_next_state_final = False
        for states in dfa[current]:
            next_transition = states[1]
            print(current, ':')
            print("  filho:", next_transition)
            for next_states in dfa[next_transition]:
                if(next_transition != current):
                    print("      Next States", next_states)
                    if(next_states[1] in accept_state):
                        is_next_state_final = True
        #self.printDFA(dfa)
        if(is_next_state_final):
            print("Existe um estado final dps desse")
            self.lookAhead(current)
            for states in dfa[current]:
                print("states:", states[1])
                
                if(states[1] != current):
                    global_er = ''
                    recursion_er = ''
                    for next_states in dfa[states[1]]:
                        if(states[1] == next_states[1]):
                            recursion_er += '(' + next_states[0] + ')*'
                    #recursion_er += ')*'
                    for next_states in dfa[states[1]]:
                        print(states[1])
                        print("  ", next_states)
                        #if(states[1] == next_states[1]):
                            #print("recursion")
                            #a = 5
                            #recursion_er = next_states[0] + '*'
                        #else:
                        if(states[1] != next_states[1]):
                            next_er = next_states[0]
                            new_accept = next_states[1]
                            print("  next er: ", next_er)
                            print("  new ac: ", new_accept)
                            new_er = states[0] + recursion_er+ next_er
                            print("  new er: ", new_er)
                            #new_tuple = (new_er, new_accept)
                            #new_tuple = tuple(new_tuple)
                            #print("  ", new_tuple)
                            global_er += new_er
                            print("  new er: ", global_er)
                            global_er += '|'
                        print("global parcial: ", global_er)
                    #new_tuple = (global_er[:-1], next_states[1])
                    new_tuple = (global_er[:-1], new_accept)
                    new_tuple = tuple(new_tuple)
                    id = dfa[current].index(states)
                    dfa[current][id] = new_tuple
                    del dfa[states[1]]
                    print("global er:", global_er)
        else:
            print("Itera mais a fundo")
            for states in dfa[current]:
                print("Iterator:", current, states)
                if(current != states[1] and last != states[1]):
                    self.deleteStates(current, states)
        self.ER_states = dfa
        #self.printDFA(self.ER_states)

        
    
    def deleteStates1(self, last, production):
        print("\nDeleting Intermediate States (",last ,")")
        er = ''
        states = self.ER_states
        #self.printDFA(states)
        print("\t(Current)", last, " -> ", production)
        current = production[1]
        print("atual: ", current, " - last: ", last)
        accept_state = self.getAcceptStates(self.ER_states)
        
        if(current == accept_state[0]):
            #print("Estado final ", production[0])
            if(production[0] != '&'):
                return production[0] + ')'
            return '&)'
        elif(last == current):
            #print("teste", production)
            length = len(production[0])
            if(length > 1):
                return '(' + production[0] + ')*'
            else:
                return production[0] + '*)'
        #else:
            #print(production[0])
            #er += production[0] + '|'     
        er += '('
        
        self.lookAhead(current)
        #self.printDFA(self.ER_states)
        new_er = er
        for transitions in states[current]:
            #print(last, "->", transitions)
            print("\tdeleteStates(", current,", ", transitions, ")")
            er_aux = self.deleteStates(current, transitions)
            if(current != last and er_aux != ''):
                er += '|'
            new_er += er_aux
            if(new_er != ''):
                new_er += ''
            er += new_er
            print("\tER parcial:", er)
        return  production[0] + er + ')'
     
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
