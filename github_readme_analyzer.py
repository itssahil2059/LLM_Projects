import requests
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("NO API KEY FOUND")
else:
    print("API KEY FOUND")

openai = OpenAI()
model = "gpt-4o-mini"

system_prompt = """
You are an expert in reading and analyzing github README files. You will be given the content of a README file,
and your task is to analyze it and provide insights on its structure, clarity, and effectiveness in conveying information about the project.
- What is the project about?
- What does the Project do?
- Is it doing any contribution to the open source community or is it making any impact in the world?
- Is it using any AI or ML in the project to solve any problem?
- What are the key features of the project?
Keep your analysis clean and answer it clearly in short sentences less than 70 words each. At very last provide the solution in which the 
project can be improved in one or two sentences. Do not provide any other information except the above mentioned points.
"""
def fetch_readme_content(repo_url):
    repo_url = repo_url.rstrip('/')

    parts = repo_url.replace('http://github/com/', '').split('/')
    raw_url = f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/main/README.md"
    try:
        response = requests.get(raw_url)
        if response.status_code == 200:
            return response.text
    except:
        return None

def analyze_readme(repo_url):
    print(f"\nFetching README from: {repo_url}")
    readme_content = fetch_readme_content(repo_url)
    
    if not readme_content:
        print("Failed to fetch ReadME content.")
        return
    
    print("README fetched succesfully. Analyzing...")

    stream = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this README:\n\n{readme_content[:5000]}"}
        ],
        stream = True
    )
    for chunk in stream:
        piece = chunk.choices[0].delta.content or ""
        print(piece, end="", flush=True)
    print("\n\nAnalysis complete.")

if __name__ == "__main__":
    url = input("Enter the github repository URL: ")
    analyze_readme(url)    

