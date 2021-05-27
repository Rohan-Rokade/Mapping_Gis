



import streamlit as st
import pandas as pd
import numpy as np
import pymongo
import folium
import branca
from folium import  Marker
import folium.plugins as plugins
from folium.plugins import  MarkerCluster
from streamlit_folium import folium_static
import sqlite3
import re




conn=sqlite3.connect('data.db')
c=conn.cursor()

username_list = []

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO usertable(username,password) VALUES(?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM usertable WHERE username=? AND password=? ',(username,password))
    data=c.fetchall()
    return data

def signup_user(username):
    c.execute('SELECT * FROM usertable WHERE username='+username)
    data=c.fetchall()
    st.table(data)
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data=c.fetchall()
    return data


def login_tab():
    
        st.subheader("Login to Cotinue")

        username1=st.sidebar.text_input("User Name")
        password1=st.sidebar.text_input("Password",type="password")

        st.sidebar.text("Press Enter to Login")
        

        create_usertable()
        result=login_user(username1,password1)

       

        if True:

            if result:
                   
                st.success("Logged in with {}".format(username1))
                

                emp_arr=['']
                infra_arr=['Wifi','Hospital','Towers']
                infra_list=np.append(emp_arr,infra_arr)
                
                infra_selected = st.selectbox('Select one Telecom Infrastructure:',infra_list, format_func=lambda u: 'Select one Telecom Infrastructure' if u == '' else u,key="Infra list")
                
                if infra_selected:
                    st.success("You selected a Telecom Infrastructure")
                    
                    if infra_selected=='Wifi':
                        df1=pd.read_csv("https://raw.githubusercontent.com/Rohan-Rokade/Mapping-_Telecom-/main/wifi_gen.csv")
                        st.table(df1)
                        
                        emp_arr=['']
                        wifi_arr=['Metadata Attached','Heat Map']
                        wifi_list=np.append(emp_arr,wifi_arr)
                        
                        wifi_inner_selected = st.selectbox('select an option',wifi_list, format_func=lambda u: 'Select an option' if u == '' else u,key="wifi inner  list") 
                        if  wifi_inner_selected:
                                st.success("You selected an option")
                                if wifi_inner_selected =='Metadata Attached':
                                    
                                    
                        
                                    def fancy_html(row):
                                        i = row
                                        mi="MetaData Information"
                                        Network_Service_Provider = df1['nsp'].iloc[i]                             
                                        Number_of_Connected_Users = df1['ncu'].iloc[i]                           
                                    
                                        
                                        left_col_colour = "#2A799C"
                                        right_col_colour = "#C5DCE7"
                                        
                                        html = """<!DOCTYPE html>
                                    <html>
                                    
                                    <head>
                                    <h4 style="margin-bottom:0"; width="300px">{}</h4>""".format(mi)+"""
                                    
                                    </head>
                                    
                                    <table style="height: 126px; width: 300px;">
                                    <tbody>
                                    <tr>
                                    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Network Service Provider</span></td>
                                    <td style="width: 100px;background-color: """+ right_col_colour +""";">{}</td>""".format(Network_Service_Provider) + """
                                    </tr>
                                    <tr>
                                    <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Number of Connected_Users</span></td>
                                    <td style="width: 100px;background-color: """+ right_col_colour +""";">{}</td>""".format(Number_of_Connected_Users) + """
                                    </tr>
                                    
                                    
                                    
                                    </tbody>
                                    </table>
                                    </html>
                                    """
                                        return html
                                    
                                    location = df1['lat'].mean(), df1['lon'].mean()
                                    m101 = folium.Map(location=location,zoom_start=5)
                                    
                                    for i in range(0,len(df1)):
                                        
                                        ncu9 = df1['ncu'].iloc[i]
                                        if ncu9 >= 1 and ncu9 <=2:
                                            colors = 'green'
                                        elif ncu9 > 2 and ncu9<=4:
                                            colors = 'purple'
                                        elif ncu9 >4:
                                            colors = 'red'
                                        
                                        html = fancy_html(i)
                                        iframe = branca.element.IFrame(html=html,width=500,height=180)
                                        popup = folium.Popup(iframe,parse_html=True)
                                        
                                        mc = MarkerCluster()
                                        
                                        mc.add_child(Marker([df1['lat'].iloc[i],df1['lon'].iloc[i]],
                                                      popup=popup,icon=folium.Icon(color=colors,icon='info-sign'))).add_to(m101)
                                    m101.add_child(mc)
                                    st.subheader(" **Range for legends**")
                                    st.write("Green : 1 - 2")
                                    st.write("Purple : 3 - 4")
                                    st.write("Red : 5 - 6")
                                        
                                    
                                    folium_static(m101)
                        
                                else:
                                    
                                    m103 = folium.Map(location=[np.average(df1['lat']),np.average(df1['lon'])], tiles='cartodbpositron', zoom_start=4)
                                    
                                    
                                    data_heat = df1[['lat','lon','ncu']].values.tolist()
                                    plugins.HeatMap(data_heat).add_to(m103)
                                    folium_static(m103)
                        else:
                            st.warning("No option selected")
                        
                        
                    elif infra_selected=='Hospital':
                        df1=pd.read_csv("https://raw.githubusercontent.com/Rohan-Rokade/Mapping-_Telecom-/main/hos_gen.csv")
                        st.table(df1)
                        
                        m99= folium.Map(location=[np.average(df1['lat']),np.average(df1['lon'])], tiles='cartodbpositron', zoom_start=4)
                        mc = MarkerCluster()
                        
                        
                        for i in range(0,len(df1)):
                            
                        
                                    def fancy_html(row):
                                                    i = row
                                                    mi="MetaData Information"
                                                    hostname = df1['host'].iloc[i]                             
                                                    contact_number = df1['contact'].iloc[i] 
                                                    opening=df1['open'].iloc[i]
                                                    closing=df1['closed'].iloc[i]
                                                
                                                    
                                                    left_col_colour = "#2A799C"
                                                    right_col_colour = "#C5DCE7"
                                                    
                                                    html = """<!DOCTYPE html>
                                                <html>
                                                
                                                <head>
                                                <h4 style="margin-bottom:0"; width="300px">{}</h4>""".format(mi)+"""
                                                
                                                </head>
                                                
                                                <table style="height: 126px; width: 300px;">
                                                <tbody>
                                                <tr>
                                                <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;"> Hospital Name</span></td>
                                                <td style="width: 100px;background-color: """+ right_col_colour +""";">{}</td>""".format(hostname) + """
                                                </tr>
                                                <tr>
                                                <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Contact Number</span></td>
                                                <td style="width: 100px;background-color: """+ right_col_colour +""";">{}</td>""".format(contact_number) + """
                                                </tr>
                                                <tr>
                                                <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Opening Time</span></td>
                                                <td style="width: 100px;background-color: """+ right_col_colour +""";">{}</td>""".format(opening) + """
                                                </tr>
                                                <tr>
                                                <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Closing Time</span></td>
                                                <td style="width: 100px;background-color: """+ right_col_colour +""";">{}</td>""".format(closing) + """
                                                </tr>
                                                
                                                
                                                
                                                </tbody>
                                                </table>
                                                </html>
                                                """
                                                    return html
                                        
                                    html = fancy_html(i)
                                    iframe = branca.element.IFrame(html=html,width=500,height=180)
                                    popup = folium.Popup(iframe,parse_html=True)
                                    
            
                                    mc.add_child(Marker(location=[df1['lat'].iloc[i],df1['lon'].iloc[i]],popup=popup,icon=folium.Icon(icon='info-sign'))).add_to(m99)
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
                            
                            
                            
                            m95= folium.Map(location=[np.average(data9['lat']),np.average(data9['lon'])], tiles='cartodbpositron', zoom_start=4)
                            mc = MarkerCluster()
                            for idx, row in data9.iterrows():
                                 mc.add_child(Marker(location=[row['lat'], row['lon']],
                            popup=("Hospital Name: {xyz1}<br>""Opening time of Hospital: {open1}<br>" "Closing time of Hospital: {close1}<br>" "Contact Number :{contact1}<br>")
                        .format(xyz1=row.host,open1=row.open,close1=row.closed,contact1=row.contact),
                            icon=folium.Icon(icon='info-sign')
                                    ))
                            m95.add_child(mc) 
                            folium_static(m95)
                            
                        
                        
                        
                       
                        
                    elif  infra_selected=='Towers':
                        DATABASE = "mongodb+srv://amaan:PwxIIvIMb2tTow3z@cluster0-myavd.mongodb.net/natours?retryWrites=true&w=majority"
                        @st.cache
                        def load_data():
                                client = pymongo.MongoClient(DATABASE)
                        
                                db = client["natours"]
                                towers= db["towers"].find().limit(500)
                        
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
                        
                        m_4 = folium.Map(location=[np.average(data2['lat']),np.average(data2['lon'])], tiles='cartodbpositron', zoom_start=4)


                        data_heat = data2[['lat','lon','samples']].values.tolist()
                        plugins.HeatMap(data_heat).add_to(m_4)
                        folium_static(m_4)
                else:
                    st.warning("No option selected")
                    
            else :
                st.warning("Incorrect username/Password")
        else:
            pass


def email_validator(email):

    #Remove below line if  you want to implement email validation
    return True
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex,email)):  
        return True  
          
    else:  
        return False

