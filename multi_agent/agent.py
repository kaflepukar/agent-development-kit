from google.adk.agents import Agent
from multi_agent.tools.get_time_tool import get_current_time
from multi_agent.sub_agents.stock_analyst.stock_analyst_agent import stock_analyst
from google.adk.tools.agent_tool import AgentTool
from multi_agent.sub_agents.funny_nerd.funny_nerd_agent import funny_nerd
from multi_agent.sub_agents.news_analyst.news_analyst_tool import news_analyst



root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="""
You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - stock_analyst
    - funny_nerd

    You also have access to the following tools:
    - news_analyst
    - get_current_time

""",
sub_agents=[stock_analyst, funny_nerd],
tools = [AgentTool( news_analyst), get_current_time]
)