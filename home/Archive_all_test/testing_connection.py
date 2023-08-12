# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 04:09:23 2023

@author: u1111677
"""

import os, time
import openai as p
import pandas as pd
import json
from .config import *
from datetime import datetime
#from input_db import *
pd.set_option('mode.chained_assignment',None)

global messages
 
from openai import ChatCompletion
from azure.identity import InteractiveBrowserCredential, DefaultAzureCredential, ClientSecretCredential

def ground_data():
    return f"""
You are a SmartSyncBot designed to assist users with two specific services. Please note that you should only respond to inquiries related to the following two tasks:

1) Field Mapping Details:
   If a user provides a field name, you are required to check the provided mapping sheet. The mapping sheet serves as your master reference for all field mapping details. Please respond with the exact field mapping of the given field name from all available target systems, including MDM, OM, OCED, and OCEP. Provide information only from the data available in the given sheet for field mapping. Please provide the answer with the available information instead of asking for more details.

2) Sync Check Details:
   If a user provides an entity_id or name, your task is to check the available data to find the exact records from the respective target systems (MDM, OM, OCED, and OCEP) and provide appropriate sync details. You can use the MDM_ID field value to search through all four systems. Upon finding a match, respond with basic sync details along with brief data from the respective target system's source data, including main columns such as id fields, name, country in a tabular format ( Markdown table formatting). You can provide more or all available details for any target system upon request.

You have access to exports from all four systems, namely:
- MDM_source_data for MDM system
- OM_source_data for OM system
- OCED_source_data for OCED system
- OCEP_source_data for OCEP system

These exports serve as your master reference for all sync check related questions, and you should provide exact answers based on the data available in MDM_source_data, OM_source_data, OCED_source_data, and OCEP_source_data.

Please adhere to the following guidelines while responding to user queries:
- If the user explicitly asks for sync details from specific target systems (MDM, OM, OCED, or OCEP), provide information only for the systems mentioned in the user's query.
- If the user does not specify any target system and asks in general, provide sync details for all systems where you were able to find a match. Additionally, provide an appropriate message for target systems where you were unable to find a match.

Remember, your role is to assist users with field mapping and sync check details based on the provided data exports and mapping sheet. Please present your responses in a clear and organized tabular format ( Markdown table formatting) for better readability. Any queries or requests beyond these two tasks are considered out of scope, and you should refrain from responding to such inquiries.

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
MDM  - Country
OM   - Region_code
OCED - Country_cd
OCEP - Country_code """},
{"role": "system", "name":"example_user", "content":
"Give me sync details of Luna Nova"},
{"role": "system", "name": "example_assistant", "content":
"""Sure! Let me check the available data for Luna Nova (MDM_ID : eFgHiJ ) across all target systems.
The sync details for Luna Nova are as follows:
1)MDM
MDM_ID     : eFgHiJ
First_name : Luna
Last_name  : Nova
Country	   : France
2)OM
MDM_ID     : eFgHiJ
First_name : Luna
Last_name  : Nova
Country	   : France
OM_ID	   : 246813579135790
3)OCED
MDM_ID     : eFgHiJ
First_name : Luna
Last_name  : Nova
Country	   : France
OCED_ID	   : eFgHiJ#RD1-MDM
4)OCEP
MDM_ID     : eFgHiJ
First_name : Luna
Last_name  : Nova
Country	   : France
OCEP_ID    : 012340M5qP9sT1c

As per the available information, Luna Nova appears to be synced in all target systems. 
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
{"role": "system", "name":"example_user", "content": "Give me sync details of Luna Nova"},
{"role": "system", "name": "example_assistant", "content": 
{
    "service_name": "sync_check",
    "field_name": "Luna Nova"
}
},

]
    return cont_ident
    
  
def chatbot(usr_prompt,mapping_sheet1='',sync_data_json=''):
    master_instructions=ground_data()
    cntxt=context()
    messages=[
        {"role": "system", "content": master_instructions},
        #{"role": "system", "content": "Your name is Antony's bot"},
        {"role": "system", "name":"Mapping_sheet","content": mapping_sheet1},
        {"role": "system", "content": "Please use the information provided below as a reference to answer the questions related to sync details"},
        {"role": "system","name":"combined_source_data", "content": sync_data_json},
        #{"role": "system","name":"OM_source_data", "content": om_data_json},
        #{"role": "system","name":"OCED_source_data", "content": oced_data_json},
        #{"role": "system", "name":"OCEP_source_data","content": ocep_data_json}
        #{"role": "user", "content": master_instructions+usr_prompt}
        ]
    messages.extend(cntxt)
    messages.append({"role": "user", "content": master_instructions+usr_prompt})
    
    #completion = ChatCompletion.create(deployment_id=deployment_id,messages,#temperature=0.2)
    completion = ChatCompletion.create(messages=messages,deployment_id=deployment_id)
    
    respnse=completion['choices'][0]['message']['content']
    usge=completion.usage
    return respnse,usge
    
