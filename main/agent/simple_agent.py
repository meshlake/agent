from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.prompts import PromptTemplate
from actions import (
    ask_for_evidence,
    negotiate_compensation,
    stable_message,
    chat,
)
from prompts.react_chat import react_chat


class SimpleAgent(AgentExecutor):
    """Agent class."""

    memory: ConversationBufferMemory

    def __init__(self, config={}, memory: ConversationBufferMemory = None) -> None:
        """Initialize the agent."""
        llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

        if memory is None:
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )

        tools = self.__set_tools(config, memory)

        prompt_template = react_chat

        prompt = PromptTemplate.from_template(prompt_template)

        agent = create_react_agent(llm, tools, prompt)

        super().__init__(agent=agent, tools=tools, verbose=True, memory=memory)

    def __get_tool(self, tool_name, memory, action_config={}):
        readonlymemory = ReadOnlySharedMemory(memory=memory)
        """Get a tool by name."""
        if tool_name == "StableMessage":
            return stable_message.StableMessage(action_config)
        elif tool_name == "AskForEvidence":
            return ask_for_evidence.AskForEvidence()
        elif tool_name == "NegotiateCompensation":
            return negotiate_compensation.NegotiateCompensation(
                readonlymemory, action_config
            )
        elif tool_name == "Chat":
            return chat.Chat(readonlymemory)
        else:
            raise ValueError("Tool not found")

    def __set_tools(self, config, memory):
        tools = []
        for action in config.get("actions", []):
            tool = self.__get_tool(action["name"], memory, action)
            tools.append(tool)
        return tools

    def invoke(self, question: str) -> str:
        """Answer a question."""
        input = f"Use Chinese answer: {question}"
        chat_history = self.memory.chat_memory.messages.__str__()
        res = super().invoke(
            {
                "input": input,
                # Notice that chat_history is a string, since this prompt is aimed at LLMs, not chat models
                "chat_history": chat_history,
            }
        )
        return res.get("output")
