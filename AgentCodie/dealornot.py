from langchain.agents import initialize_agent, Tool
from langchain.utilities import DuckDuckGoSearchRun, WolframAlphaQueryRun
from langchain.llms import OpenAI

# Initialize the search tools
search = DuckDuckGoSearchRun()
wolfram = WolframAlphaQueryRun()

# Create the tools
tools = [
    Tool(name="DuckDuckGo Search", func=search.run, description="A DuckDuckGo search tool to find information on the internet."),
    Tool(name="Wolfram Alpha", func=wolfram.run, description="A Wolfram Alpha tool to compute and analyze data.")
]

# Initialize the agent
llm = OpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="For a given {product} and {price} determine if the product can be found for a lower price", verbose=True)

# Define the function to format the response
def format_response(response):
    lines = response.split("\n")
    return "\n".join([f"- {line.strip()}" for line in lines if line.strip()])

# Run the agent
product = "Apple MacBook Pro 16-inch"
price = 2499

query = f"Is {price} a good deal for a {product}? Provide a detailed analysis and recommendation."
response = agent.run(query)
formatted_response = format_response(response)

print(formatted_response)
