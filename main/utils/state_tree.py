class StateTreeNode:

    state: str

    def __init__(self, state: str, config=None, parent=None):
        self.state = state
        self.config = config
        self.parent = parent
        self.children = []

    def add_child(self, child_state):
        # 检查是否存在相同状态的节点
        if any(child.state == child_state.state for child in self.children):
            raise ValueError(
                f"Node with state '{child_state}' already exists in the tree."
            )

        self.children.append(child_state)
        return child_state

    def get_all_child_states(self):
        all_states = [self.state]
        for child in self.children:
            all_states.extend(child.get_all_child_states())
        return all_states

    def get_child_states(self):
        child_states = []
        for child in self.children:
            child_states.append(child.state)
        return child_states

    def get_path_to_root(self):
        path = [self.state]
        current_node = self
        while current_node.parent:
            path.append(current_node.parent.state)
            current_node = current_node.parent
        return path

    def find_node_by_state(self, target_state):
        if self.state == target_state:
            return self

        for child in self.children:
            result = child.find_node_by_state(target_state)
            if result:
                return result

        return None

    def traverse(self):
        print(self.state)
        for child in self.children:
            child.traverse()

    def __repr__(self) -> str:
        return f"StateTreeNode(state={self.state})"
