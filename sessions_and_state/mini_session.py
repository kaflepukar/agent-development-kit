from google.adk.sessions import InMemorySessionService, Session


temp_service = InMemorySessionService()

example_session: Session = temp_service.create_session(
    app_name="my_app",
    user_id="example_user",
    state = {"initial_key":"initial_value"}  # state can be initialized

)

print("Examining Session Properties")
print(f"ID : {example_session.id}")
print(f"App Name : {example_session.app_name}")
print(f"User ID : {example_session.user_id}")
print(f"State : {example_session.state}")  # state is a dictionary
print(f"Events : {example_session.events}")  # events is a list
print(f"Last Updated : {example_session.last_update_time}")