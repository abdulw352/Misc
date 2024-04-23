from langchain.agents import initialize_agent, Tool
from langchain.utilities import DuckDuckGoSearchRun
from crewai_agent import CrewAIAgent

# Create a DuckDuckGo search tool
search = DuckDuckGoSearchRun()
tools = [Tool(name="DuckDuckGo Search", func=search.run, description="A DuckDuckGo search tool to find information on the internet.")]

# Initialize the CrewAI agent
agent = CrewAIAgent(tools)

# Define the function to format the response as a bulleted list
def format_response(response):
    lines = response.split("\n")
    tasks = [line.strip() for line in lines if line.strip()]
    return "\n".join([f"- {task}" for task in tasks])

# Run the agent and format the response
query = "What do I need to know before buying a car car?"
response = agent.run(query)
formatted_response = format_response(response)

print(formatted_response)
