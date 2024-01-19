import sys
sys.path.append("...")
from main import ML_Agent


config = {"actions": [{"name": "Chat", "situation": "user ask question about tax"}]}

agent = ML_Agent(config)


for line in sys.stdin:
    question = line.strip()
    if "q" == question:
        break
    # The LLM takes a prompt as an input and outputs a completion
    answer = agent.invoke(input=question)

    print(answer)
