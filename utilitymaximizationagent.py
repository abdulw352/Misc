import os
import openai
import requests
from datetime import datetime
from math import exp

class UtilityMaximizationAgent:
    def __init__(self, openai_api_key, depreciation_rate):
        self.openai_api_key = openai_api_key
        self.depreciation_rate = depreciation_rate

    def get_llm_response(self, prompt):
        openai.api_key = self.openai_api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    def search_web(self, query):
        url = f"https://www.googleapis.com/customsearch/v1?key={os.environ['GOOGLE_API_KEY']}&cx={os.environ['GOOGLE_CX']}&q={query}"
        response = requests.get(url)
        data = response.json()
        return [item['link'] for item in data['items']]

    def calculate_present_value(self, purchase_price, years_owned):
        return purchase_price * exp(-self.depreciation_rate * years_owned)

    def recommend_utilization_strategy(self, good_type, purchase_price, purchase_date):
        # Get information from LLM
        prompt = f"Provide information about the typical usage patterns, depreciation rates, and maintenance requirements for {good_type}."
        llm_response = self.get_llm_response(prompt)

        # Search the web for additional information
        web_search_query = f"{good_type} depreciation, maintenance, usage"
        web_links = self.search_web(web_search_query)

        # Synthesize information and calculate present value
        years_owned = (datetime.now() - purchase_date).days / 365
        present_value = self.calculate_present_value(purchase_price, years_owned)

        # Recommend utilization strategy
        recommendation = f"Based on the information gathered, here is a recommended utilization strategy for your {good_type}:\n\n"
        recommendation += f"- Current present value: ${present_value:.2f}\n"
        recommendation += f"- Typical depreciation rate: {self.depreciation_rate * 100:.2f}% per year\n"
        recommendation += "- Maintenance requirements:\n"
        recommendation += llm_response + "\n"
        recommendation += "- Considering the depreciation and present value, it's recommended to utilize the good in the following way:\n"
        recommendation += "  - Maximize usage to get the most value out of the good before it depreciates further\n"
        recommendation += "  - Explore alternative usage scenarios that can provide additional utility\n"
        recommendation += "  - Invest in necessary maintenance to maintain the good's condition and value\n"
        recommendation += "  - Consider selling the good when the present value is no longer justified by the remaining useful life"

        return recommendation

# Example usage
agent = UtilityMaximizationAgent(openai_api_key="your_openai_api_key", depreciation_rate=0.1)
good_type = "Laptop"
purchase_price = 1200
purchase_date = datetime(2021, 1, 1)
strategy = agent.recommend_utilization_strategy(good_type, purchase_price, purchase_date)
print(strategy)
