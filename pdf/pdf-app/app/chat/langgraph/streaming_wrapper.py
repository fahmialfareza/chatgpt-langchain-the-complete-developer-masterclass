from queue import Queue
from threading import Thread
from flask import current_app
from app.chat.callbacks.stream import StreamingHandler
from app.chat.tracing.langfuse import langfuse_handler


class LangGraphStreamWrapper:
    def __init__(self, graph, chat_args):
        self.graph = graph
        self.chat_args = chat_args

    def stream(self, input_text):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()

            stream = self.graph.stream(
                {"input": input_text}, config={"callbacks": [handler, langfuse_handler]}
            )

            for _ in stream:
                pass

            queue.put(None)

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
