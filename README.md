#  Nosko 
A portfolio assistant agent for retail investors to track investment holdings.  

N🔴sk🟢 is Built by a [retail investor](https://x.com/ni5k0) - for retail investors. 

This is a passion project, developed in my spare time. The goal is to give retailers an edge in the agentic era of investment.

# Steps
```
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

pip install google-adk

cd v1_pie_agent 

# modify .replace_with_env file to .env
# Get the API Key in  https://openrouter.ai/

web adk
```

# Agent Versions 
**v1_pie_agent** 
- Simple agent with no database 
- Integration with LiteLLM

**v2_apple_pie_agent**(coming soon)
- local memory (store in your computer)
...

# models
Search models in https://openrouter.ai/

```
model="openrouter/openai/gpt-4.1"
model="openrouter/google/gemini-2.5-pro",
```

# Disclaimer
Nosko is not a financial advisor and does not provide investment advice. Use at your own risk. 
