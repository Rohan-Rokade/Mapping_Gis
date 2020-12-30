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
    
   
        st.success("You selected a Telecom INfrastructure")
        
        
            df1=pd.read_csv("https://raw.githubusercontent.com/Rohan-Rokade/networkdetector/master/308.csv"")
            st.table(df1)
           
            
    
