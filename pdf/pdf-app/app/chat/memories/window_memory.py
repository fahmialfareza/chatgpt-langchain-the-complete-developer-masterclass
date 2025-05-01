from app.chat.memories.histories.sql_history import SqlMessageHistory


def window_memory_node_builder(chat_args, k=2):
    message_history = SqlMessageHistory(conversation_id=chat_args.conversation_id)

    def memory_node(state: dict) -> dict:
        input_text = state.get("input")
        if input_text:
            message_history.add_user_message(input_text)

        history = message_history.load_memory(k=k)
        return {**state, "chat_history": history}

    return memory_node
