# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 04:09:23 2023
name of original code : SmartSyncBot_V9_making_fn_for_UI
@author: u1111677
"""

import os, time
import openai as p
import pandas as pd
import json
from .config import *
from datetime import datetime
from .input_db_v2 import *
pd.set_option('mode.chained_assignment',None)

#global messages
 
from openai import ChatCompletion
from azure.identity import InteractiveBrowserCredential, DefaultAzureCredential, ClientSecretCredential

def ground_data():
    return f"""
You are a SmartSyncBot designed to assist users with two specific services. Please note that you should only respond to inquiries related to the following two tasks:

1) Field Mapping Details:
   If a user provides a field name, you are required to check the provided mapping sheet. The mapping sheet serves as your master reference for all field mapping details. Please respond with the exact field mapping of the given field name from all available target systems, including MDM, OM, OCED, and OCEP. Provide information only from the data available in the given sheet for field mapping. Please provide the answer with the available information instead of asking for more details.The final ouput of mapping details check requires only two columns with headers 
   Source_system and Field_name

2) Sync Check Details:
   If a user provides an entity_id or name, your task is to check the available data to find the exact records from the respective target systems (MDM, OM, OCED, and OCEP) and provide appropriate sync details. You can use the MDM_ID field value to search through all four systems. Upon finding a match, respond with basic sync details along with brief data from the respective target system's source data, including main columns such as id fields, name, country in a tabular format ( Give the tabular data such a way that table structure is returned as html tags). You can provide more or all available details for any target system upon request.

You have access to exports from all four systems, namely:
- MDM_source_data for MDM system
- OM_source_data for OM system
- OCED_source_data for OCED system
- OCEP_source_data for OCEP system

These exports serve as your master reference for all sync check related questions, and you should provide exact answers based on the data available in MDM_source_data, OM_source_data, OCED_source_data, and OCEP_source_data.

Please adhere to the following guidelines while responding to user queries:
- If the user explicitly asks for sync details from specific target systems (MDM, OM, OCED, or OCEP), provide information only for the systems mentioned in the user's query.
- If the user does not specify any target system and asks in general, provide sync details for all systems where you were able to find a match. Additionally, provide an appropriate message for target systems where you were unable to find a match.

Remember, your role is to assist users with field mapping and sync check details based on the provided data exports and mapping sheet. Please present your responses in a clear and organized tabular format ( Give the tabular data such a way that table structure is returned as html tags) for better readability. Any queries or requests beyond these two tasks are considered out of scope, and you should refrain from responding to such inquiries.

Please provide answer with the available instruction instead of asking for more details 
If the user does not specify any target system and asks in general, provide sync details for all systems where you were able to find a match 

Now, please proceed with the defined tasks and provide helpful responses to users accordingly.
    """
    
def ground_data_for_idnt():
    return """
You are SmartSyncBot. Your primary purpose is to provide two services as defined below. If the user asks you a question that is not related to the below two services, politely inform them that it is beyond your scope.

Context:
1) Field Mapping Details
    Step 1: If the user asks for mapping details of any particular field, identify it as a mapping service.
    Step 2: Determine the field name for which the user wants you to check the mapping details.
    Step 3: Formulate your final JSON response, combining the service_name and field_name identified in the previous steps in the following format:
        {
            "service_name": "mapping_check",
            "field_name": "identified_field_name"
        }
    Step 4: Provide your response following the above steps.Your response must always be in the form of json as defined in step3.

2) Sync Check Details
    Step 1: If the user asks for sync details of any particular field, identify it as a sync service.
    Step 2: Identify the field name for which the user is asking for sync details.
    Step 3: Formulate your final JSON response, combining the service_name and field_name identified in the previous steps in the following format:
        {
            "service_name": "sync_check",
            "field_name": "identified_field_name"
        }
    Step 4: Provide your response following the above steps.Your response must always be in the form of json as defined in step3.

