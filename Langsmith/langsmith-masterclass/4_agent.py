from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from ddgs import DDGS
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv

load_dotenv()

@tool
def duckduckgo_search(query: str) -> str:
  """Search the web using DuckDuckGo. Use this for general knowledge questions."""
  try:
    with DDGS() as ddgs:
      results = list(ddgs.text(query, max_results=3))
      if not results:
        return "No search results found."
      return "\n\n".join(
        f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}"
        for r in results
      )
  except Exception as e:
    return f"Search failed: {str(e)}"

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  try:
    url = f'https://wttr.in/{city}?format=j1'
    response = requests.get(url, timeout=10)
    data = response.json()

    current = data['current_condition'][0]
    temp_c = current['temp_C']
    temp_f = current['temp_F']
    desc = current['weatherDesc'][0]['value']
    humidity = current['humidity']
    wind_kmph = current['windspeedKmph']

    return (
      f"Weather in {city}: {desc}, "
      f"Temperature: {temp_c}°C ({temp_f}°F), "
      f"Humidity: {humidity}%, "
      f"Wind: {wind_kmph} km/h"
    )
  except Exception as e:
    return f"Failed to fetch weather data for {city}: {str(e)}. Try using duckduckgo_search instead."

llm = ChatOpenAI()

# Step 2: Pull the ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")  # pulls the standard ReAct agent prompt

# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_react_agent(
    llm=llm,
    tools=[duckduckgo_search, get_weather_data],
    prompt=prompt
)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[duckduckgo_search, get_weather_data],
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# What is the release date of Dhadak 2?
# What is the current temp of gurgaon
# Identify the birthplace city of Kalpana Chawla (search) and give its current temperature.

# Step 5: Invoke
response = agent_executor.invoke({"input": "What is the current temp of gurgaon"})
print(response)

print(response['output'])