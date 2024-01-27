from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain.prompts import PromptTemplate


class AskForEvidence(Tool):
    def __init__(self, action_config={}):
        llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

        situation = action_config.get("situation", "after sales")

        def func(input) -> str:
            describe_after_sales_prompt = """
                You are an after-sales customer service responsible for 
                when {situation}, 
                You need to apologize to the user and ask for proof.\n
                Use Chinese to reply.\n
                User situation: {input}
            """

            describe_after_sales_chain = LLMChain(
                llm=llm,
                prompt=PromptTemplate(
                    template=describe_after_sales_prompt,
                    input_variables=["input"],
                    situation=situation,
                ),
            )

            res = describe_after_sales_chain.invoke({"input": input})
            return res.get("text")

        super().__init__(
            name="Describe the after-sales situation but no evidence",
            func=func,
            description=f"useful for when {situation} and don't provide any evidence.Input should be a brief description of the user situation.",
            return_direct=True,
        )