def password_validator(password):

    if len(password)>4 and re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) and re.search("[_@$]", password) :
        return True
    return False


def signup_tab():
    st.subheader("Create New Account")

    username1=st.sidebar.text_input("New User Name")
    password1=st.sidebar.text_input("Password for New User",type="password")

    if st.sidebar.button("Submit"):

        if email_validator(username1) and password_validator(password1):

            if username1 in username_list:
                st.warning("Please use any other username. This username already exists!!")

            else:      
                
                add_userdata(username1, password1)
                st.info("Go to login menu to login")
                st.balloons()
                username_list.append(username1)
        else:
            st.warning("Invalid username/password format")
            st.write("Conditions for valid passwords")
            st.write("Conditions for a valid password are:\nShould have at least one number.\nShould have at least one uppercase and one lowercase character.\nShould have at least one special symbol.\nShould be between 6 to 20 characters long.")

def logout_tab():
    st.success("You are Logged Out")
    


def main():
    menu=["Home","Login","Logout","Sign Up"]
    choice=st.sidebar.selectbox("Menu",menu,index=0)
    create_usertable()
    add_userdata("Eksh","Eksh@123")
    username_list.append("Eksh")
    

    if choice =="Home":
        st.title("Server Based Web GIS Application for Goverment Authorities")
            
    elif choice=="Login":
        login_tab()
        
    
    elif choice=='Logout':
        logout_tab()

    elif choice == "Sign Up":
        signup_tab()

            
if __name__== '__main__':
    
    main()
        

