import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import plotly.express as px
import plotly.io as pio
import pandas as pd
import json
import requests

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()

# AGGREGATED_INSURANCE
# Using a buffered cursor
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM aggregated_insurance")
    mydb.commit()
    table1 = cursor.fetchall() 
    Aggre_insurance = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()

#AGGREGATED_TRANSACTION
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM aggregated_transaction")
    mydb.commit()
    table2 = cursor.fetchall()
    Aggre_transaction = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()

#AGGREGATED_USER
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM aggregated_user")
    mydb.commit()
    table3 = cursor.fetchall()
    Aggre_user = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()

#MAP_INSURANCE
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM map_insurance")
    mydb.commit()
    table4 = cursor.fetchall()
    Map_insurance = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()

#MAP_TRANSACTION
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM map_transaction")
    mydb.commit()
    table5 = cursor.fetchall()
    Map_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()
#MAP_USER
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM map_user")
    mydb.commit()
    table6 = cursor.fetchall()
    Map_user = pd.DataFrame(table6,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()
#TOP_INSURANCE
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM top_insurance")
    mydb.commit()
    table7 = cursor.fetchall()
    Top_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()
#TOP_TRANSACTION
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM top_transaction")
    mydb.commit()
    table8 = cursor.fetchall()
    Top_transaction = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
finally:
    cursor.close()
    mydb.close()

#CONNECTION TO MYSQL
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Raj$1006",
            database="phonepe_data",
            port="3306")
cursor = mydb.cursor()
#TOP_USER
cursor = mydb.cursor(buffered=True)
try:
    cursor.execute("SELECT * FROM top_user")
    mydb.commit()
    table9 = cursor.fetchall()
    Top_user = pd.DataFrame(table9,columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))
finally:
    cursor.close()
    mydb.close()

#AGGREGATED INSURANCE
def Transaction_amount_count_Y(df,year):
    tacy = df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States",y="Transaction_amount", title = f"TRANSACTION AMOUNT-{year}")
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States",y="Transaction_count", title = f"TRANSACTION COUNT-{year}")
        st.plotly_chart(fig_count)

    # India's state wise latitude and longitude
    col1,col2 = st.columns(2)

    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow", range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].min()),
                                hover_name="States", title=f"{year}TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
        #Fit bounds --> Fit india from world map

    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow", range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].min()),
                                hover_name="States", title=f"{year}TRANSACTION COUNT", fitbounds="locations")
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    return tacy

# For Quarter
def Transaction_amount_count_Y_Q(df,quarter):
    tacy = df[df["Quarter"] == quarter] # Year df
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States",y="Transaction_amount", title = f"{tacy['Years'].min()}-YEAR QUARTER-{quarter} TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States",y="Transaction_count", title = f"{tacy['Years'].min()}-YEAR QUARTER-{quarter} TRANSACTION AMOUNT")
        st.plotly_chart(fig_count)

    # India's state wise latitude and longitude
    col1,col2 = st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow", range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].min()),
                                hover_name="States", title=f"{tacy['Years'].min()}-YEAR QUARTER-{quarter} TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
        #Fit bounds --> Fit india from world map

    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow", range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].min()),
                                hover_name="States", title=f"{tacy['Years'].min()}-YEAR QUARTER-{quarter} TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
    return tacy
    

def Aggre_Tran_Transaction_type(df,state):
    tacy = df[df["States"] == state] # Year df
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame=tacyg, names= "Transaction_type", values= "Transaction_amount",
                        title= f"{state.upper()}-TRANSACTION AMOUNT", hole= 0.5) 
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2 = px.pie(data_frame=tacyg, names= "Transaction_type", values= "Transaction_count",
                        title= f"{state.upper()}-TRANSACTION COUNT", hole= 0.5) 
        st.plotly_chart(fig_pie_2)

# AGGREGATED USER ANALYSIS
def Aggre_user_plot_1(df,year):
    aguy = df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace =True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transaction_count", title=f"BRANDS & TRANSACTION COUNT-{year}")
    st.plotly_chart(fig_bar_1)

    return aguy

