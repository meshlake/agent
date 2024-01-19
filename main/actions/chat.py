from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain_openai import ChatOpenAI


class Chat(Tool):
    def __init__(self, readonlymemory):
        llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

        def func(input) -> str:
            chat_prompt = """
                This is a conversation between a human and a bot:

                {chat_history}

                Have a conversation with a human, answering the following questions as best you can.

                Question: {input}

            """
            chat_prompt_chain = LLMChain(
                llm=llm,
                prompt=PromptTemplate(
                    template=chat_prompt,
                    input_variables=["input", "chat_history"],
                ),
                memory=readonlymemory,
            )
            res = chat_prompt_chain.invoke({"input": input})
            return res.get("text")

        super().__init__(
            name="chat",
            func=func,
            description="useful for when you cannot find the right tool.Input should be the user's new message.",
            return_direct=True,
        )
