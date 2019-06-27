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