# AGGREGATED USER ANALYSIS (QUARTER)
def Aggre_user_plot_2(df,quarter):
    aguyq = df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace =True)

    #Grouping
    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)


    fig_bar_1 = px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"BRANDS & TRANSACTION COUNT-QUARTER {quarter}")
    st.plotly_chart(fig_bar_1)

    return aguyq

# AGGREGATED USER ANALYSIS 
def Aggre_user_plot_3(df,state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1 = px.line(auyqs, x="Brands", y="Transaction_count", 
                        title=f"{state.upper()} - BRANDS, TRANSACTION COUNT", markers=True)
    st.plotly_chart(fig_line_1)

#MAP INSURANCE DISTRICT
def Map_insur_District(df,state):
    tacy = df[df["States"] == state] # Year df
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x="Districts", y="Transaction_amount", height=600,
                        title=f"{state.upper()} - DISTRICT AND TRANSACTION AMOUNT")
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(tacyg, x="Districts", y="Transaction_count", height=600,
                        title=f"{state.upper()} - DISTRICT AND TRANSACTION COUNT")
        st.plotly_chart(fig_bar_2)

#MAP TRANSACTION DISTRICT
def Map_tran_District(df,state):
    tacy = df[df["States"] == state] # Year df
    tacy.reset_index(drop=True, inplace = True)

    tacyg = tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x="District", y="Transaction_amount",
                        title=f"{state.upper()} - DISTRICT AND TRANSACTION AMOUNT")
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(tacyg, x="District", y="Transaction_count",
                        title=f"{state.upper()} - DISTRICT AND TRANSACTION COUNT")
        st.plotly_chart(fig_bar_2)

# MAP USER (YEAR)
def map_user_plot_1(df,year):   
    muy = df[df["Years"]==year]
    muy.reset_index(drop=True, inplace =True)

    muyg = muy.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace = True)

    fig_line_1 = px.line(muyg, x="States", y=["RegisteredUser","AppOpens"],
                            title=f"REGISTERED USER & APPOPENS - {year}", markers=True)
    st.plotly_chart(fig_line_1)

    return muy

# MAP USER (QUARTER)
def map_user_plot_2(df,quarter):   
    muyq = df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace =True)

    muyqg = muyq.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyqg.reset_index(inplace = True)

    fig_line_1 = px.line(muyqg, x="States", y=["RegisteredUser","AppOpens"],
                            title=f"REGISTERED USER & APPOPENS - Quarter {quarter}", markers=True)
    st.plotly_chart(fig_line_1)

    return muyq
# MAP USER FOR REGISTEREDUSED & APPOPENS
def map_user_plot_3(df, states):
    muyqs = df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace =True)

    fig_map_user_bar_1 = px.bar(muyqs,x="Districts", y = "RegisteredUser", 
                                title=f"{states.upper()} REGISTERED USER",height=500)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2 = px.bar(muyqs,x="Districts", y = "AppOpens",
                                title=f"{states.upper()} APP OPENS",height=500)
    st.plotly_chart(fig_map_user_bar_2)

#TOP INSURANCE (1)
def Top_insurance_plot_1(df,state):
    tiy = df[df["States"]==state]
    tiy.reset_index(drop=True, inplace =True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insur_bar_1 = px.bar(tiy,x="Quarter", y = "Transaction_amount",
                                        title="TRANSACTION AMOUNT",height=800)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2 = px.bar(tiy,x="Quarter", y = "Transaction_count",
                                        title="TRANSACTION COUNT",height=800)
        st.plotly_chart(fig_top_insur_bar_2)

#TOP USER
def top_user_plot_1(df,year):
    tuy = df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace =True)

    tuyg = pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace = True)

    fig_top_plot_1=px.bar(tuyg, x="States",y="RegisteredUsers",color="Quarter",
                          title=f"REGISTERED USERS - {year}",hover_name="States")
    st.plotly_chart(fig_top_plot_1)

    return tuy

