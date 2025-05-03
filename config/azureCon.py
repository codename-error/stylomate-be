import base64
import os
from dotenv import load_dotenv
import requests
from langchain_openai import AzureChatOpenAI, AzureOpenAI
from langchain.schema import HumanMessage, AIMessage

load_dotenv()

def setup_openai_chat(model_name):
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY tidak ditemukan di .env")
    
    return AzureChatOpenAI(
        api_key="GExcK7DeWyNIOOsqck2ggm5dSTn13OqzYt2Y38LFNPPGgN1HPC5yJQQJ99BEACfhMk5XJ3w3AAAAACOGpWvg",
        api_version="2024-12-01-preview",
        azure_endpoint="https://muham-ma695f75-swedencentral.cognitiveservices.azure.com/",
        deployment_name=model_name,
        temperature=1,
        max_tokens=4096
    )