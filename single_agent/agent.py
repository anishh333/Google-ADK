from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='Weather_AI',
    description='A helpful assistant for user questions about weather',
    instruction='Answer user questions about weather, its conditions, causes and solutions',
    tools=[google_search]
)
