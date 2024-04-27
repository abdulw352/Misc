import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.utilities import DuckDuckGoSearchRun
import sqlite3

# Set up OpenAI API key
llm = OpenAI(openai_api_key="YOUR_OPENAI_API_KEY")

# Set up DuckDuckGo search tool
search = DuckDuckGoSearchRun()
tools = [Tool(name="DuckDuckGo Search", func=search.run, description="A DuckDuckGo search tool to find information on the internet.")]

# Initialize the agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Create a SQLite database and table
conn = sqlite3.connect("products.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products
             (product_name TEXT, average_price REAL, description TEXT, sentiment TEXT, pros TEXT, cons TEXT)''')

# List of common products to search for
product_list = ["iPhone", "Samsung Galaxy", "Toyota Camry", "Nike Air Force 1", "Playstation 5", "MacBook Pro", "Levi's Jeans", "Coca-Cola", "Spotify Premium", "Amazon Echo"]

for product in product_list:
    # Perform a search for the product
    query = f"Search for information about the {product} product, including its price, description, consumer sentiment, pros and cons."
    response = agent.run(query)

    # Extract relevant information from the response
    product_info = response.split("\n\n")
    product_name = product
    average_price = [line for line in product_info if "Average price" in line][0].split(":")[1].strip()
    description = [line for line in product_info if "Description" in line][0].split(":")[1].strip()
    sentiment = [line for line in product_info if "Consumer sentiment" in line][0].split(":")[1].strip()
    pros = [line for line in product_info if "Pros" in line][0].split(":")[1].strip()
    cons = [line for line in product_info if "Cons" in line][0].split(":")[1].strip()

    # Insert the product information into the database
    c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", (product_name, average_price, description, sentiment, pros, cons))
    conn.commit()

# Close the database connection
conn.close()