# TOP USER STATE
def top_user_plot_2(df,state):
    tuys = df[df["States"]==state]
    tuys.reset_index(drop=True, inplace =True)

    fig_top_plot_2=px.bar(tuys, x="Quarter",y="RegisteredUsers", title="REGISTERED USERS,QUARTER",
                        color="RegisteredUsers")
    st.plotly_chart(fig_top_plot_2)

#CONNECTION TO MYSQL
def top_chart_insurance_amount(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # INSURANCE AMOUNT DESC
    query1 = f'''SELECT States,sum(Insurance_amount) as Insurance_amount
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Insurance_amount desc
                 limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "Insurance_amount"))
    col1,col2,col3 =  st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="Insurance_amount", title = "TOP 5 INSURANCE AMOUNT")
        st.plotly_chart(fig_amount_1)


    #INSURANCE AMOUNT ASC
    query2 = f'''SELECT States,sum(Insurance_amount) as Insurance_amount
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Insurance_amount asc
                 limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "Insurance_amount"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="Insurance_amount", title = "LAST 5 INSURANCE AMOUNT")
        st.plotly_chart(fig_amount_2)


    #INSURANCE AMOUNT AVERAGE
    query3 = f'''SELECT States,avg(Insurance_amount) as Insurance_amount
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Insurance_amount;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "Insurance_amount"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="Insurance_amount", title = "AVERAGE INSURANCE AMOUNT")
        st.plotly_chart(fig_amount_3)

#CONNECTION TO MYSQL FOR COUNT
def top_chart_insurance_count(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # INSURANCE COUNT DESC
    query1 = f'''SELECT States,sum(Insurance_count) as Insurance_count
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Insurance_count desc
                 limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "Insurance_count"))
    col1,col2,col3=st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="Insurance_count", title = "TOP 5 INSURANCE COUNT")
        st.plotly_chart(fig_amount_1)

    #INSURANCE COUNT ASC
    query2 = f'''SELECT States,sum(Insurance_count) as Insurance_count
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Insurance_count asc
                 limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "Insurance_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="Insurance_count", title = "LAST 5 INSURANCE COUNT")
        st.plotly_chart(fig_amount_2)

    #INSURANCE COUNT AVERAGE
    query3 = f'''SELECT States,avg(Insurance_count) as Insurance_count
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Insurance_count;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "Insurance_count"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="Insurance_count", title = "AVERAGE INSURANCE COUNT")
        st.plotly_chart(fig_amount_3)

#CONNECTION TO MYSQL FOR TRANSACTION AMOUNT
def top_chart_transaction_amount(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # TRANSACTION AMOUNT DESC
    query1 = f'''SELECT States,sum(Transaction_amount) as Transaction_amount
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Transaction_amount desc
                 limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "Transaction_amount"))
    col1,col2,col3 =  st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="Transaction_amount", title = "TOP 5 TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount_1)


    #INSURANCE AMOUNT ASC
    query2 = f'''SELECT States,sum(Transaction_amount) as Transaction_amount
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Transaction_amount asc
                 limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "Transaction_amount"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="Transaction_amount", title = "LAST 5 TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount_2)


    #INSURANCE AMOUNT AVERAGE
    query3 = f'''SELECT States,avg(Transaction_amount) as Transaction_amount
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Transaction_amount;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "Transaction_amount"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="Transaction_amount", title = "AVERAGE TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount_3)

#CONNECTION TO MYSQL FOR TRANSACTION COUNT
def top_chart_transaction_count(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # INSURANCE COUNT DESC
    query1 = f'''SELECT States,sum(Transaction_count) as Transaction_count
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Transaction_count desc
                 limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "Transaction_count"))
    col1,col2,col3=st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="Transaction_count", title = "TOP 5 TRANSACTION COUNT")
        st.plotly_chart(fig_amount_1)

    #INSURANCE COUNT ASC
    query2 = f'''SELECT States,sum(Transaction_count) as Transaction_count
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Transaction_count asc
                 limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "Transaction_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="Transaction_count", title = "LAST 5 TRANSACTION COUNT")
        st.plotly_chart(fig_amount_2)

    #INSURANCE COUNT AVERAGE
    query3 = f'''SELECT States,avg(Transaction_count) as Transaction_count
                 FROM phonepe_data.{table_name}
                 group by states
                 order by Transaction_count;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "Transaction_count"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="Transaction_count", title = "AVERAGE TRANSACTION COUNT")
        st.plotly_chart(fig_amount_3)

