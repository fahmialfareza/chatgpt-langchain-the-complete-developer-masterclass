import os
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
