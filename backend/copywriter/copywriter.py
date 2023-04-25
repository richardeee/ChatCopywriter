import openai
import os
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import WolframAlphaAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

from dotenv import load_dotenv
load_dotenv()

AZURE_OPENAI_API_KEY_1 = os.environ.get("AZURE_OPENAI_API_KEY_1")
AZURE_OPENAI_API_BASE_1 = os.environ.get("AZURE_OPENAI_API_BASE_1")
AZURE_OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
AZURE_GPT_4_DEPLOYMENT = os.environ.get("AZURE_GPT_4_DEPLOYMENT")
AZURE_GPT_4_32K_DEPLOYMENT = os.environ.get("AZURE_GPT_4_32K_DEPLOYMENT")
AZURE_EMBEDDING_DEPLOYMENT = os.environ.get("AZURE_EMBEDDING_DEPLOYMENT")
AZURE_CHAT_DEPLOYMENT = os.environ.get("AZURE_GPT_CHAT_DEPLOYMENT")

class Copywriter():
    
    def __init__(self, api_key: str, api_base:str, api_version: str, gpt_deployment_name: str):
        self.api_key = api_key
        self.api_base = api_base
        self.api_version = api_version
        self.gpt_deployment_name = gpt_deployment_name
        openai.api_type = "azure"
        openai.api_key = AZURE_OPENAI_API_KEY_1
        openai.api_base = AZURE_OPENAI_API_BASE_1
        openai.api_version = AZURE_OPENAI_API_VERSION
        self.model = AzureChatOpenAI(
            openai_api_base=self.api_base,
            openai_api_version=self.api_version,
            deployment_name=self.gpt_deployment_name,
            openai_api_key=self.api_key,
            openai_api_type = "azure",
        ) # type: ignore
        self.tools = []

    def run(self, question: str, deployment: str, overrides: dict ) :
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        tools = []
        agent_chain = initialize_agent(tools,self.model, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True,memory=memory)
        result = agent_chain.run()
        return {
            'role': 'Copilot',
            'text': result
        }