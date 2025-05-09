import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")


def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join([row[0] for row in rows if row[0] is not None])


def run_sqlite_query(query: str) -> str:
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred: {str(err)}"


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)


class DescribeTableArgsSchema(BaseModel):
    table_names: List[str]


def describe_table(table_names):
    c = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    rows = c.execute(
        f"SELECT sql from sqlite_master WHERE type='table' AND name IN ({tables})"
    )
    return "\n".join(row[0] for row in rows if row[0] is not None)


describe_table_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, return the schema of those tables",
    func=describe_table,
    args_schema=DescribeTableArgsSchema,
)
