from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

normal_model = ChatOpenAI(
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.5,
)