"""Iterative Story Refinement
Let's build a system with two agents:

Writer Agent - Writes a draft of a short story
Critic Agent - Reviews and critiques the short story to suggest improvements"""

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool

# OpenRouter model via LiteLLM — swap the model string to any OpenRouter model you prefer
# Options: "openrouter/openai/gpt-4o-mini", "openrouter/anthropic/claude-3-haiku",
#          "openrouter/meta-llama/llama-3.3-70b-instruct" (free tier)
OR_MODEL = LiteLlm(model="openrouter/meta-llama/llama-3.3-70b-instruct:free")


def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', 
    indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

print("exit_loop function created.")

# This agent runs only once at beginning for basic draft
basic_draft=Agent(
    name="initial_story",
    model=OR_MODEL,
    instruction="""Write a short story of 100 words based on the user's prompt
    Output only the story text, with no introduction or explanation.""",
    output_key="basic_story"
)

# This is evalution agent used for provide feeback or approval signal

evalute_agent=Agent(
    name="evalution_agent",
    model=OR_MODEL,
    instruction="""You are a strict but fair story editor.
    Story Draft: {basic_story}
    Review the story draft and decide if it meets the user's request.
    - If it's good enough, say: APPROVED
    - If it needs improvement, provide 2-3 specific suggestions.
    Output only your decision and suggestions, nothing else.""",
    output_key="evalution_output"
)

# Now we define the loop
# Loop Agent runs an agent repeatadly based on a condition

refine_agent=Agent(
    name="refine_story",
    model=OR_MODEL,
    instruction="""You are a story refiner.

Story Draft:
{basic_story}

Critique:
{evalution_output}

YOU HAVE EXACTLY ONE FUNCTION AVAILABLE: `exit_loop`
DO NOT call any other function. DO NOT call 'refine_story'. DO NOT call any made-up function.

DECISION RULES:
1. Read the Critique above.
2. IF the Critique contains the word "APPROVED" → call the `exit_loop` function immediately. Output nothing else.
3. IF the Critique contains improvement suggestions → output the improved story text ONLY. Do NOT call any function.""",
    output_key="basic_story",
    tools=[FunctionTool(exit_loop)]
)

story_refinment_loop= LoopAgent(
    name="Story_refinement",
    sub_agents=[evalute_agent,refine_agent],
    max_iterations=2
)
root_agent=SequentialAgent(
    name="root_agent",
    sub_agents=[basic_draft,story_refinment_loop]
)