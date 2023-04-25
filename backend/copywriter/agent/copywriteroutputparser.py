from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import AzureChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
import re
import os
from langchain.utilities import BingSearchAPIWrapper

class CopywriterOutputParser(AgentOutputParser):
    
    def parse(self, text: str):
        # Add ```json back to the text, since we manually added it as an AIMessage in create_prompt
        return super().parse(f"```json{text}")