# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 04:09:23 2023

@author: u1111677
"""

import os, time
import openai
import pandas as pd
from config import *
from datetime import datetime

 
from openai import ChatCompletion
from azure.identity import InteractiveBrowserCredential, DefaultAzureCredential, ClientSecretCredential

def training():
    return f"""
    You are a very helpful Bot.
    You provide only two below services , anything not related to the below two numbered points ( 1 and 2 )are out of scope for you and donot answer anything unrelated to below two number of services
    1)You will provide the mapping details , that is the exact field name in all target system (MDM,OM,OCED and OCEP)
    for any respective field name, provided one of the field name is given.
    The mapping sheet provided to you is your master reference for mapping details and provide details that are only  available in the given sheet upon asking for mapping details.
    2)You will provide the sync details , that is whether the record or profile or entity being asked by the user 
    is present (i.e Synced) to all  4 target systems (MDM,OM,OCED and OCEP).
    You can use the MDM_ID field value to search through all 4 systems (MDM,OM,OCED and OCEP) to find whether the entity have synced to the target system. Upon finding a match provide basic sync details along with brief data from the respective 
    target system source data( Intially return only main column like id fields , name,country,etc). You can provide more or all details you have available for any target system when being asked for more.
    The exports from all 4 systems are provided to you as content with name as( MDM_source_data for MDM system , OM_source_data for OM system , OCED_source_data for OCED system , OCEP_source_data for OCEP system) , this is your master reference for all sync check related questions and provide exact answers only based on the data exports available (MDM_source_data,OM_source_data,OCED_source_data,OCEP_source_data).
    If the user is explicitly asking for sync details from only one or set of target systems ( MDM , OM,OCED or OCEP) , you have to provide only for the target systems user is asking.
    If no target system is specified and user is asking in general , please provide sync details for all systems where you were able to find a match and an appropriate message for target system 
    where you were unable to find a match
    """
  
def chatbot(usr_prompt):
    completion = ChatCompletion.create(deployment_id=deployment_id, messages=[
        {"role": "system", "content": training_data},
        {"role": "system", "content": "Your name is Antony's bot"},
        {"role": "system", "name":"Mapping_sheet","content": mapping_sheet},
        {"role": "system", "content": "Please use the information provided below as a reference to answer the questions related to sync details"},
        {"role": "system","name":"MDM_source_data", "content": mdm_data_json},
        {"role": "system","name":"OM_source_data", "content": om_data_json},
        {"role": "system","name":"OCED_source_data", "content": oced_data_json},
        {"role": "system", "name":"OCEP_source_data","content": ocep_data_json},
        {"role": "user", "content": training_data+usr_prompt}
    ])
    
    respnse=completion['choices'][0]['message']['content']
    usge=completion.usage
    return respnse,usge





try:

    now = datetime.now()
    start_time = time.time()
    start_time1=time.ctime(start_time)
    print("\nStart Time: ",start_time1,"\n")
  
    ####################-INPUTS-#####################################
    map_sheet_name='mapping_sheet.xlsx'
    mp_sheet_path='Inputs/Mapping_sheet/'+map_sheet_name
    mp_sheet=pd.read_excel(mp_sheet_path)
    print("\nMapping sheet\n",mp_sheet)
    mp_sheet2=mp_sheet.copy()
    mapping_sheet=mp_sheet2.to_json(orient='records')
    #mapping_sheet=mp_sheet2.to_string(index=False)
    
    mdm_export_fl='MDM_export.xlsx'
    om_export_fl='OM_export.xlsx'
    oced_export_fl='OCED_export.xlsx'
    ocep_export_fl='OCEP_export.xlsx'
    export_path='Inputs/Data_exports/'
    mdm_export_path=export_path+mdm_export_fl
    om_export_path=export_path+om_export_fl
    oced_export_path=export_path+oced_export_fl
    ocep_export_path=export_path+ocep_export_fl
    
    mdm_data=pd.read_excel(mdm_export_path)
    om_data=pd.read_excel(om_export_path)
    oced_data=pd.read_excel(oced_export_path)
    ocep_data=pd.read_excel(ocep_export_path)
    
    mdm_data_json=mdm_data.to_json(orient='records')
    om_data_json=om_data.to_json(orient='records')
    oced_data_json=oced_data.to_json(orient='records')
    ocep_data_json=ocep_data.to_json(orient='records')
    
    print("\nExports\n")
    print("MDM\n",mdm_data,"\n")
    print("OM\n",om_data,"\n")
    print("OCED\n",oced_data,"\n")
    print("OCEP\n",ocep_data,"\n")

    #####################################################################
  
    training_data=training()
    
    while(True):
    
        print("\n**************************************************************************************\n")
        user_prompt=input("\nSmart_Sync_Bot : How can I help you today?\n\nUser : ")
        
        response,usage=chatbot(user_prompt)
        
        print("\nSmart_Sync_Bot :" ,response )
        print("\nUsage\n",usage,"\n")
        #print("Full response :\n" , completion)
        #print("\ntype of response :",type(completion))

        ch=input("\n\nSmart_Sync_Bot : Do you want to continue (yes/no) ? \n\nUser : ")
        if(ch=="no"):
            break
    
  
  
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
  
  
#give this for accuracy 
#Great job so far, these have been perfect  