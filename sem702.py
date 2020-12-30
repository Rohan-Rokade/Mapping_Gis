# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 17:54:31 2020

@author: hp
"""
#asdfghjkl;sdfghjklasdfghjk

import streamlit as st
import pandas as pd
import numpy as np
import pymongo
import folium
from folium import  Marker
from folium.plugins import  MarkerCluster
from streamlit_folium import foliumh_static


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
            df1=pd.read_csv("https://raw.githubusercontent.com//Rohan-Rokade//Mapping-_Telecom-//main//wifi_gen.csv")
            st.table(df1)
            
            m98= folium.Map(location=[np.average(df1['lat']),np.average(df1['lon'])],tiles='OpenStreetMap',zoom_start=6)
            
            for idx, row in df1.iterrows():
                 folium.Marker(location=[row['lat'], row['lon']],popup=("Network service Provider: {nsp1}<br>"
             "Number of Connected Users: {ncp1}<br>").format(nsp1=row.nsp,ncp1=row.ncu),icon=folium.Icon(icon='cloud',color='green')).add_to(m98)
            folium_static(m98)
            
            
        elif infra_selected=='Hospital':
            df1=pd.read_csv("https://raw.githubusercontent.com//Rohan-Rokade//Mapping-_Telecom-//main//hos_gen.csv")
            st.table(df1)
            
            m99= folium.Map(location=[np.average(df1['lat']),np.average(df1['lon'])], tiles='cartodbpositron', zoom_start=4)
            mc = MarkerCluster()
            
            for idx, row in df1.iterrows():
                 mc.add_child(Marker(location=[row['lat'], row['lon']],
            popup=("Hospital Name: {xyz1}<br>""Opening time of Hospital: {open1}<br>" "Closing time of Hospital: {close1}<br>" "Contact Number :{contact1}<br>")
            .format(xyz1=row.host,open1=row.open,close1=row.closed,contact1=row.contact)
                    ,icon=folium.Icon(icon='info-sign')
                    ))
            m99.add_child(mc)
            
            folium_static(m99)
            
            #time fix 
            hr_input=st.slider('Slide Hours', min_value=0, max_value=24)
            df1['op_hr']=df1['open'].str[:2]
            df1['op_hr']=df1['op_hr'].astype(int)
          
         
            data8=df1[(df1.op_hr==hr_input)]
            st.write(data8)
            
            m96= folium.Map(location=[np.average(df1['lat']),np.average(df1['lon'])], tiles='cartodbpositron', zoom_start=4)
            mc = MarkerCluster()
            for idx, row in data8.iterrows():
                 mc.add_child(Marker(location=[row['lat'], row['lon']],
            popup=("Hospital Name: {xyz1}<br>""Opening time of Hospital: {open1}<br>" "Closing time of Hospital: {close1}<br>" "Contact Number :{contact1}<br>")
            .format(xyz1=row.host,open1=row.open,close1=row.closed,contact1=row.contact)
                    ,icon=folium.Icon(icon='info-sign')
                    ))
            m96.add_child(mc) 
            folium_static(m96)
            
            pt_input=st.text_input("Enter the name or substring of Hospital name you want to find","enter here")
            
            
            if(pt_input!= "enter here"):
                data9=df1[df1.host.str.contains(pt_input)]
                st.write(data9)
                m95= folium.Map(location=[np.average(df1['lat']),np.average(df1['lon'])], tiles='cartodbpositron', zoom_start=4)
                mc = MarkerCluster()
                for idx, row in data9.iterrows():
                     mc.add_child(Marker(location=[row['lat'], row['lon']],
                popup=("Hospital Name: {xyz1}<br>""Opening time of Hospital: {open1}<br>" "Closing time of Hospital: {close1}<br>" "Contact Number :{contact1}<br>")
                .format(xyz1=row.host,open1=row.open,close1=row.closed,contact1=row.contact)
                        ,icon=folium.Icon(icon='info-sign')
                        ))
                m95.add_child(mc) 
                folium_static(m95)
            
            
            
           
            
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
            
            m_3 = folium.Map(location=[np.average(data2['lat']),np.average(data2['lon'])], tiles='cartodbpositron', zoom_start=4)
            # Add points to the map
            mc = MarkerCluster()

            for idx, row in data2.iterrows():
                 mc.add_child(Marker(location=[row['lat'], row['lon']],
                                     popup=("Range: {range1}<br>"
             "Radio Type: {radio1}<br>").format(range1=row.range,radio1=row.radio),icon=folium.Icon(icon='info-sign')))
            m_3.add_child(mc)
            
            folium_static(m_3)

        
            
        
    else:
        st.warning("No Telecom Infrastructure Selected")
