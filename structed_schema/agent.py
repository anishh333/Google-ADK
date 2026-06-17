from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel,Field

class sample(BaseModel):
    capital: str=Field(description="captical_name")

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""Extract the capital city from the user query and 
    return it in the format {capital:"captial_name"}.""",
    output_schema=sample,
    output_key="capital"
)