#CONNECTION TO MYSQL
def top_chart_registered_user(table_name,state):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # INSURANCE AMOUNT DESC
    query1 = f'''SELECT Districts, sum(RegisteredUser) as RegisteredUser
                    FROM phonepe_data.{table_name}
                    where states= '{state}'
                    group by districts
                    order by RegisteredUser desc
                    limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "RegisteredUser"))
    col1,col2,col3=st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="districts",y="RegisteredUser", title = "TOP 5 REGISTERED USER")
        st.plotly_chart(fig_amount_1)

    #INSURANCE AMOUNT ASC
    query2 = f'''SELECT Districts, sum(RegisteredUser) as RegisteredUser
                    FROM phonepe_data.{table_name}
                    where states= '{state}'
                    group by districts
                    order by RegisteredUser asc
                    limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "RegisteredUser"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="districts",y="RegisteredUser", title = "LAST 5 REGISTERED USER")
        st.plotly_chart(fig_amount_2)

    #INSURANCE AMOUNT AVERAGE
    query3 = f'''SELECT Districts, avg(RegisteredUser) as RegisteredUser
                    FROM phonepe_data.{table_name}
                    where states= '{state}'
                    group by districts
                    order by RegisteredUser;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "RegisteredUser"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="districts",y="RegisteredUser", title = "AVERAGE REGISTERED USER")
        st.plotly_chart(fig_amount_3)

#CONNECTION TO MYSQL
def top_chart_appopens(table_name,state):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # APP OPENS DESC
    query1 = f'''SELECT Districts, sum(appopens) as appopens
                    FROM phonepe_data.{table_name}
                    where states= '{state}'
                    group by districts
                    order by appopens desc
                    limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "appopens"))
    col1,col2,col3=st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="districts",y="appopens", title = "TOP 5 APP OPENS")
        st.plotly_chart(fig_amount_1)

    #APP OPENS ASC
    query2 = f'''SELECT Districts, sum(appopens) as appopens
                    FROM phonepe_data.{table_name}
                    where states= '{state}'
                    group by districts
                    order by appopens asc
                    limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "appopens"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="districts",y="appopens", title = "LAST 5 APP OPENS")
        st.plotly_chart(fig_amount_2)

    #APP OPENS AVERAGE
    query3 = f'''SELECT Districts, avg(appopens) as appopens
                    FROM phonepe_data.{table_name}
                    where states= '{state}'
                    group by districts
                    order by appopens;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "appopens"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="districts",y="appopens", title = "AVERAGE APP OPENS")
        st.plotly_chart(fig_amount_3)

#TOP USER - REGISTERED USERS
#CONNECTION TO MYSQL
def top_chart_registered_users(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # REGISTERED USERS DESC
    query1 = f'''SELECT States, sum(RegisteredUsers) as RegisteredUsers
                    FROM phonepe_data.top_user
                    group by States
                    order by RegisteredUsers desc
                    limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "RegisteredUsers"))
    col1,col2,col3=st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="RegisteredUsers", title = "TOP 5 REGISTERED USERS")
        st.plotly_chart(fig_amount_1)

    #REGISTERED USERS ASC
    query2 = f'''SELECT States, sum(RegisteredUsers) as RegisteredUsers
                    FROM phonepe_data.top_user
                    group by States
                    order by RegisteredUsers asc
                    limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "RegisteredUsers"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="RegisteredUsers", title = "LAST 5 REGISTERED USERS")
        st.plotly_chart(fig_amount_2)

    #AVERAGE REGISTERED USERS
    query3 = f'''SELECT States, avg(RegisteredUsers) as RegisteredUsers
                    FROM phonepe_data.top_user
                    group by States
                    order by RegisteredUsers ;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "RegisteredUsers"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="RegisteredUsers", title = "AVERAGE REGISTERED USERS")
        st.plotly_chart(fig_amount_3)

# TOP BRANDS
#CONNECTION TO MYSQL
def top_chart_top_brands(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # Top selling brands
    query1 = f'''SELECT Brands,sum(Percentage) as Percentage
                    FROM phonepe_data.{table_name}
                    group by Brands
                    order by Percentage desc
                    limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("Brands", "Percentage"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="Brands",y="Percentage", title = "TOP 5 Brands")
        st.plotly_chart(fig_amount_1)

    # least selling brands
    query1 = f'''SELECT Brands,sum(Percentage) as Percentage
                    FROM phonepe_data.{table_name}
                    group by Brands
                    order by Percentage asc
                    limit 5;'''
    cursor.execute(query1)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("Brands", "Percentage"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="Brands",y="Percentage", title = "LAST 5 Brands")
        st.plotly_chart(fig_amount_2)

