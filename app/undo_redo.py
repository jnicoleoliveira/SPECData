class UndoRedo:

    def __init__(self, action_names, undo_functions, redo_functions, max=None):
        self.action_names = action_names
        self.undo_functions = undo_functions
        self.redo_functions = redo_functions

        self.max_undo = 10 if max is None else max
        self.action_stack = []

    def add_action(self, action):
        """
        Adds action object to the top of the stack.
        Adds action object to the top of the stack.
        If the stack is at its max length, removes last in stack.
        :param action:
        :return:
        """
        if len(self.action_stack) == self.max_undo:
            index = self.action_stack.index(self.max_undo)
            self.action_stack.remove(index)

        self.action_stack.append(action)

    def undo(self):
        action = self.action_stack.pop()
        object = self.action_stack.object
        index = self.action_names.index(action.action_name)
        self.undo_functions[index](object)
        return action

    def redo(self):
        action = self.action_stack.pop()
        object = self.action_stack.object
        index = self.action_names.index(action.action_name)
        self.redo_functions[index](object)
        return action

class UserAction:

    def __init__(self, action_name, obj):
        self.action_name = action_name
        self.object = obj


class TimeMachine:

    def __init__(self, base_state, max=None):

        self.max_states = 10 if max is None else max

        # -- Redo and State Stacks -- #
        self.redo_stack = []
        self.state_stack = []

        # -- Set up -- #
        self.state_stack.append(base_state)
        self.size = 1

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
            self.size -=1

        self.state_stack.append(state)
        self.size +=1

        del self.redo_stack
        self.redo_stack = []

    def undo(self):

        if self.size == 1:
            return self.state_stack[0]   # do not pop base state

        last_state = self.state_stack.pop()
        self.size -=1

        self.redo_stack.append(last_state)
        return last_state

    def redo(self):
        if len(self.redo_stack is not 0):
            return self.redo_stack.pop()
        else:
            return None

    def can_undo(self):
        return self.size > 1

    def can_redo(self):
        return self.redo_stack is not None and len(self.redo_stack) != 0


class State:

    def __init__(self, pending_widget, accepted_widget, rejected_widget):
        self.pending_widget = pending_widget
        self.accepted_widget = accepted_widget
        self.rejected_widget = rejected_widget