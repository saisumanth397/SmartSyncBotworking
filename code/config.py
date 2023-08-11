# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 02:43:56 2023

@author: u1111677
"""

import openai
from azure.identity import InteractiveBrowserCredential, DefaultAzureCredential, ClientSecretCredential



try:


  ad_programmatic_scope = "api://2a459df9-d8e1-43e0-998e-320abbe581d0/.default"
  deployment_id = "deployment-ac1a68648c60427a957606598b973057"
  openai.api_type = "azure_ad"
  openai.api_base = "http://openai.work.iqvia.com/cse/prod/proxy/azure/az-cs-eaus-dpo-openai-gpt-demo-d01"
  openai.api_version = "2023-03-15-preview"
  credentials = DefaultAzureCredential()
  token = credentials.get_token(ad_programmatic_scope)
  openai.api_key = token.token
  
  
except Exception as e:
    print("\nError in configuration \n",e)