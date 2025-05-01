from langgraph.graph import StateGraph
from langchain_core.messages import (
    BaseMessage,
    get_buffer_string,
    HumanMessage,
    SystemMessage,
)
from app.chat.llms import llm_map
from app.chat.vector_stores import retriever_map
from app.chat.memories import memory_map
from app.chat.models import ChatArgs
from app.web.api import set_conversation_components
from app.chat.memories.histories.sql_history import SqlMessageHistory


def select_component(component_type, component_map, chat_args):
    from app.web.api import get_conversation_components
    from app.chat.score import random_component_by_score

    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)


def llm_node_builder(chat_args, llm, retriever):
    message_history = SqlMessageHistory(conversation_id=chat_args.conversation_id)

    def llm_node(state: dict) -> dict:
        chat_history: list[BaseMessage] = state.get("chat_history", [])
        input_text: str = state.get("input", "")

        new_user_message = HumanMessage(content=input_text)
        chat_context = get_buffer_string(chat_history + [new_user_message])

        # Step 1: Retrieve from vector DB using full chat context
        documents = retriever.invoke(chat_context)

        context_text = "\n\n".join([doc.page_content for doc in documents])
        system_message = SystemMessage(
            content=(
                f"You are a helpful assistant. Use the following PDF context:\n\n{context_text}"
            )
        )

        # Step 2: Final messages for LLM
        messages = [system_message] + chat_history + [new_user_message]

        # Step 3: Run LLM
        response = llm.invoke(messages)

        # Step 4: Persist to memory
        message_history.add_ai_message(response.content)

        return {
            **state,
            "answer": response.content,
            "retriever_documents": documents,
        }

    return llm_node


def build_langgraph_chat(chat_args: ChatArgs):
    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory_node = select_component("memory", memory_map, chat_args)

    llm_node = llm_node_builder(chat_args, llm, retriever)

    graph = StateGraph(dict)
    graph.add_node("memory", memory_node)
    graph.add_node("llm", llm_node)

    graph.set_entry_point("memory")
    graph.add_edge("memory", "llm")
    graph.set_finish_point("llm")

    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        retriever=retriever_name,
        llm=llm_name,
        memory=memory_name,
    )

    return graph.compile()
