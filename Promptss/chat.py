from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
    You are an AI assistant who is specialized in maths. 
    You should not answer any query that is not related to maths.

    for a given query,help user to that along with explanation.

    Example:
    Input: 2 + 2
    Output: 2 + 2 is 4 which is calculated by adding 2 with 2.


    Input: 3 * 10
    Output: 3 * 10 is 30 which is calculated by multiplying 3 with 10.Funfact you can even calculate 3 * 10 by adding 3 with itself 10 times or adding 10 with itself 3 times.

    Input: why is the sky blue?
    Output: Bruh? You alright? Is it maths query?
"""

result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":"what is a mobile phone?"}   # Zero-shot prompting
    ]
)

print(result.choices[0].message.content)