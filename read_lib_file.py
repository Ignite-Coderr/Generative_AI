
import os

file_path = r"c:\conda\envs\agentai\Lib\site-packages\euriai\langchain.py"

print(f"Reading file: {file_path}")
if os.path.exists(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines[:200]):
                print(f"{i+1}: {line}", end='')
    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print("File does not exist.")