# TOP TRANSACTION AMOUNT
#CONNECTION TO MYSQL
def top_chart_top_tran_amount(table_name,state):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # "TOP 5 STATES - TRANSACTION AMOUNT"
    query1 = f'''SELECT States,sum(Transaction_amount) as Transaction_amount
                    FROM phonepe_data.{table_name}
                    group by States
                    order by Transaction_amount desc
                    limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "Transaction_amount"))
    col1,col2,col3 = st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="Transaction_amount", title = "TOP 5 STATES - TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount_1)

    # "LAST 5 STATES - TRANSACTION AMOUNT"
    query2 = f'''SELECT States,sum(Transaction_amount) as Transaction_amount
                    FROM phonepe_data.{table_name}
                    group by States
                    order by Transaction_amount 
                    limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "Transaction_amount"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="Transaction_amount", title = "LAST 5 STATES - TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount_2)

     # "AVG 5 STATES - TRANSACTION AMOUNT"
    query3 = f'''SELECT States,avg(Transaction_amount) as Transaction_amount
                    FROM phonepe_data.{table_name}
                    group by States
                    order by Transaction_amount;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "Transaction_amount"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="Transaction_amount", title = " AVERAGE TRANSACTION AMOUNT")
        st.plotly_chart(fig_amount_3)

# TOP TRANSACTION COUNT
#CONNECTION TO MYSQL
def top_chart_top_tran_count(table_name,state):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    # "TOP 5 STATES - TRANSACTION COUNT"
    query1 = f'''SELECT States,sum(Transaction_count) as Transaction_count
                    FROM phonepe_data.{table_name}
                    group by States
                    order by Transaction_count desc
                    limit 5;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "Transaction_count"))
    col1,col2,col3 = st.columns(3)
    with col1:
        fig_amount_1 = px.bar(df_1, x="States",y="Transaction_count", title = "TOP 5 STATES - TRANSACTION COUNT")
        st.plotly_chart(fig_amount_1)

    # "LAST 5 STATES - TRANSACTION COUNT"
    query2 = f'''SELECT States,sum(Transaction_count) as Transaction_count
                    FROM phonepe_data.{table_name}
                    group by States
                    order by Transaction_count 
                    limit 5;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "Transaction_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States",y="Transaction_count", title = "LAST 5 STATES - TRANSACTION COUNT")
        st.plotly_chart(fig_amount_2)

     # "AVG 5 STATES - TRANSACTION COUNT"
    query3 = f'''SELECT States,avg(Transaction_count) as Transaction_count
                    FROM phonepe_data.{table_name}
                    group by States
                    order by Transaction_count;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "Transaction_count"))
    with col3:
        fig_amount_3 = px.bar(df_3, x="States",y="Transaction_count", title = " AVERAGE TRANSACTION COUNT")
        st.plotly_chart(fig_amount_3)

