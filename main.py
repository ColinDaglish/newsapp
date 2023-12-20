import pandas as pd
import bs4
import requests
import os
from dotenv import load_dotenv
import time
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import ChatPromptTemplate

# load secrets fron .env file
load_dotenv(".env")


# initialise
llm = OpenAI()
chat_model = ChatOpenAI()

instruction = (
    "List all the countries in the world that are recognised as an "
    "independent state by the United Kingdom"
)

template = """You are a helpful assistant who generates comma separated lists.
A user will pass ask a question and you will return the answer in a comma separated list.
ONLY return a comma separated list, and nothing more."""
human_template = "{text}"


chat_prompt = ChatPromptTemplate.from_messages(
    [("system", template), ("human", human_template)]
)

chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()

country_list = chain.invoke({"text": instruction})

human_template = """List the URLs to the top 10 news organisations in {text}"""

chat_prompt = ChatPromptTemplate.from_messages(
    [("system", template), ("human", human_template)]
)

chain = chat_prompt | ChatOpenAI() | CommaSeparatedListOutputParser()

print(chat_prompt)
urls = {}
for country in country_list:
    urls[country] = chain.invoke({"text": country})
    time.sleep(1)
