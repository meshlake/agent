import sys
from agent.agent import Agent as ML_Agent

config = {
    "situation": "tax agent",
    "actions": [
        {
            "name": "DocRetriever",
            "situation": "tax cousulting",
            "rules": {
                "doc": {
                    "name": "tax_data", 
                    "path": "data/tax_data.xlsx", 
                    "lang": "zh-cn"
                }
            },
        }
    ],
}

agent = ML_Agent(config)


for line in sys.stdin:
    question = line.strip()
    if "q" == question:
        break
    # The LLM takes a prompt as an input and outputs a completion
    answer = agent.invoke(question)

    print(answer)