#BRANDS AND ITS PERCENTAGE
#CONNECTION TO MYSQL
def top_chart_brands(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

    query1 = f'''SELECT Brands,sum(Percentage) as Percentage
                    FROM phonepe_data.{table_name}
                    group by Brands
                    order by Percentage desc;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("Brands", "Percentage"))
    fig_amount_1 = px.bar(df_1, x="Brands",y="Percentage", title = "Brands AND ITS PERCENTAGE")
    st.plotly_chart(fig_amount_1)

#Pincodes and Registered users
# #CONNECTION TO MYSQL
def top_chart_pincodes_regusers(table_name):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Raj$1006",
                database="phonepe_data",
                port="3306")
    cursor = mydb.cursor()

#Top 10 Registeresusers with pincodes
    query1 = f'''SELECT cast(Pincodes as char), SUM(RegisteredUsers) 
                    FROM phonepe_data.{table_name}
                    GROUP BY Pincodes
                    order by Pincodes desc
                    limit 10;'''
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("Pincodes", "RegisteredUsers"))
    df_1['Pincodes'] = df_1['Pincodes'].astype(str)
    col1,col2 = st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="Pincodes",y="RegisteredUsers", title = "TOP 10 PINCODES WITH MORE REGISTERED USERS"
                              ,labels={"Pincodes": "Pincode", "RegisteredUsers": "Registered Users"},text_auto=True,template="plotly_white")
        st.plotly_chart(fig_amount_1)

#Last 10 Registeresusers with pincodes
    query2 = f'''SELECT cast(Pincodes as char), SUM(RegisteredUsers) 
                    FROM phonepe_data.{table_name}
                    GROUP BY Pincodes
                    order by Pincodes asc
                    limit 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("Pincodes", "RegisteredUsers"))
    df_2['Pincodes'] = df_2['Pincodes'].astype(str)
    with col2:
        fig_amount_2 = px.bar(df_2, x="Pincodes",y="RegisteredUsers", title = "10 PINCODES WITH LEAST REGISTERED USERS",
                              labels={"Pincodes": "Pincode", "RegisteredUsers": "Registered Users"},text_auto=True,template="plotly_white")
        st.plotly_chart(fig_amount_2)

