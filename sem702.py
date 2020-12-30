# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:54:31 2020

@author: hp
"""


import streamlit as st
import pandas as pd
import numpy as np
import pymongo


dashboard_selectbox = st.sidebar.selectbox(
    "DASHBOARD",
    ("Home", "Mapping of Telecom Infrastructure"))

if dashboard_selectbox=="Home":
    st.title("SEM 7 Project,Mapping of Telecom Infrastructure in GIS application done by ROHAN ROKADE & MAAZ AMAAN SHAIKH")
    
if dashboard_selectbox=="Mapping of Telecom Infrastructure" :
    
    emp_arr=['']
    infra_arr=['Wifi','Hospital','Towers']
    infra_list=np.append(emp_arr,infra_arr)
    
    infra_selected = st.selectbox('Select one Telecom Infrastructure:',infra_list, format_func=lambda u: 'Select an option' if u == '' else u,key="Infra list")
    
    if infra_selected:
        st.success("You selected a Telecom INfrastructure")
        
        if infra_selected=='Wifi':
            df1=pd.read_csv("C:\\Users\\hp\Desktop\\wifi_gen.csv")
            st.table(df1)
           
            
        elif  infra_selected=='Towers':
            DATABASE = "mongodb+srv://amaan:PwxIIvIMb2tTow3z@cluster0-myavd.mongodb.net/natours?retryWrites=true&w=majority"
            @st.cache
            def load_data():
                    client = pymongo.MongoClient(DATABASE)
            
                    db = client["natours"]
                    towers= db["towers"].find().limit(100)
            
                    data = [userRecord for userRecord in towers ] 
                    df1= pd.DataFrame(data)
                    df1.reset_index(drop=True, inplace=True)
                    df1.drop(['_id'], axis=1,inplace=True)
                    return df1
            
            data2=load_data()
            st.table(data2.head())
            
    else:
        st.warning("No Telecom Infrastructure Selected")
