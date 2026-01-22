import asyncio
from google.adk.sessions.database_session_service import DatabaseSessionService
from dotenv import load_dotenv
from google.adk.runners import Runner
import uuid
from persistant_memory.memory_agent.agent import memory_agent
from typing import List
from persistant_memory.utils import call_agent_async

load_dotenv()

db_url = "sqlite+aiosqlite:///./memory.db"
session_service = DatabaseSessionService(db_url=db_url)

initial_statte = {

    "user_name": "Kafle Pukar",
    "todos": [],
    
}

async def main():
    APP_NAME = "To Do APP"
    USER_ID = "pukar_kafle"
    SESSION_ID = str(uuid.uuid4())
    all_sessions = await session_service.list_sessions(app_name=APP_NAME, user_id=USER_ID)
    
    if all_sessions and len(all_sessions.sessions) > 0:
        SESSION_ID = all_sessions.sessions[0].id
        print(f"Working on existing sessions:{SESSION_ID}")

    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME, 
            user_id=USER_ID,
            state=initial_statte
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    runner = Runner(
        agent = memory_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print("\nWelcome to Memory Agent Chat!")
    print("Your todos will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)

if __name__ == "__main__":
    asyncio.run(main())