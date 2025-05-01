from langchain.schema import BaseChatMessageHistory
from app.web.api import get_messages_by_conversation_id, add_message_to_conversation


class SqlMessageHistory(BaseChatMessageHistory):

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id

    def get_messages(self):
        return get_messages_by_conversation_id(self.conversation_id)

    @property
    def messages(self):
        # Add this line so LangChain's `.chat_memory.messages[...]` slicing works
        return self.get_messages()

    def add_message(self, message: str):
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=message.content,
        )

    def clear(self):
        pass
