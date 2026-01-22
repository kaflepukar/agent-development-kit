from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import List

def add_todo(todo:str, tool_context: ToolContext) -> dict:
    """Add a new todo to the user's todo list.

    Args:
        todo: The todo text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
     
    print(f"--- Tool: add_todo called for '{todo}' ---")

    todos: List = tool_context.state.get("todos", [])

    todos.append(todo)

    tool_context.state["todos"] = todos

    return {
        "action": "add_todo",
        "todo": todo,
        "message": f"Added todo: {todo}" 
    }


def view_todos(tool_context: ToolContext) -> dict:
    """ List all todos available for a given session/ runner 
    Args: 
        tool_context: Context for accessing all session state
    
    Returns:
        A list of todos
    """
    print("--- Tool: view_todos called ---")

    todos = tool_context.state.get["todos", []]

    return {
        "action": "veiw_todos", 
        "todos": todos,
        "length of todos": len(todos)
    }


def update_todo(index: int, updated_text:str, tool_context:ToolContext) -> dict:
    """Update an existing todo.

    Args:
        index: The 1-based index of the todo to update
        updated_text: The new text for the todo
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(
        f"--- Tool: update_todos  called for index {index} with '{updated_text}' ---"
    )

    todos = tool_context.state.get("todos",[])
    
    if not todos or index < 1 or index > len(todos):
        return {
            "action": "update_todo",
            "status": "error",
            "message": f"Could not find todo at position {index}. Currently there are {len(todos)} todos.",
        }
    
    old_todo = todos[index -1]
    todos[index - 1] = updated_text
    tool_context.state["todos"] = todos


    return {
        "action": "update_todo",
        "index": index,
        "old_text": old_todo,
        "updated_text": updated_text,
        "message": f"Updated todo {index} from '{old_todo}' to '{updated_text}'",
    }

def delete_todo(index: int, tool_context: ToolContext) -> dict:
    """Delete a todo.

    Args:
        index: The 1-based index of the todo to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: delete_todo called for index {index} ---")

    # Get current todos from state
    todos = tool_context.state.get("todos", [])

    # Check if the index is valid
    if not todos or index < 1 or index > len(todos):
        return {
            "action": "delete_todo",
            "status": "error",
            "message": f"Could not find todo at position {index}. Currently there are {len(todos)} todos.",
        }

    # Remove the todo (adjusting for 0-based indices)
    deleted_todo = todos.pop(index - 1)

    # Update state with the modified list
    tool_context.state["todos"] = todos

    return {
        "action": "delete_todo",
        "index": index,
        "deleted_todo": deleted_todo,
        "message": f"Deleted todo {index}: '{deleted_todo}'",
    }



def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_user_name called with '{name}' ---")

    # Get current name from state
    old_name = tool_context.state.get("user_name", "")

    # Update the name in state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"Updated your name to: {name}",
    }


memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="A smart todo agent with persistent memory",
    instruction="""
    You are a friendly todo assistant that remembers users across conversations.
    
    The user's information is stored in state:
    - User's name: {user_name}
    - todos: {todos}
    
    You can help users manage their todos with the following capabilities:
    1. Add new todo
    2. View existing todos
    3. Update todo
    4. Delete todo
    5. Update the user's name
    
    Always be friendly and address the user by name. If you don't know their name yet,
    use the update_user_name tool to store it when they introduce themselves.
    
    **todo MANAGEMENT GUIDELINES:**
    
    When dealing with todos, you need to be smart about finding the right todo:
    
    1. When the user asks to update or delete a todo but doesn't provide an index:
       - If they mention the content of the todo (e.g., "delete my meeting todo"), 
         look through the todos to find a match
       - If you find an exact or close match, use that index
       - Never clarify which todo the user is referring to, just use the first match
       - If no match is found, list all todos and ask the user to specify
    
    2. When the user mentions a number or position:
       - Use that as the index (e.g., "delete todo 2" means index=2)
       - Remember that indexing starts at 1 for the user
    
    3. For relative positions:
       - Handle "first", "last", "second", etc. appropriately
       - "First todo" = index 1
       - "Last todo" = the highest index
       - "Second todo" = index 2, and so on
    
    4. For viewing:
       - Always use the view_todos tool when the user asks to see their todos
       - Format the response in a numbered list for clarity
       - If there are no todos, suggest adding some
    
    5. For addition:
       - Extract the actual todo text from the user's request
       - Remove phrases like "add a todo to" or "remind me to"
       - Focus on the task itself (e.g., "add a todo to buy milk" → add_todo("buy milk"))
    
    6. For updates:
       - Identify both which todo to update and what the new text should be
       - For example, "change my second todo to pick up groceries" → update_todo(2, "pick up groceries")
    
    7. For deletions:
       - Confirm deletion when complete and mention which todo was removed
       - For example, "I've deleted your todo to 'buy milk'"
    
    Remember to explain that you can remember their information across conversations.

    IMPORTANT:
    - use your best judgement to determine which todo the user is referring to. 
    - You don't have to be 100% correct, but try to be as close as possible.
    - Never ask the user to clarify which todo they are referring to.
    """,
    tools=[
        add_todo,
        view_todos,
        update_todo,
        delete_todo,
        update_user_name,
    ],
)