def identify_bot(usr_prompt2):
    grd_data=ground_data_for_idnt()
    messages2=[{"role": "system", "content": grd_data},
               {"role": "user", "content": grd_data+usr_prompt2}
              ]
    identification=ChatCompletion.create(messages=messages2,deployment_id=deployment_id)
    
    identfied=identification['choices'][0]['message']['content']
    usg=identification.usage
    
    return identfied,usg
    

    

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
        
def sync_details_fetch(srch_fld,mdm_dt,om_dt,oced_dt,ocep_dt):
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
    
    print("Final sync_db\n",sync_db)
    
    connct.close()
    
    return sync_db

def chattestbot(usr_msg):
    mapping_sheet=""
    print("\I am here inside testing_connection\n")
    master_instructions=ground_data()
    cntxt=context()
    messages=[
        {"role": "system", "content": master_instructions},
        #{"role": "system", "content": "Your name is Antony's bot"},
        {"role": "system", "name":"Mapping_sheet","content": mapping_sheet},
        {"role": "system", "content": "Please use the information provided below as a reference to answer the questions related to sync details"},
        #{"role": "system","name":"combined_source_data", "content": sync_data_json},
        {"role": "system","name":"OM_source_data", "content": om_data_json},
        {"role": "system","name":"OCED_source_data", "content": oced_data_json},
        {"role": "system", "name":"OCEP_source_data","content": ocep_data_json},
        {"role": "user", "content": master_instructions+usr_msg}
        ]
    messages.extend(cntxt)
    messages.append({"role": "user", "content": master_instructions+usr_msg})
    
    #completion = ChatCompletion.create(deployment_id=deployment_id,messages,#temperature=0.2)
    completion = ChatCompletion.create(messages=messages,deployment_id=deployment_id)
    
    respnse=completion['choices'][0]['message']['content']
    usge=completion.usage
    return respnse


