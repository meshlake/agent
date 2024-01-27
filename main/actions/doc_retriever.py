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
from langchain_core.retrievers import BaseRetriever
from langchain_core.pydantic_v1 import BaseModel, Field


class RetrieverInput(BaseModel):
    """Input to the retriever."""

    query: str = Field(description="query to look up in retriever")


class DocRetriever(Tool):
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

        rules = action_config["rules"]
        doc_name = rules["doc"]["name"]
        doc_path = rules["doc"]["path"]
        situation = action_config["situation"]

        retriever: BaseRetriever = self.__doc_embedding(doc_path)

        super().__init__(
            name=f"Query data related to tax issues",
            description=f"must use when user do {situation}.",
            func=retriever.get_relevant_documents,
            coroutine=retriever.aget_relevant_documents,
            args_schema=RetrieverInput,
        )
