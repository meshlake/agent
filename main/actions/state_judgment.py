from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent


class StateJudgment:
    """State Action use for state route."""

    agent_executor: AgentExecutor

    def get_next_state(self, memory: ConversationBufferMemory, states: list[str]):
        """Get next state."""

        memory_str = self.__memory_to_str(memory)

        states_list_str = ",".join(states)

        answer = self.agent_executor.invoke(
            {
                "input": f"根据聊天记录判断当前用户在咨询哪种情景的问题\n {memory_str} \n有以下几种情景：{states_list_str} \n 请回复当前用户的情景，如果都不符合请回复None"
            }
        )
        return answer.get("output")

    def __memory_to_str(self, memory: ConversationBufferMemory):
        """Convert memory to string."""
        if memory.buffer_as_str is None:
            memory_str = ""
            for message in memory.chat_memory.messages:
                memory_str += message.content + "\n"
            return memory_str
        else:
            return memory.buffer_as_str

    def __init__(self):
        llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

        prompt = hub.pull("hwchase17/react-chat-json")

        agent = create_json_chat_agent(llm, [], prompt)

        self.agent_executor = AgentExecutor(
            agent=agent, tools=[], verbose=True, handle_parsing_errors=True
        )
