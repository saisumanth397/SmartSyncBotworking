from openai import ChatCompletion
from azure.identity import InteractiveBrowserCredential, DefaultAzureCredential, ClientSecretCredential
from .config import *

def ground_data():
    return f"""
You are a helpful assistant
    """

def chattestbot(usr_msg):
    print("\nI am here inside test_2")
    master_instructions=ground_data()
    #cntxt=context()
    messages=[
        {"role": "system", "content": master_instructions},
        {"role": "user", "content": master_instructions+usr_msg}
        ]
    #messages.extend(cntxt)
    messages.append({"role": "user", "content": master_instructions+usr_msg})
    
    #completion = ChatCompletion.create(deployment_id=deployment_id,messages,#temperature=0.2)
    completion = ChatCompletion.create(messages=messages,deployment_id=deployment_id)
    
    respnse=completion['choices'][0]['message']['content']
    usge=completion.usage
    return respnse

#inp=input("Ask me anything : ")
#asw=chattestbot(inp)
#print("bot : ",asw)