Remember, your response should always be a JSON containing only two objects as described in the above steps.
    """
    
def context():
    cont=[
{"role": "system", "name":"example_user", "content": "Give me mapping for Country"},
{"role": "system", "name": "example_assistant", "content": """Sure! Let me check the mapping sheet for the field 'Country' across all target systems.
The field mapping details are as follows:
<!DOCTYPE html> <html> <head> <style> body { font-family: Tahoma, Geneva, sans-serif; } table { border-collapse: collapse; } table td { padding: 15px; } table thead th { background-color: #54585d; color: #ffffff; font-weight: bold; font-size: 13px; border: 1px solid #54585d; padding: 5px; } table tbody td { color: #636363; border: 1px solid #dddfe1; } table tbody tr { background-color: #f9fafb; } table tbody tr:nth-child(odd) { background-color: #ffffff; } </style> </head> <body> <table> <thead> <tr> <th>Source System</th> <th>Field Name</th> </tr> </thead> <tbody> <tr> <td>MDM</td> <td>Country</td> </tr> <tr> <td>OM</td> <td>Region_code</td> </tr> <tr> <td>OCED</td> <td>Country_cd</td> </tr> <tr> <td>OCEP</td> <td>Country_code</td> </tr> </tbody> </table> </body> </html>
"""},
{"role": "system", "name":"example_user", "content":
"Give me sync details of Luna"},
{"role": "system", "name": "example_assistant", "content":
"""Sure! Let me check the available data for Luna(MDM_ID : eFgHiJ ) across all target systems.
The sync details for Luna Nova are as follows:
<!DOCTYPE html> <html> <head> <style> body { font-family: Tahoma, Geneva, sans-serif; } table { border-collapse: collapse; } table td { padding: 15px; } table thead th { background-color: #54585d; color: #ffffff; font-weight: bold; font-size: 13px; border: 1px solid #54585d; padding: 5px; } table tbody td { color: #636363; border: 1px solid #dddfe1; } table tbody tr { background-color: #f9fafb; } table tbody tr:nth-child(odd) { background-color: #ffffff; } </style> </head> <body> <table> <thead> <tr> <th>Target System</th> <th>MDM_ID</th> <th>Name</th> <th>Country</th> <th>OM_ID</th> <th>OCED_ID</th> <th>OCEP_ID</th> </tr> </thead> <tbody> <tr> <td>MDM</td> <td>eFgHiJ</td> <td>Luna</td> <td>France</td> <td>N/A</td> <td>N/A</td> <td>N/A</td> </tr> <tr> <td>OM</td> <td>eFgHiJ</td> <td>Luna</td> <td>France</td> <td>246813579135790</td> <td>N/A</td> <td>N/A</td> </tr> <tr> <td>OCED</td> <td>eFgHiJ</td> <td>Luna</td> <td>France</td> <td>N/A</td> <td>eFgHiJ#RD1-MDM</td> <td>N/A</td> </tr> <tr> <td>OCEP</td> <td>eFgHiJ</td> <td>Luna</td> <td>France</td> <td>N/A</td> <td>N/A</td> <td>012340M5qP9sT1c</td> </tr> </tbody> </table> </body> </html>

As per the available information, Luna appears to be synced in all target systems. 
Let me know if you need any further information. """}
]
    return cont
    
def context_for_ident():
    cont_ident=[
{"role": "system", "name":"example_user", "content": "Give me mapping for Country"},
{"role": "system", "name": "example_assistant", "content": 
{
    "service_name": "mapping_check",
    "field_name": "Country"
}
},
{"role": "system", "name":"example_user", "content": "Give me sync details of Luna"},
{"role": "system", "name": "example_assistant", "content": 
{
    "service_name": "sync_check",
    "field_name": "Luna"
}
},

]
    return cont_ident
    
  
def chatbot(usr_prompt,mapping_sheet1='',sync_data_json=''):
    master_instructions=ground_data()
    cntxt=context()
    messages=[
        {"role": "system", "content": master_instructions},
        {"role": "system", "name":"Mapping_sheet","content": mapping_sheet1},
        {"role": "system", "content": "Please use the information provided below as a reference to answer the questions related to sync details"},
        {"role": "system","name":"combined_source_data", "content": sync_data_json}
        ]
    messages.extend(cntxt)
    messages.append({"role": "user", "content": master_instructions+usr_prompt})
    
    #completion = ChatCompletion.create(deployment_id=deployment_id,messages,#temperature=0.2)
    completion = ChatCompletion.create(messages=messages,deployment_id=deployment_id)
    
    respnse=completion['choices'][0]['message']['content']
    usge=completion.usage
    print("\nChat_bot Usage\n",usge,"\n")
    return respnse
    
def identify_bot(usr_prompt2):
    grd_data=ground_data_for_idnt()
    messages2=[{"role": "system", "content": grd_data},
               {"role": "user", "content": grd_data+usr_prompt2}
              ]
    identification=ChatCompletion.create(messages=messages2,deployment_id=deployment_id)
    
    identfied=identification['choices'][0]['message']['content']
    usg=identification.usage
    print("\nidentify_bot Usage\n",usg,"\n")
    
    return identfied
    

    

def search_mapping(mp_sheet,srch_field): 

    result_df = mp_sheet[mp_sheet.applymap(lambda x: str(x).lower() == srch_field.lower()).any(axis=1)]
    if result_df.empty:
        print("\nNo matching records found.") # comment this later
        result_df=pd.DataFrame()
        return result_df
        
    else:
        print("\nMatching records found:") # comment this later
        print(result_df)                    # comment this later
        return result_df
        
        
def get_mdm_data(id_fld):
	return f"""select * from Reltio
               where mdm_id='{id_fld}' 
               or lower(name)=lower('{id_fld}') """
        
def get_om_data(id_nam):
    return f""" select * from Organization_Manager
                where mdm_id='{id_nam}'
            """
def get_oced_data(id_nam):
    return f""" select * from OCE_Marketing
                where mdm_id='{id_nam}'
            """
def get_ocep_data(id_nam):
    return f""" select * from OCE_Sales
                where mdm_id='{id_nam}'
            """
        
def sync_details_fetch(srch_fld):
    mdm_result = pd.DataFrame({'Source_system_name': ['MDM']})
    om_result = pd.DataFrame({'Source_system_name': ['OM']})
    oced_result = pd.DataFrame({'Source_system_name': ['OCED']})
    ocep_result = pd.DataFrame({'Source_system_name': ['OCEP']})
    
    connct=sqlite3.connect(DB_Name)
    
    mdm_qry=get_mdm_data(srch_fld)
    mdm_result=pd.read_sql_query(mdm_qry,connct)
    
    
    
    if mdm_result.empty:
        print("\nNo match in MDM for ",srch_fld)
        #mdm_result = pd.DataFrame({'Source_system_name': ['MDM']})
        mdm_result['Source_system_name']=['MDM']
    else:
        mdm_id_fund=mdm_result["MDM_ID"].iloc[0]
        print("\nMatch found for MDM ID : ",mdm_id_fund,"\n")
        print(mdm_result)
        
        om_qry=get_om_data(mdm_id_fund)
        oced_qry=get_oced_data(mdm_id_fund)
        ocep_qry=get_ocep_data(mdm_id_fund)
        om_result=pd.read_sql_query(om_qry,connct)
        oced_result=pd.read_sql_query(oced_qry,connct)
        ocep_result=pd.read_sql_query(ocep_qry,connct)
    
    if om_result.empty:
        om_result['Source_system_name']=['OM']
    if oced_result.empty:
        oced_result['Source_system_name']=['OCED']
    if ocep_result.empty:
        ocep_result['Source_system_name']=['OCEP']
    
    mdm_result['Source_system_name']=['MDM']
    om_result['Source_system_name']=['OM']
    oced_result['Source_system_name']=['OCED']
    ocep_result['Source_system_name']=['OCEP']
    
    sync_db=pd.concat([mdm_result,om_result,oced_result,ocep_result],axis=0)
    sync_db=sync_db.reset_index(drop=True)
    
    print("\nFinal sync_db\n",sync_db)
    
    connct.close()
    
    return sync_db
    
def smartsyncbot(user_prompt):   
        
    #Calling identify_bot
    
    #user_prompt_ident=input("\nSmart_Sync_Bot : How can I help you today?\n\nUser : ")
    response_intial=identify_bot(user_prompt)
    
    if  "service_name" in response_intial:
        response_intial=json.loads(response_intial)
        print("\nService Identified :" , response_intial["service_name"])
        print("SmartSyncBot checking .....\n")
        print(response_intial)
        #print("\nidentify_bot Usage\n",usage_ident,"\n")
    else:
        print("\nI am here\n")
        print(response_intial)
        
        return response_intial
        #print("\nidentify_bot Usage\n",usage_ident,"\n")
    
    #Calling chatbot
    
    if  isinstance(response_intial, dict):
        if response_intial["service_name"]=='sync_check':
            sync_db_df=sync_details_fetch(response_intial["field_name"]) #search function to get the necessary imports from systems
            print("\nReturned sycing result\n" , sync_db_df)
            #print("Type : ",type(sync_db_df))
            sync_db_df=sync_db_df.to_json(orient='records')
            #print("Type : ",type(sync_db_df))
            response=chatbot(user_prompt,sync_data_json=sync_db_df)
            print("\nSmart_Sync_Bot :" ,response )
            #print("\nChat_bot Usage\n",usage,"\n")                
        
        elif response_intial["service_name"]=='mapping_check':
            mp_sht=search_mapping(mp_sheet,response_intial["field_name"])
            print("\nReturned mapping result\n" , mp_sht)
            #print("Type : ",type(mp_sht))
            mp_sht2=mp_sht.to_json(orient='records')
            #print("Type : ",type(mp_sht2))
            response=chatbot(user_prompt,mapping_sheet1=mp_sht2)
            print("\nSmart_Sync_Bot :" ,response )
            #print("\nChat_bot Usage\n",usage,"\n")  
    
    return response



try:

    now = datetime.now()
    start_time = time.time()
    start_time1=time.ctime(start_time)
    print("\nStart Time: ",start_time1,"\n")
  
 
    ###############################################################################################################################  
    # - UNCOMMENT THIS FOR INDIVIDUAL CODE TESTING -##
    #usr=input("\nWhat Can I do for you ?\n")
    #rsp=smartsyncbot(usr)
    #print("\nSmart Sync Bot\n",rsp,"\n")
  
  
  
  
    ###############################################################################################################################
    end_time = time.time()
    end_time1=time.ctime(end_time)
    
    print("\n\nEnd time: ",end_time1)
    time_taken=end_time-start_time
    print("Time Taken : ", int(time_taken) ," Seconds")
    time_sec=int(time_taken)
    
    if time_sec >=60 and time_sec <= 3600 :
        print("Time Taken(min) : ", round(time_sec/60 ,2) ," Minute")
        
    elif time_sec > 3600 :
        print("Time Taken (hr) : ", round(time_sec/3600 ,2)," Hour")
  
except Exception as e:
  print("\nError\n",e)
  
except p.error.AuthenticationError as ae:
    # Catch and handle the specific AuthenticationError
    print("\nAuthenticationError: ", ae)

except p.error as ope:
    print("\nOpenAI Error\n", ae)
    
except p.error.APIError as api:
  #Handle API error, e.g. retry or log
  print("\nOpenAI API returned an API Error\n",api)
  
  
#give this for accuracy 
#Great job so far, these have been perfect  