from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent


class ChatWithDoc(Tool):
    agent_executor: AgentExecutor = None

    def __doc_embedding(self, doc):
        loader = UnstructuredExcelLoader(doc)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(texts, embeddings)
        return db.as_retriever()

    def __init__(self, readonlymemory, action_config={}):
        llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

        rules = action_config["rules"]
        doc_name = rules["doc"]["name"]
        doc_path = rules["doc"]["path"]
        situation = action_config["situation"]

        def func(input) -> str:
            print(f"ChatWithDoc invoke: {input}")
            res = self.agent_executor.invoke({"input": input})
            return res["output"]

        super().__init__(
            name=f"Query data related to tax issues",
            func=func,
            description=f"must use when user do {situation}.",
            return_direct=True,
        )

        retriever = self.__doc_embedding(doc_path)

        tool = create_retriever_tool(
            retriever,
            f"search_{doc_name}",
            f"Searches and returns excerpts from {doc_name}.",
        )

        tools = [tool]

        prompt = hub.pull("hwchase17/openai-tools-agent")

        agent = create_openai_tools_agent(llm, tools, prompt)

        self.agent_executor = AgentExecutor(agent=agent, tools=tools)

        print("ChatWithDoc init")
