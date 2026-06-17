# Sequential multi_agent pipeline: Research → Summarize → Generate Questions
from google.adk.agents.llm_agent import Agent
from google.adk.agents import SequentialAgent

research_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='research_agent',
    description='Researches a topic and presents structured findings.',
    instruction="""You are a specialized research agent.
    The user will provide a topic. Research it thoroughly using your knowledge
    and present the findings in a well-structured format with key facts and details.""",
    output_key="research_output"
)

summarizer_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='summarizer_agent',
    description='Summarizes research findings into concise bullet points.',
    instruction="""You are a specialized summarizer agent.
    Summarize the following research findings into 3-4 concise bullet points.

    Research findings:
    {research_output}""",
    output_key="summarizer_output"
)

question_generator_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='question_generator_agent',
    description='Generates exam-style questions with answers from summarized data.',
    instruction="""You are a specialized exam questions generator agent.
    Based on the summary below, generate 3-5 insightful exam-style questions
    along with their detailed answers.

    Summary:
    {summarizer_output}""",
    output_key="question_generator_output"
)

root_agent = SequentialAgent(
    name="AI_Exam_guide",
    description="Researches a topic, summarizes it, then generates exam questions — in that exact order.",
    sub_agents=[research_agent, summarizer_agent, question_generator_agent]
)
