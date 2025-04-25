from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel


class WriteReportArgs(BaseModel):
    filename: str
    html: str


def write_report(filename, html):
    with open(filename, "w") as f:
        f.write(html)


write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML file to disk. Use this tool whenever someone asks for a report.",
    func=write_report,
    args_schema=WriteReportArgs,
)
