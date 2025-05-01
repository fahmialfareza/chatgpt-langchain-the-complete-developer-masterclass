from app.chat.tracing.langfuse import langfuse_handler


class TraceableChain:
    def __call__(self, *args, **kwargs):
        try:
            callbacks = kwargs.get("callbacks", [])
            callbacks.append(langfuse_handler)
            kwargs["callbacks"] = callbacks
        except Exception as e:
            print("Langfuse tracing failed:", e)

        # Forward to actual ConversationalRetrievalChain constructor
        super().__call__(*args, **kwargs)
