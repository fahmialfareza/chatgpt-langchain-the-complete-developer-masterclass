from app.chat.langgraph.chat_graph import build_langgraph_chat  # your graph builder
from app.chat.langgraph.streaming_wrapper import LangGraphStreamWrapper


def build_chat(chat_args):
    graph = build_langgraph_chat(chat_args)

    if chat_args.streaming:
        return LangGraphStreamWrapper(graph, chat_args)
    return graph
