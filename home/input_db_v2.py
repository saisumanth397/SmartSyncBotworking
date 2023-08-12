
import os, time
import pandas as pd
import json
from datetime import datetime
import sqlite3


try:

    #now = datetime.now()
    #start_time = time.time()
    #start_time1=time.ctime(start_time)
    #print("\nStart Time: ",start_time1,"\n")
  
    ####################-INPUTS-#####################################    
    map_sheet_name='mapping_sheet.xlsx'
    mp_sheet_path='Inputs/Mapping_sheet/'
    mp_sht=mp_sheet_path+map_sheet_name
    #mp_sht_pth = os.path.join(os.path.dirname(__file__), 'Inputs/Mapping_sheet/mapping_sheet.xlsx')
    mp_sht_pth = os.path.join(os.path.dirname(__file__), mp_sht)
    mp_sheet=pd.read_excel(mp_sht_pth)
    #print("\nMapping sheet\n",mp_sheet)
    
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
    
    
    #####################- Setting up DB -############################
    
    DB_Name='Data_Repository'
    conn=sqlite3.connect(DB_Name)
    cursor=conn.cursor()
    
    mdm_table_name='Reltio'
    om_table_name='Organization_Manager'
    oced_table_name='OCE_Marketing'
    ocep_table_name='OCE_Sales'
    
    mdm_data.to_sql(mdm_table_name, conn, index=False, if_exists='replace')
    om_data.to_sql(om_table_name, conn, index=False, if_exists='replace')
    oced_data.to_sql(oced_table_name, conn, index=False, if_exists='replace')
    ocep_data.to_sql(ocep_table_name, conn, index=False, if_exists='replace')
    conn.commit()
    
    #get_mdm_qry="SELECT * FROM Reltio"
    #get_om_qry="SELECT * FROM Organization_Manager"
    #get_oced_qry="SELECT * FROM OCE_Marketing"
    #get_ocep_qry="SELECT * FROM OCE_Sales"
    #mdm_df=pd.read_sql_query(get_mdm_qry,conn)
    #om_df=pd.read_sql_query(get_om_qry,conn)
    #oced_df=pd.read_sql_query(get_oced_qry,conn)
    #ocep_df=pd.read_sql_query(get_ocep_qry,conn)
    #print("\nMDM FROM DB\n",mdm_df)
    #print("\nOM FROM DB\n",om_df)
    #print("\nOCED FROM DB\n",oced_df)
    #print("\nOCEP FROM DB\n",ocep_df)
    
    conn.close()
    
    
    
    
    
    
    
    
    
    
    
    
    end_time = time.time()
    end_time1=time.ctime(end_time)
    
    #print("\n\nEnd time: ",end_time1)
    
except Exception as e:
  print("\nError in input database\n",e)