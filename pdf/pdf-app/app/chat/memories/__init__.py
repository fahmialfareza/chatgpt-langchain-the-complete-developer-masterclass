from .sql_memory import memory_node_builder
from .window_memory import window_memory_node_builder

memory_map = {
    "sql_buffer_memory": memory_node_builder,
    "sql_window_memory": window_memory_node_builder,
}
