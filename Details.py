import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.dataframe_explorer import dataframe_explorer
import altair as alt
from streamlit_gsheets import GSheetsConnection
from babel.numbers import format_currency

    
def app():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="1",usecols=list(range(7)))

    st.dataframe(df)

 #------------------------------------------------------------------------------------------------------------------   
#Preparing for dates selections
  
    
def app():
    
    st.header('Details',divider='rainbow')
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Main", usecols=list(range(7)),ttl=3)

    

    
    # Map month names to their corresponding numeric values
    month_mapping = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    df['Month'] = df['Month'].map(month_mapping)
    
    
    # Combine the day, month, and year columns into a single datetime column
    df['date'] = pd.to_datetime(df[['Day', 'Month', 'Year']])

        
    
        


#-----------------------------------------------------------------------------------------------------------------------
#Date range selection
  
    # Let the user select a date using Streamlit's date input widget
    col1,col2=st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=datetime.now())
    with col2:
        end_date = st.date_input("End date", value=datetime.now())

    

    # Filter the dataframe based on the selected date range
    mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
    df2= df.loc[mask]
    st.error("You have selected dates from " + str(start_date)+ "  to  " + str(end_date))
    columns_to_display = ['date', 'Type', 'Particulars', 'Amount', 'Description']  # Change these to your actual column names
    df2 = df2[columns_to_display]
    st.dataframe(df2,use_container_width=True)
    # Display the dataframe according to the selected date range
    
#----------------------------------------------------------------------------------------------------------------------

#Visualization


    # Aggregate the selected range of data
    expenses = df2[df2['Type'] == 'Expense'].groupby('Particulars', as_index=False)['Amount'].sum()
    receives = df2[df2['Type'] == 'Receive'].groupby('Particulars', as_index=False)['Amount'].sum()
    #Plotting the aggregated data within the selected range
    receives_chart = alt.Chart(receives).mark_bar().encode(
        x='Particulars',
        y='Amount',
        color='Particulars'
    ).properties(
        
    )

    receives_text = receives_chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Adjust the position of the text
    ).encode(
        text='Amount:Q'
    )

    expenses_chart = alt.Chart(expenses).mark_bar().encode(
        x='Particulars',
        y='Amount',
        color='Particulars'
    ).properties(
    )

    expenses_text = expenses_chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Adjust the position of the text
    ).encode(
        text='Amount:Q'
    )

    
    
    
    st.subheader('Receives')
    st.altair_chart(receives_chart + receives_text, use_container_width=True)

    st.subheader('Expenses')
    st.altair_chart(expenses_chart + expenses_text, use_container_width=True)
    


# Table

    #Calculation
    total_receives = receives['Amount'].sum()
    total_expenses = expenses['Amount'].sum()
    balance= total_receives - total_expenses

    receives['Amount'] = receives['Amount'].apply(lambda x: format_currency(x, 'INR', locale='en_IN'))
    expenses['Amount'] = expenses['Amount'].apply(lambda x: format_currency(x, 'INR', locale='en_IN'))

    #Converting values in Indian Currency ₹
    total_receives = format_currency(total_receives, 'INR', locale='en_IN')
    total_expenses = format_currency(total_expenses, 'INR', locale='en_IN')
    balance = format_currency(balance, 'INR', locale='en_IN')

    # Display aggregated data in table format
    a,b=st.columns(2)
    with a:
        st.subheader("Receives")
        st.table(receives[['Particulars', 'Amount']])
    with b:
        st.subheader("Expenses")
        st.table(expenses[['Particulars', 'Amount']])
        
    a1,a2,a3=st.columns(3)
    with a1:
        st.write(f"**Total Receives: {total_receives}**")
    with a2:
        st.write(f"**Total Expenses: {total_expenses}**")
    with a3:
        st.write(f"**Balance: {balance}**")

    with st.expander("Filtered Data"):
        filtered_df=dataframe_explorer(df2,case=False)
        st.dataframe(filtered_df,use_container_width=True)
        