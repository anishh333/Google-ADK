from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel,Field
from datetime import date

class Todo(BaseModel):
    task:str=Field(description="task")
    date: str = Field(description="Date in MM-DD-YY format")
    priority:str=Field(description="high,medium,low")

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction = """
        Extract the following information from the user's message:

        - task: name of the task
        - date: scheduled date (YYYY-MM-DD)
        - priority: one of high, medium, or low

        Return only valid JSON matching this schema:

        {
        "task": "",
        "date": "",
        "priority": ""
        }

        If the user does not specify a value, infer it only when reasonable; otherwise leave it empty.
        """,
    output_schema=Todo,
    output_key="task"
)
