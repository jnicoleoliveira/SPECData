class TimeMachine:

    def __init__(self, base_state, max=None):

        self.max_states = 10 if max is None else max

        # -- Redo and State Stacks -- #
        self.redo_stack = []
        self.state_stack = []

        # -- Set up -- #
        self.state_stack.append(base_state)
        self.size = 1
        self.has_undone = False

    def add_state(self, state):
        """
        Adds state object to the top of the stack.
        If the stack is at its max length, removes last in stack.
        Re-initializes the redo stack
        :param action:
        :return:
        """
        if self.size == self.max_states:
            val = self.state_stack[self.max_states - 1]
            self.state_stack.remove(val)
            self.size -= 1

        self.state_stack.append(state)
        self.size += 1

        del self.redo_stack
        self.redo_stack = []
        print str(self.size)

    def undo(self):
        if self.has_undone is False:
            self.has_undone = True
            if self.size > 1:
                self.state_stack.pop()
                self.size -= 1

        if self.size == 1:
            return self.state_stack[0]   # do not pop base state

        last_state = self.state_stack.pop()
        self.size -= 1

        self.redo_stack.append(last_state)
        print str(self.size)

        return last_state

    def redo(self):
        if len(self.redo_stack) is not 0:
            return self.redo_stack.pop()
        else:
            return None

    def can_undo(self):
        print "UNDO?" + str(self.size)
        return self.size > 1

    def can_redo(self):
        print len(self.redo_stack)
        return self.redo_stack is not None and len(self.redo_stack) != 0

