from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent


class StateBoot:
    """State Action use for state route."""

    agent_executor: AgentExecutor

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

    def invoke(self, memory: ConversationBufferMemory, states: list[str], input):
        """Invoke the agent."""
        memory_str = self.__memory_to_str(memory)

        states_list_str = ",".join(states)

        input = f"根据聊天记录引导用户咨询以下情景\n 聊天记录：{memory_str} \n有以下几种情景：{states_list_str} \n 用户最新输入：{input} \n 请像聊天一样回复用户，引导用户咨询对应情景"
        
        answer = self.agent_executor.invoke(
            {
                "input": input,
            }
        )
        return answer.get("output")
