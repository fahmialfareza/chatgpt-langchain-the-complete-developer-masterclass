from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import (
    ConversationSummaryMemory,
    ConversationBufferMemory,
    FileChatMessageHistory,
)
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

memory = ConversationSummaryMemory(
    memory_key="messages",
    return_messages=True,
    # chat_memory=FileChatMessageHistory("messages.json"),
    llm=chat,
)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ],
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
)

while True:
    content = input(">> ")

    result = chain({"content": content})

    print(result["text"])
