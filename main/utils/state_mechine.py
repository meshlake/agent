from typing import Optional
from .state_tree import StateTreeNode


class StateMachine:
    states: StateTreeNode

    def __init__(self, states: StateTreeNode):
        self.states = states
        self.current_state: Optional[StateTreeNode] = states
        self.state_history = []

    # def add_state(self, state_name, state):
    #     """
    #     Add a state to the state machine.

    #     Parameters:
    #     - state_name: The name of the state.
    #     - state: An object representing the state.
    #     """
    #     self.states[state_name] = state

    # def set_initial_state(self, state_name):
    #     """
    #     Set the initial state of the state machine.

    #     Parameters:
    #     - state_name: The name of the initial state.
    #     """
    #     if state_name in self.states:
    #         self.current_state = state_name
    #         self.state_history.append(state_name)
    #     else:
    #         raise ValueError(f"State '{state_name}' not found.")

    def transition_to(self, state_name):
        """
        Transition to the specified state.

        Parameters:
        - state_name: The name of the target state.
        """
        child_states = self.current_state.get_child_states()
        if child_states != None and len(child_states) > 0:
            self.current_state = self.current_state.find_node_by_state(state_name)
            # self.current_state = state_name
            self.state_history.append(state_name)
        else:
            raise ValueError(f"State '{state_name}' not found.")

    # def execute(self, input):
    #     """
    #     Execute the current state's action.
    #     """
    #     if self.current_state is not None:
    #         return self.current_state.executor.invoke(input)
    #     else:
    #         raise ValueError("No initial state set.")
