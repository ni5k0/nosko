import asyncio
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

load_dotenv()

# https://docs.litellm.ai/docs/providers/openrouter
model = LiteLlm(
    model="openrouter/google/gemini-2.5-pro",
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

# ===== PART 1: Initialize Persistent Session Service =====

# Using SQLite database for persistent storage
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)


# ===== PART 2: Define Initial State =====
# This will only be used when creating a new session
initial_state = {
    "user_name": "nisko",
    "portfolio": {},
}

async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
#   print(f"\n>>> User Query: {query}")

  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      # You can uncomment the line below to see *all* events during execution
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  print(f"<<< Agent Response: {final_response_text}")


async def main_async():
    # Setup constants
    APP_NAME = "Portfolio Assistant"
    USER_ID = "ni5k0"

    # ===== PART 3: Session Management - Find or Create =====
    # Check for existing sessions for this user
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # If there's an existing session, use it, otherwise create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Use the most recent session
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create a new session with initial state
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # ===== PART 4: Agent Runner Setup =====
    # Create a runner with the memory agent
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Conversation Loop =====
    print("\nI'm N🔴sk🟢 , Welcome to Portfolio Assistant CHAT! ")
    print("Your portfolio will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break


        # Process the user query through the agent
        await call_agent_async(user_input, runner, USER_ID, SESSION_ID)
        # print(f"Session ID: {SESSION_ID}")


if __name__ == "__main__":
    asyncio.run(main_async())