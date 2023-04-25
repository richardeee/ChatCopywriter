import openai
from flask import Flask, request, jsonify, Response
import os
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
import re

from langchain.utilities import BingSearchAPIWrapper
from copywriter.agent.tools.dallehelper import Dalle2Helper
from copywriter.agent.copywriteragent import CopywriterAgent
from copywriter.agent.copywriterprompttemplate import CopywriterPromptTemplate
from copywriter.agent.copywriteroutputparser import CopywriterOutputParser

from dotenv import load_dotenv
load_dotenv()

AZURE_OPENAI_API_KEY_1 = os.environ.get("AZURE_OPENAI_API_KEY_1")
AZURE_OPENAI_API_BASE_1 = os.environ.get("AZURE_OPENAI_API_BASE_1")
AZURE_OPENAI_API_VERSION = os.environ.get("2OPENAI_API_VERSION")
AZURE_CHATGPT_DEPLOYMENT = os.environ.get("AZURE_CHATGPT_DEPLOYMENT")

openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY_1
openai.api_base = AZURE_OPENAI_API_BASE_1
openai.api_version = AZURE_OPENAI_API_VERSION

BING_SUBSCRIPTION_KEY = os.environ.get("BING_SUBSCRIPTION_KEY")
BING_SEARCH_URL =  os.environ.get("BING_SEARCH_URL")

DALLE_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY_2")
DALLE_API_BASE = os.environ.get("AZURE_OPENAI_API_BASE_2")

search = BingSearchAPIWrapper(bing_search_url=str(BING_SEARCH_URL), bing_subscription_key=str(BING_SUBSCRIPTION_KEY))
dalle = Dalle2Helper(DALLE_API_KEY, DALLE_API_BASE)

app = Flask(__name__)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

# @app.route("/generate", methods=["POST"])
# def generate():
#     print("Generateing: " + request.json["title"] + " - " + request.json["title_description"] + " - " + request.json["approach"])
#     approach = request.json["approach"]
#     try:
#         impl = copywrite_approaches.get(approach)
#         if not impl:
#             return jsonify({"error": "unknown approach"}), 400
#         r = impl.run(request.json["title"], request.json["title_description"],request.json.get("overrides") or {})
#         return jsonify(r)
#     except Exception as e:
#         print("Exception in /generate")
#         return jsonify({"error": str(e)}), 500
    
@app.route("/testagent", methods=["POST"])
def generate():
    llm = AzureChatOpenAI(
            openai_api_base=AZURE_OPENAI_API_BASE_1,
            openai_api_version=AZURE_OPENAI_API_VERSION,
            deployment_name='gpt-4',
            openai_api_key=AZURE_OPENAI_API_KEY_1,
            openai_api_type = "azure",
        ) # type: ignore
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    tools = [
            Tool(
                name = "Bing Search",
                func=search.run,
                description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
            ),
            Tool(
                name = "Dalle",
                func=dalle.run,
                description="useful for when you need to generate image. the input to this should be a natural language describing the image."
            )
        ]
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

    tool_names = [tool.name for tool in tools]

    prompt = CopywriterPromptTemplate(
        template=template,
        tools=tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps"]
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    output_parser = CopywriterOutputParser()
    agent = CopywriterAgent(
        llm_chain=llm_chain,
        allowed_tools=tool_names,
        output_parser=output_parser
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
    agent_executor.run("Please help me write a blog about labor's day. Please generate image between each paragraph. Please output in html format.")

if __name__ == "__main__":
    app.run()