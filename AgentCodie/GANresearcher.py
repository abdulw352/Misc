from langchain.agents import initialize_agent, Tool
from langchain.utilities import DuckDuckGoSearchRun
from langchain.llms import OpenAI
import os

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Set up DuckDuckGo search tool
search = DuckDuckGoSearchRun()
tools = [Tool(name="DuckDuckGo Search", func=search.run, description="A DuckDuckGo search tool to find information on the internet.")]

# Initialize the researcher agent
researcher_llm = OpenAI(temperature=0.7)
researcher_agent = initialize_agent(tools, researcher_llm, agent="zero-shot-react-description", verbose=True)

# Initialize the evaluator agent
evaluator_llm = OpenAI(temperature=0.3)
evaluator_agent = initialize_agent(tools, evaluator_llm, agent="zero-shot-react-description", verbose=True)

# Define the research prompt
research_prompt = """
You are a researcher tasked with finding information about [TOPIC]. Your goal is to provide a thorough and accurate response to the given query.

Query: [QUERY]

Please provide your response, and be prepared to defend or revise your response based on the evaluator's feedback.
"""

# Define the evaluation prompt
evaluation_prompt = """
You are an evaluator tasked with assessing the researcher's response to the following query:

Query: [QUERY]

Researcher's response:
[RESPONSE]

Please provide your evaluation of the researcher's response, identifying any inaccuracies, missing information, or areas for improvement. If the response is satisfactory, state that it is acceptable. Otherwise, provide feedback to the researcher on how to improve the response.
"""

# Function to run the GAN-like research and evaluation process
def run_research_evaluation(topic, query, verbose=False):
    research_query = research_prompt.replace("[TOPIC]", topic).replace("[QUERY]", query)
    response = researcher_agent.run(research_query)

    if verbose:
        print("Researcher's response:")
        print(response)
        print("\n")

    while True:
        evaluation_query = evaluation_prompt.replace("[QUERY]", query).replace("[RESPONSE]", response)
        evaluation = evaluator_agent.run(evaluation_query)

        if "acceptable" in evaluation.lower():
            if verbose:
                print("Evaluator's feedback:")
                print(evaluation)
            break
        else:
            if verbose:
                print("Evaluator's feedback:")
                print(evaluation)
                print("\n")
            research_query = research_prompt.replace("[TOPIC]", topic).replace("[QUERY]", query)
            response = researcher_agent.run(research_query)
            if verbose:
                print("Researcher's updated response:")
                print(response)
                print("\n")

    return response

# Example usage
topic = "Solar energy"
query = "What are the benefits and drawbacks of solar energy?"
verbose = True

final_response = run_research_evaluation(topic, query, verbose)
print("Final response:")
print(final_response)
