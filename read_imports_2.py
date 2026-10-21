
try:
    with open(r'c:\conda\envs\agentai\Lib\site-packages\euriai\langchain.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(20, 40):
            if i < len(lines):
                print(f"{i+1}: {lines[i]}", end='')
except Exception as e:
    print(e)
