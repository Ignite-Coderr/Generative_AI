from dotenv import load_dotenv
import os
from openai import OpenAI
import json

import requests
load_dotenv()

client = OpenAI()


# Tool Function
def get_weather(city: str):
    # TODO: Do an actual API Call
    print("🔧 Tool Called: get_weather", city)

    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong while fetching the weather data."




# Available tools
available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    }
}


system_prompt = """
You are an helpful AI Assistant who is specialized in resolving user query.

You work on start, plan, action, observe mode.

For the given user query and available tools:
- plan the step by step execution
- based on the planning select the relevant tool
- perform the action
- wait for the observation
- then resolve the query.

Rules:
- Follow the Output JSON Format.
- Always perform one step at a time and wait for next input
- Carefully analyse the user query

Output JSON Format:
{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input parameter for the function"
}

Available Tools:
- get_weather: Takes a city name as an input and returns the current weather for the city

Example:

User Query: What is the weather of new york?

Output: {"step": "plan", "content": "User wants weather data"}
Output: {"step": "plan", "content": "I should call get_weather"}
Output: {"step": "action", "function": "get_weather", "input": "new york"}
Output: {"step": "observe", "output": "12 Degree Cel"}
Output: {"step": "output", "content": "Weather in new york is 12 Degree Cel"}
"""


messages = [
    {"role": "system", "content": system_prompt}
]


# User Input
user_query = input("> ")

messages.append({"role": "user", "content": user_query})


while True:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_output = json.loads(response.choices[0].message.content)

    messages.append({
        "role": "assistant",
        "content": json.dumps(parsed_output)
    })


    step = parsed_output.get("step")


    # PLAN STEP
    if step == "plan":
        print(f"💨: {parsed_output.get('content')}")
        continue


    # ACTION STEP
    if step == "action":

        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if tool_name in available_tools:

            print(f"⚙️ Calling Tool: {tool_name}({tool_input})")

            output = available_tools[tool_name]["fn"](tool_input)

            observation = {
                "step": "observe",
                "output": output
            }

            messages.append({
                "role": "assistant",
                "content": json.dumps(observation)
            })

        continue


    # FINAL OUTPUT
    if step == "output":
        print(f"💡: {parsed_output.get('content')}")
        break