import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Startup Analysis')

df = pd.read_csv("Startup_cleaned_data.csv")

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month

# Print the dataframe
#st.dataframe(df)

def load_overall_analysis():
    st.header("Overall Analysis of Startups and Investors")

    #total invested amout
    total = round(df['Amount'].sum(),2)
    # Max amount invested
    max_invested = round(df.groupby('Startup')['Amount'].max().sort_values(ascending=False).head(1).values[0],2)

    avg_invested = round(df.groupby('Startup')['Amount'].sum().mean(),2)

    total_startups = round(df.groupby('Startup')['Startup'].count().sum(),2)

    col1,col2,col3,col4 = st.columns(4)
    
    with col1:
        st.metric("Total Amount Invested", str(total) + "CR")
    with col2:
        st.metric("Max Amount Invested", str(max_invested) + "CR")
    with col3:
        st.metric("Avg. Amount Invested", str(avg_invested) + "CR")
    with col4:
        st.metric("total startups funded", str(total_startups))


    #MOM Chart
    st.header("Month on Month Graph")
    
    temp_df = df.groupby(['year','month'])['Amount'].sum().reset_index()
    temp_df['X_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    #year = st.selectbox('Select year', temp_df['year'].unique())
    #btn = st.button("MOM Chart")
    #if btn:
    fig, ax = plt.subplots()
    ax.plot(temp_df['X_axis'], temp_df['Amount'])
    ax.set_xticklabels(temp_df['X_axis'].to_list(), rotation = 90)
    st.pyplot(fig)

    
def load_investor_details(investor):

    st.title(investor)

    #Get the recent 5 invesments by the investor

    recent_5 = df[df['Investors Name'].str.contains(investor)].head()
    st.header("Most Recent Investments")
    st.dataframe(recent_5)

    col1, col2 = st.columns(2)
    with col1:
         # Total Investments
        total_Investments = df[df['Investors Name'].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False)
        st.header("Biggest Investments")
        st.dataframe(total_Investments)
    
    with col2:
        fig, ax = plt.subplots()
        ax.bar(total_Investments.index, total_Investments.values)
        ax.set_xticklabels(total_Investments.index.to_list(), rotation = 90)
        st.pyplot(fig)

    # Sector wise imvestments
    st.header("Sector wise imvestments")
    sectors = df[df['Investors Name'].str.contains(investor)].groupby('Industry Vertical')['Amount'].sum()
    fig, ax = plt.subplots()
    ax.pie(sectors, labels=sectors.index, autopct="%0.01f")
    st.pyplot(fig)

    # YOY Growth
    st.header("YOY Growth")
    YOY_growth = df[df['Investors Name'].str.contains(investor)].groupby('year')['Amount'].sum()
    fig, ax = plt.subplots()
    ax.plot(YOY_growth)
    st.pyplot(fig)

st.sidebar.title("Startups Funding Analysis")

chosen_option = st.sidebar.selectbox("Select one", ['Overall Analysis', 'Startup', 'Investors'])

if chosen_option == 'Overall Analysis':
    but0 = st.sidebar.button("Show overall analysis")
    if but0:
        load_overall_analysis()
elif chosen_option == 'Startup':
    startup = st.sidebar.selectbox("Select Startup",df['Startup'].unique().tolist())
    st.sidebar.button("Startup Analysis")
    st.header(startup)
elif chosen_option == 'Investors':
    selected_Investor = st.sidebar.selectbox("Select Investor",sorted(set(df['Investors Name'].str.split(',').sum())))
    btn2 = st.sidebar.button("Investor Details")
    if btn2:
        load_investor_details(selected_Investor)



