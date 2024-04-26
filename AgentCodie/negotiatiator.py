from langchain.agents import initialize_agent, Tool
from langchain.utilities import DuckDuckGoSearchRun
from crewai_agent import CrewAIAgent

# Create a DuckDuckGo search tool
search = DuckDuckGoSearchRun()
tools = [Tool(name="DuckDuckGo Search", func=search.run, description="A DuckDuckGo search tool to find information on the internet.")]

# Initialize the CrewAI agent
agent = CrewAIAgent(tools)

# Define the negotiation prompt
negotiation_prompt = """
You are an experienced negotiator tasked with negotiating the best possible deal for your client. Your goal is to secure the most favorable terms, prices, and conditions for your client.

Negotiation context: [CONTEXT]

Please provide a detailed negotiation strategy outlining the key points you will focus on, the tactics you will employ, and the potential concessions you are willing to make. Also, include any important information or data you will need to gather during the negotiation process.
"""

# Run the agent and obtain the negotiation strategy
context = "Your client is a large retail company looking to negotiate a long-term supply contract with a major electronics manufacturer."
query = negotiation_prompt.replace("[CONTEXT]", context)
negotiation_strategy = agent.run(query)

print(negotiation_strategy)