try:

    now = datetime.now()
    start_time = time.time()
    start_time1=time.ctime(start_time)
    #print("\nStart Time: ",start_time1,"\n")
  
    ####################-INPUTS-#####################################
    map_sheet_name='mapping_sheet.xlsx'
    mp_sheet_path='Inputs/Mapping_sheet/'
    mp_sht=mp_sheet_path+map_sheet_name
    #mp_sht_pth = os.path.join(os.path.dirname(__file__), 'Inputs/Mapping_sheet/mapping_sheet.xlsx')
    mp_sht_pth = os.path.join(os.path.dirname(__file__), mp_sht)
    mp_sheet=pd.read_excel(mp_sht_pth)
    
    print("\nMapping sheet\n",mp_sheet)
    mp_sheet2=mp_sheet.copy()
    mapping_sheet=mp_sheet2.to_json(orient='records')
    mapping_sheet=mp_sheet2.to_string(index=False)
    
    mdm_export_fl='MDM_export.xlsx'
    om_export_fl='OM_export.xlsx'
    oced_export_fl='OCED_export.xlsx'
    ocep_export_fl='OCEP_export.xlsx'
    export_path='Inputs/Data_exports/'
    mdm_export_pth=export_path+mdm_export_fl
    om_export_pth=export_path+om_export_fl
    oced_export_pth=export_path+oced_export_fl
    ocep_export_pth=export_path+ocep_export_fl
    
    mdm_export_path=os.path.join(os.path.dirname(__file__), mdm_export_pth)
    om_export_path=os.path.join(os.path.dirname(__file__), om_export_pth)
    oced_export_path=os.path.join(os.path.dirname(__file__), oced_export_pth)
    ocep_export_path=os.path.join(os.path.dirname(__file__), ocep_export_pth)
    
    
    mdm_data=pd.read_excel(mdm_export_path)
    om_data=pd.read_excel(om_export_path)
    oced_data=pd.read_excel(oced_export_path)
    ocep_data=pd.read_excel(ocep_export_path)
    
    mdm_data_json=mdm_data.to_json(orient='records')
    om_data_json=om_data.to_json(orient='records')
    oced_data_json=oced_data.to_json(orient='records')
    ocep_data_json=ocep_data.to_json(orient='records')
    
    #print("\nExports\n")
    #print("MDM\n",mdm_data,"\n")
    #print("OM\n",om_data,"\n")
    #print("OCED\n",oced_data,"\n")
    #print("OCEP\n",ocep_data,"\n")

    ##############################- Creating calls to search through the DB-#######################################
    #mapping_sheet_org=mp_sheet.copy()
    mdm_data_og=mdm_data.copy()
    om_data_og=om_data.copy()
    oced_data_og=oced_data.copy()
    ocep_data_og=ocep_data.copy()
    
    
   
    ###########################- testing DB read##########################################
    
    #connec=sqlite3.connect(DB_Name)
    #
    #get_mdm_qry="SELECT * FROM Reltio"
    #get_om_qry="SELECT * FROM Organization_Manager"
    #get_oced_qry="SELECT * FROM OCE_Marketing"
    #get_ocep_qry="SELECT * FROM OCE_Sales"
    #mdm_df=pd.read_sql_query(get_mdm_qry,connec)
    #om_df=pd.read_sql_query(get_om_qry,connec)
    #oced_df=pd.read_sql_query(get_oced_qry,connec)
    #ocep_df=pd.read_sql_query(get_ocep_qry,connec)
    #print("\nMDM FROM DB\n",mdm_df)
    #print("\nOM FROM DB\n",om_df)
    #print("\nOCED FROM DB\n",oced_df)
    #print("\nOCEP FROM DB\n",ocep_df)
    #
    #conn.close()
    
    ########################################################################
    
    
  
    #feedback=[]
    #
    #while(True):
    #
    #    print("\n**************************************************************************************\n")
    #    
    #    #Calling identify_bot
    #    
    #    user_prompt_ident=input("\nSmart_Sync_Bot : How can I help you today?\n\nUser : ")
    #    response_intial,usage_ident=identify_bot(user_prompt_ident)
    #    
    #    if  "service_name" in response_intial:
    #        response_intial=json.loads(response_intial)
    #        print("\nService Identified :" , response_intial["service_name"])
    #        print("SmartSyncBot checking .....\n")
    #        print(response_intial)
    #        print("\nidentify_bot Usage\n",usage_ident,"\n")
    #    else:
    #        print("\nI am here\n")
    #        print(response_intial)
    #        print("\nidentify_bot Usage\n",usage_ident,"\n")
    #    
    #    #Calling chatbot
    #    
    #    if  isinstance(response_intial, dict):
    #        if response_intial["service_name"]=='sync_check':
    #            sync_db_df=sync_details_fetch(response_intial["field_name"],mdm_data_og,om_data_og,oced_data_og,ocep_data_og)
    #            print("Returned sycing result\n" , sync_db_df)
    #            print("Type : ",type(sync_db_df))
    #            sync_db_df=sync_db_df.to_json(orient='records')
    #            print("Type : ",type(sync_db_df))
    #            response,usage=chatbot(user_prompt_ident,sync_data_json=sync_db_df)
    #            print("\nSmart_Sync_Bot :" ,response )
    #            print("\nChat_bot Usage\n",usage,"\n")                
    #        
    #        elif response_intial["service_name"]=='mapping_check':
    #            mp_sht=search_mapping(mp_sheet,response_intial["field_name"])
    #            print("Returned mapping result\n" , mp_sht)
    #            print("Type : ",type(mp_sht))
    #            mp_sht2=mp_sht.to_json(orient='records')
    #            print("Type : ",type(mp_sht2))
    #            response,usage=chatbot(user_prompt_ident,mapping_sheet1=mp_sht2)
    #            print("\nSmart_Sync_Bot :" ,response )
    #            print("\nChat_bot Usage\n",usage,"\n")  
    #        
    #        feedback=[
    #                    {"role": "user","content":user_prompt_ident},
    #                    {"role":"assistant","content":response}
    #                    ]
    #        messages.extend(feedback)
    #    
    #
    #    ch=input("\n\nSmart_Sync_Bot : Do you want to continue (yes/no) ? \n\nUser : ")
    #    if(ch=="no"):
    #        break
    
    
    ######################- testing - ########################
    #inp=input("Ask me anything : ")
    #asw=chattestbot(inp)
    #print("bot : ",asw)
    
    
    #########################################################
  
  
    end_time = time.time()
    end_time1=time.ctime(end_time)
    
    #print("\n\nEnd time: ",end_time1)
    time_taken=end_time-start_time
    #print("Time Taken : ", int(time_taken) ," Seconds")
    time_sec=int(time_taken)
    
    #if time_sec >=60 and time_sec <= 3600 :
    #    print("Time Taken(min) : ", round(time_sec/60 ,2) ," Minute")
    #    
    #elif time_sec > 3600 :
    #    print("Time Taken (hr) : ", round(time_sec/3600 ,2)," Hour")
  
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