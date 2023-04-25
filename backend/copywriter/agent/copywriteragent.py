from langchain.agents import Tool
from langchain import LLMChain
from langchain.chat_models import AzureChatOpenAI
from typing import List, Union
from langchain.schema import (
    AgentAction,
    AIMessage,
    BaseLanguageModel,
    BaseMessage,
    BaseOutputParser,
    HumanMessage,
)
from langchain.agents.conversational_chat.base import ConversationalChatAgent
import re
import os
from langchain.utilities import BingSearchAPIWrapper
import os
from typing import Any, List, Optional, Sequence, Tuple
from langchain.tools.base import BaseTool
from langchain.agents.conversational_chat.prompt import (
    PREFIX,
    SUFFIX,
)
from langchain.prompts.base import BasePromptTemplate
from langchain.callbacks.base import BaseCallbackManager
from langchain.agents.agent import Agent, AgentOutputParser

from copywriter.agent.copywriterprompttemplate import CopywriterPromptTemplate
from copywriter.agent.copywriteroutputparser import CopywriterOutputParser
from copywriter.agent.tools.dallehelper import Dalle2Helper


BING_SUBSCRIPTION_KEY = os.environ.get("BING_SUBSCRIPTION_KEY")
BING_SEARCH_URL = os.environ.get("BING_SEARCH_URL")

DALLE_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY_2")
DALLE_API_BASE = os.environ.get("AZURE_OPENAI_API_BASE_2")

search = BingSearchAPIWrapper(bing_search_url=str(BING_SEARCH_URL), bing_subscription_key=str(BING_SUBSCRIPTION_KEY))
dalle = Dalle2Helper()

class CopywriterAgent(ConversationalChatAgent):

    template = """Answer the following questions as best you can, but speaking as a pirate might speak. You have access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

            Question: {input}
            {agent_scratchpad}"""
    
    # def __init__(self, api_key, api_base, api_version, gpt_deployment_name, *args, **kwargs):
        
    #     self.api_key = api_key
    #     self.api_base = api_base
    #     self.api_version = api_version
    #     self.gpt_deployment_name = gpt_deployment_name

    #     self.tools = [
    #         Tool(
    #             name = "Bing Search",
    #             func=search.run,
    #             description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    #         ),
    #         Tool(
    #             name = "Dalle",
    #             func=dalle.run,
    #             description="useful for when you need to generate image. the input to this should be a natural language describing the image."
    #         )
    #     ]
    #     self.prompt = CopywriterPromptTemplate(
    #         template=self.template,
    #         tools=self.tools,
    #         # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    #         # This includes the `intermediate_steps` variable because that is needed
    #         input_variables=["input", "intermediate_steps"]
    #     )
    #     self.output_parser = CopywriterOutputParser()
    #     self.llm = AzureChatOpenAI(
    #         openai_api_base=self.api_base,
    #         openai_api_version=self.api_version,
    #         deployment_name=self.gpt_deployment_name,
    #         openai_api_key=self.api_key,
    #         openai_api_type = "azure",
    #     ) # type: ignore
    #     self.llm_chain = LLMChain(llm = self.llm, prompt=self.prompt)

    output_parser = CopywriterOutputParser()

    def _construct_scratchpad(
            self, intermediate_steps: List[Tuple[AgentAction, str]]
        ) -> List[BaseMessage]:
            thoughts = super()._construct_scratchpad(intermediate_steps)
            # Manually append an AIMessage with the JSON of the intermediate steps
            thoughts.append(AIMessage(content="```json"))
            return thoughts
    
    @classmethod
    def create_prompt(
        cls,
        tools: Sequence[BaseTool],
        system_message: str = PREFIX,
        human_message: str = SUFFIX,
        input_variables: Optional[List[str]] = None,
        output_parser: Optional[BaseOutputParser] = None,
    ) -> BasePromptTemplate:
        return super().create_prompt(
            tools,
            system_message,
            human_message,
            input_variables,
            output_parser or CopywriterOutputParser(),
        )
    
    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        callback_manager: Optional[BaseCallbackManager] = None,
        system_message: str = PREFIX,
        human_message: str = SUFFIX, # modify human_message to accept either a string or a list of strings
        input_variables: Optional[List[str]] = None,
        output_parser: Optional[AgentOutputParser] = None,
        **kwargs: Any,
    ) -> Agent:
        return super().from_llm_and_tools(
            llm=llm,
            tools=tools,
            callback_manager=callback_manager,
            system_message=system_message,
            human_message=human_message,
            input_variables=input_variables,
            output_parser=output_parser or CopywriterOutputParser(),
            **kwargs,
        )