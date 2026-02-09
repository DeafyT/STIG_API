import ollama
from .Configurations import configuration
from .Configurations import prompts

model = configuration.ai_model
client = ollama.Client(host=configuration.ai_address)

#Thist function calls the AI to answer questions related to the STIG. Prompt data is stored in prompts.py 
# (inside Configurations). Deliminations are as follows: ***{stig data}***, ---{stig output}---
async def ask_ai(stig_data, question):
    user_prompt = prompts.question_prompt + f'***{stig_data}***' + question
    async for chunk in await ollama.AsyncClient().chat(
        model = model,
        messages = [{'role': 'system', 'content': prompts.sys_prompt}] + [{'role': 'user', 'content': user_prompt}],
        think=False,
        stream=True
    ):
        content = chunk['message']['content']
        if content:
            yield content

#This is a similar function to the one above. However, this one is focused on analyzing the output from a STIG
#check and determining if this meets the STIG requirements.
async def ai_analysis(stig_data, output_data):
    user_prompt = prompts.question_prompt + f'***{stig_data}***' + f'---{output_data}---'
    async for chunk in await ollama.AsyncClient().chat(
        model = model,
        messages = [{'role': 'system', 'content': prompts.sys_prompt}] + [{'role': 'user', 'content': user_prompt}],
        think=False,
        stream=True
    ):
        content = chunk['message']['content']
        if content:
            yield content