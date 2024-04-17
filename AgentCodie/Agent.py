import os
import openai
import re
from typing import List, Tuple
import textwrap

class CodeAnalysisAgent:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.context_window_size = 4096  # Maximum token count for the context window

    def get_llm_response(self, prompt: str) -> str:
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

    def chunk_code(self, code: str) -> List[str]:
        """
        Chunk the code into smaller pieces to fit within the context window.
        """
        chunks = textwrap.wrap(code, width=self.context_window_size, break_long_words=False, replace_whitespace=False)
        return chunks

    def analyze_code(self, code: str) -> Tuple[List[str], List[str]]:
        """
        Analyze the code and return a list of issues and a list of suggested improvements.
        """
        prompt = f"Analyze the following code and provide a list of issues and a list of suggested improvements:\n\n{code}"
        response = self.get_llm_response(prompt)

        # Parse the response to extract the issues and improvements
        issues = []
        improvements = []
        for line in response.split('\n'):
            if line.startswith('Issues:'):
                issues = [issue.strip() for issue in line[len('Issues:'):].split(',')]
            elif line.startswith('Improvements:'):
                improvements = [improve.strip() for improve in line[len('Improvements:'):].split(',')]

        return issues, improvements

    def add_functionality(self, code: str, request: str) -> str:
        """
        Given the existing code and a user request, add the requested functionality.
        """
        prompt = f"Analyze the following code and add the requested functionality:\n\nCode:\n{code}\n\nRequest: {request}"
        response = self.get_llm_response(prompt)
        return response

    def run(self, file_path: str, request: str) -> Tuple[str, List[str], List[str]]:
        """
        Main entry point for the agent.
        1. Read the code from the file.
        2. Chunk the code if necessary.
        3. Analyze the code and get a list of issues and suggested improvements.
        4. Add the requested functionality to the code.
        5. Return the updated code, issues, and improvements.
        """
        with open(file_path, 'r') as file:
            code = file.read()

        # Chunk the code if necessary
        code_chunks = self.chunk_code(code)

        # Analyze the code
        issues, improvements = [], []
        for chunk in code_chunks:
            chunk_issues, chunk_improvements = self.analyze_code(chunk)
            issues.extend(chunk_issues)
            improvements.extend(chunk_improvements)

        # Add the requested functionality
        updated_code = self.add_functionality(code, request)

        return updated_code, issues, improvements

# Example usage
agent = CodeAnalysisAgent(openai_api_key="your_openai_api_key")
file_path = "path/to/your/code/file.py"
request = "Add a function to calculate the factorial of a number."
updated_code, issues, improvements = agent.run(file_path, request)

print("Updated Code:")
print(updated_code)
print("\nIssues:")
print("\n".join(issues))
print("\nImprovements:")
print("\n".join(improvements))