#Streamlit part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")
with st.sidebar:
    select = option_menu("MAIN MENU",["HOME", "DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
    col1,col2 = st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe is a Digital Wallet & Online Payment App that allows you to make instant Money Transfers with UPI")
        st.write("****FEATURES****")
        st.write("****CREDIT CARD AND DEBIT CARD LINKING****")
        st.write("****BANK BALANCE CHECK****")
        st.write("****MONEY STORAGE****")
        st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")
    with col2:
        st.image((r"C:\Users\mypc\Downloads\images.png"),width=500)

    col3,col4 = st.columns(2)
    with col3:
        st.video(r"C:\Users\mypc\Downloads\PhonePe - No more E-wallets.mp4")
    with col4:
        st.write("****EASY TRANSACTIONS****") 
        st.write("****ONE APP FOR ALL YOUR PAYMENTS****")
        st.write("****YOUR BANK ACCOUNT IS ALL YOU NEED****")
        st.write("****MULTIPLE PAYMENT MODES****")
        st.write("****PHONEPE MERCHANTS****")
        st.write("****EARN GREAT REWARDS****") 
        st.write("****MULTIPLE WAYS TO PAY****")
        st.write("****1. DIRECT TRANSFER AND MORE****")
        st.write("****2. QR CODE****")
          

    col5,col6 = st.columns(2)
    with col5:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.write("****NO WALLET TOP-UP REQUIRED****")
        st.write("****PAY DIRECTLY FROM ANY BANK TO ANY BANK ACCOUNT****")
        st.write("****INSTANTLY AND AT FREE OF COST****")
    with col6:
        st.video(r"C:\Users\mypc\Downloads\PhonePe - Introduction.mp4")


    

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select The Method",["Insurance Analysis","Transaction Analysis","User Analysis"])
        if method == "Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method == "Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)
            

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q =Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State based on Transaction type", Aggre_tran_tac_Y_Q["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)


        elif method == "User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q =Aggre_user_plot_2(Aggre_user_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for user analysis", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
            

    with tab2:
        method2 = st.radio("Select The Method",["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])
        if method2 == "Map Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min(),key="unique_key_for_year_slider")
            map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance,years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", map_insur_tac_Y["States"].unique())
            Map_insur_District(map_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Map Quarter", map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q =Transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State based on Transaction type (District wise)",map_insur_tac_Y_Q["States"].unique())
            Map_insur_District(map_insur_tac_Y_Q, states)
            


        elif method2 == "Map Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min(),key="unique_key_for_year_slider")
            map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction,years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", map_tran_tac_Y["States"].unique())
            Map_tran_District(map_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Map Quarter", map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q =Transaction_amount_count_Y_Q(map_tran_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State based on Transaction type(District Wise)",map_tran_tac_Y_Q["States"].unique())
            Map_tran_District(map_tran_tac_Y_Q, states)

        elif method2 == "Map User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year for Map User", Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min(),key="unique_key_for_year_slider")
            map_user_Y=map_user_plot_1(Map_user,years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter (Map User)",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for Map User",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, states)           


    with tab3:
        method3 = st.radio("Select The Method",["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])
        if method3 == "Top Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year Top Insurance", Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for top User",top_insur_tac_Y["States"].unique())
            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter TOP INSURANCE",top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)


        elif method3 == "Top Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year Top Transaction", Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for top transaction",top_tran_tac_Y["States"].unique())
            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter TOP TRANSACTION",top_tran_tac_Y["Quarter"].min(),top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y,quarters)
        
        
        elif method3 == "Top User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year Top User", Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            top_user_Y=top_user_plot_1(Top_user,years)

            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for top user",top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)

elif select == "TOP CHARTS":
    question=st.selectbox("Select the Question",["1. Insurance amount and Count of Aggregated Insurance",
                                                 "2. Transaction amount and Count of Map Insurance",
                                                 "3. Transaction amount and Count of Top Insurance",
                                                 "4. Transaction amount and Count of Aggregated Transaction",
                                                 "5. Transaction amount and Count of Map Transaction",
                                                 "6. Transaction amount and Count of Top Transaction",
                                                 "7. Transaction Count and Aggregated User",
                                                 "8. Registered users of Map User",
                                                 "9. App opens of Map User",
                                                 "10. Registered users of Top User",
                                                 "11. Top and least selling brands",
                                                 "12. Top, Least and Average transaction amounts",
                                                 "13. Top, Least and Average transaction counts",
                                                 "14. Brands and its percentage",
                                                 "15. Most and Least number of registered users with respect to pincodes"])
    
    if  question == "1. Insurance amount and Count of Aggregated Insurance":
        
        st.subheader("INSURANCE AMOUNT")
        top_chart_insurance_amount("aggregated_insurance")

        st.subheader("INSURANCE COUNT")
        top_chart_insurance_count("aggregated_insurance")

    elif  question == "2. Transaction amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif  question == "3. Transaction amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif  question == "4. Transaction amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif  question == "5. Transaction amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif  question == "6. Transaction amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif  question == "7. Transaction Count and Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif  question == "8. Registered users of Map User":
        
        states = st.selectbox("Select the state", Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user",states)

    elif  question == "9. App opens of Map User":
        
        states = st.selectbox("Select the state", Map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_appopens("map_user",states)

    elif  question == "10. Registered users of Top User":
        
        states = st.selectbox("Select the state", Top_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")

    elif  question == "11. Top and least selling brands":
        
        st.subheader("BRANDS")
        top_chart_top_brands("aggregated_user")

    elif  question == "12. Top, Least and Average transaction amounts":
        
        states = st.markdown("")
        st.subheader("TOP, LEAST & AVERAGE TRANSACTIONS AMOUNTS")
        top_chart_top_tran_amount("top_transaction",states)

    elif  question == "13. Top, Least and Average transaction counts":
        
        states = st.markdown("")
        st.subheader("TOP, LEAST & AVERAGE TRANSACTIONS COUNTS")
        top_chart_top_tran_count("top_transaction",states)

    elif  question == "14. Brands and its percentage":
        
        st.subheader("BRANDS AND ITS PERCENTAGE")
        top_chart_brands("aggregated_user")

    elif  question == "15. Most and Least number of registered users with respect to pincodes":
        
        st.subheader("PINCODES AND REGISTERED USERS")
        top_chart_pincodes_regusers("top_user")


    