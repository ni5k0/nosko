import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


# https://docs.litellm.ai/docs/providers/openrouter
model = LiteLlm(
    model = "openrouter/google/gemini-2.5-pro",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

portfolio_assistant_agent = Agent(
    name="portfolio_assistant_agent",
    model=model,
    description="A portfolio assistant that helps retail investors track their holdings.",
    instruction='''
    You are a portfolio assistant.
    Your name is N🔴sk🟢 (as in Nosko)
    Your first goal is to collect the user's stock portfolio information.
    Start the conversation by asking the user for their stock holdings (ticker symbols) and the number of shares for each.
    You can ask for them one by one or ask the user to list all of them.
    Once you have this information, you can confirm it with the user.
    Do not offer any financial advice.
    ''',
    tools=[],
)

root_agent = portfolio_assistant_agent