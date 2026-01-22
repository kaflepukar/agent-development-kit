
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from sessions_and_state.question_answering_agent import question_answering_agent

async def main():
    service = InMemorySessionService()
    runner = Runner(agent=question_answering_agent, app_name="test_app", session_service=service)
    
    # Try running without creating session first
    try:
        msg = types.Content(role="user", parts=[types.Part(text="Hi")])
        # This will likely fail or auto-create. Let's see.
        gen = runner.run(user_id="u1", session_id="s1", new_message=msg)
        async for event in gen:
            pass
        print("Runner auto-created session or worked without explicit create check.")
    except Exception as e:
        print(f"Runner failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
