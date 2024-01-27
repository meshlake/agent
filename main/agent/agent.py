from typing import Optional
from .simple_agent import SimpleAgent
from utils.state_tree import StateTreeNode
from langchain.memory import ConversationBufferMemory
from actions.state_judgment import StateJudgment
from actions.state_boot import StateBoot
from langchain_core.messages import HumanMessage
import json
import os


class Agent:
    """Agent class."""

    states: StateTreeNode

    current_state: Optional[StateTreeNode]

    state_history = []

    memory: ConversationBufferMemory

    state_judgment: StateJudgment

    state_boot: StateBoot

    def __init__(self, config={}) -> None:
        """Initialize the agent."""
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        self.__init_state(config)

        self.state_judgment = StateJudgment()

        self.state_boot = StateBoot()

    # config convert to state tree
    def __config_to_state(self, config):
        root = StateTreeNode(state=config["situation"], config=config)
        if "actions" in config:
            for action in config["actions"]:
                if action.get("actions") != None and len(action.get("actions")) > 0:
                    child_node = self.__config_to_state(action)
                    root.add_child(child_node)
        return root

    # build state mechine
    def __init_state(self, config):
        state_tree = self.__config_to_state(config)
        state_tree.traverse()
        self.states = state_tree
        self.current_state: Optional[StateTreeNode] = state_tree
        self.state_history = []

    # current state if has next state
    def __is_has_next_state(self) -> bool:
        print(f"__is_has_next_state:{self.current_state.state}")
        child_states = self.current_state.get_child_states()
        return child_states != None and len(child_states) > 0

    def __build_new_memory(self, input):
        new_memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        new_memory.chat_memory.messages = self.memory.chat_memory.messages
        new_memory.chat_memory.add_user_message(HumanMessage(content=input))
        return new_memory

    def __transition_to(self, input):
        new_memory = self.__build_new_memory(input)
        next_states = self.current_state.get_child_states()
        next_state = self.state_judgment.get_next_state(new_memory, next_states)
        print(f"Next state: {next_state}")
        if next_state == "None":
            return (None, new_memory, next_states)
        else:
            self.current_state = self.current_state.find_node_by_state(next_state)
            self.state_history.append(next_state)
            return (self.current_state, new_memory, next_states)
        

    def invoke(self, input):
        print("###########")
        print(input)
        print("###########")
        """Invoke the agent."""

        if self.__is_has_next_state():
            next_state, new_memory, next_states = self.__transition_to(input)


            if next_state == None:
                print("state boot invoke.")
                return self.state_boot.invoke(
                    memory=new_memory, states=next_states, input=input
                )
            else:
                return self.invoke(input)
            

        else:
            config = self.current_state.config
            print("simple agent invoke")

            executor = SimpleAgent(config, self.memory)
            return executor.invoke(input)

    # def __load_config():
    #     # 获取当前脚本所在的目录
    #     current_dir = os.path.dirname(os.path.realpath(__file__))
    #     config_file_path = os.path.join(current_dir, 'config.json')

    #     # 检查文件是否存在
    #     if os.path.exists(config_file_path):
    #         try:
    #             # 读取并解析配置文件
    #             with open(config_file_path, 'r') as file:
    #                 config_data = json.load(file)
    #             return config_data
    #         except json.JSONDecodeError as e:
    #             print(f"Error decoding JSON in config file: {e}")
    #             return None
    #     else:
    #         # 文件不存在，返回 None
    #         return None
