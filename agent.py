import os
import warnings

warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

load_dotenv()

def create_llm():
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError(
            "You need to beg for tokens buddy! ;)"
        )

    endpoint = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        task="conversational",
        huggingfacehub_api_token=hf_token,
        temperature=0.1,
        max_new_tokens=1024,
    )
    llm = ChatHuggingFace(llm=endpoint)
    return llm