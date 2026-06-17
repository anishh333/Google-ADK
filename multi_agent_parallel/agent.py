# Create a parallel agents for tech researcher,health researcher,finanace researcher
# Aggregator is used to combine the result of all the agents
# Create parallel agent for finance researcher
from google.adk.agents import Agent,ParallelAgent,SequentialAgent

finance_researcher = Agent(
    model='gemini-2.5-flash-lite',
    name='finance_researcher',
    instruction="""Research current fintech trends. Include 3 key trends,
        their market implications, and the future outlook. 
        Keep the report concise (50 words).""",
    output_key="finance_findings"
)
# Create parallel agent for health researcher
health_researcher = Agent(
    model='gemini-2.5-flash-lite',
    name='health_researcher',
    instruction="""Research recent breakthroughs in longevity medicine or gene editing. Include 
        the core innovation, the top 2 research groups working on it, and the projected timeline 
        for human trials. Keep the summary focused and concise (around 50 words).""",
    output_key="health_findings"
)
# Create parallel agent for tech researcher
tech_researcher = Agent(
    model='gemini-2.5-flash-lite',
    name='tech_researcher',
    instruction="""Research the latest AI/ML trends. Include 3 key developments,
        the main companies involved, and the potential impact. 
        Keep the report very concise (50 words)""",
    output_key="tech_findings"
)
# Create aggregator agent
aggregator = Agent(
    model='gemini-2.5-flash-lite',
    name='aggregator',
    instruction="""Combine the following research findings into a single comprehensive report.
        Include key insights from each area.

        Finance findings: {finance_findings}
        Health findings: {health_findings}
        Tech findings: {tech_findings}""",
    output_key="combined_report"
)

parallel_agent=ParallelAgent(
    name="parallel_agents",
    sub_agents=[finance_researcher,health_researcher,tech_researcher],
)

root_agent=SequentialAgent(
    name="Research_System",
    sub_agents=[parallel_agent,aggregator]
)

