from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ReadOnlySharedMemory


class NegotiateCompensation(Tool):
    def __generate_compensation_rules(self, config):
        compensation_rules = ""
        rules = config["rules"]
        for i, rule in enumerate(rules["compensation"]):
            refund_amount = rule["refund_amount"]
            compensation_rules += f"When negotiating with a customer for the {i} time, you need to respond with an apology or a {refund_amount} compensation depending on the seriousness of the customer's situation.\n"
        return compensation_rules

    def __init__(self, readonlymemory, action_config={}):
        llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

        compesation_times = len(action_config["rules"]["compensation"])

        compensation_rules = self.__generate_compensation_rules(action_config)

        def func(input):
            negotiate_compensation_prompt = """
                This is a conversation between a human and a bot:

                {chat_history}

                You are an after-sales customer service responsible for negotiating compensation matters with customers.

                {compensation_rules}

                Please always emphasize to users not to return goods before replying.

                Just reply without explanation.

                New user input: {input}

            """
            negotiate_compensation_chain = LLMChain(
                llm=llm,
                prompt=PromptTemplate(
                    template=negotiate_compensation_prompt,
                    input_variables=["input", "chat_history"],
                ),
                memory=readonlymemory,
            )
            res = negotiate_compensation_chain.invoke(
                {"input": input, "compensation_rules": compensation_rules}
            )
            return res.get("text")

        super().__init__(
            name="Negotiate compensation",
            func=func,
            description=f"useful for when the user provides evidence of after-sales feedback or when it is judged based on the chat history that the user has not negotiated compensation more than {compesation_times}.Input should be the user's new message.",
            return_direct=True,
        )
