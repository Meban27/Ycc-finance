import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection
from babel.numbers import format_currency
from datetime import datetime
import pandas as pd
def app():

#Styling the layout
    st.markdown("""
        <style>
            style.element{
                padding-top:0;
            }
            #ycc-finance{
                padding-top: 10px;
            }
    
            .card {
                background-color: #010F18;
                padding: 15px;
                border:2px solid #25243B;
                border-radius: 10px;
                box-shadow: 10px 7px rgba(2,2,26,0.9);
                margin-bottom: 20px;
                
            }
            .header {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }   
            .text{
                padding-top:10px;
                text-align: center;
            }
            .yo{
                font-size:13px;
            }      
         </style>
            """,unsafe_allow_html=True

    )
    


#------------------------------------------------------------------------------------  
#Loading the data
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Coffee machine", usecols=list(range(7)),ttl=3)

    
#Calculations

    #Calculation of receives
    tot_rec=data[(data["Type"]=="Receive")]
        #Calculate the amount receive
    receipt = tot_rec["Amount"].sum()
    
        
        
        #Calculation of expense
    tot_exp= data[(data["Type"]=="Expense")]
    expense= tot_exp["Amount"].sum()
   
    closing_balance= receipt-expense
    #Format currency
    receipt_display = format_currency(receipt, 'INR', locale='en_IN')
    expense_display = format_currency(expense, 'INR', locale='en_IN')
    closing_balance_display = format_currency(closing_balance, 'INR', locale='en_IN')
#-----------------------------------------------------------------------------------------------------------------   
    
    st.header('Coffee Machine',divider='rainbow')
#-----------------------------------------------------------------------------------------------------------------
    
    # Metric Section
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="card"><p class="yo">Total Receives</p><h3 class="text">{receipt_display}</h3></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="card"><p class="yo">Total Expenses</p><h3 class="text">{expense_display}</h3></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="card"><p class="yo">Closing Balance</p><h3 class="text">{closing_balance_display}</h3></div>', unsafe_allow_html=True)
    st.divider()

#----------------------------------------------------------------------------------------------------
#Calculation section

    # Aggregate data by summing amounts for each "Particulars"
    expenses = data[data['Type'] == 'Expense'].groupby('Particulars', as_index=False).sum()
    receives = data[data['Type'] == 'Receive'].groupby('Particulars', as_index=False).sum()
    total_receives = receives['Amount'].sum()
    total_expenses = expenses['Amount'].sum()

    #Display the values in Indian Currency ₹
    receives['Amount'] = receives['Amount'].apply(lambda x: format_currency(x, 'INR', locale='en_IN'))
    expenses['Amount'] = expenses['Amount'].apply(lambda x: format_currency(x, 'INR', locale='en_IN'))
    total_receives = format_currency(total_receives, 'INR', locale='en_IN')
    total_expenses = format_currency(total_expenses, 'INR', locale='en_IN')

   
#----------------------------------------------------------------------------------------------------------
#Data Visulization
    
    expenses = data[data['Type'] == 'Expense'].groupby('Particulars', as_index=False).sum()
    receives = data[data['Type'] == 'Receive'].groupby('Particulars', as_index=False).sum()
    # Create bar charts with text labels
   
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
    
#----------------------------------------------------------------------------------------------------------------
    st.divider()
#-----------------------------------------------------------------------------------------------------------------
    col1, col2 = st.columns(2)

    # Display aggregated data in table format
    with col1:
        st.subheader("Receives")
        st.table(receives[['Particulars', 'Amount']])
        st.write(f"**Total Receives: {total_receives}**")

    with col2:
        st.subheader("Expenses")
        st.table(expenses[['Particulars', 'Amount']])
        st.write(f"**Total Expenses: {total_expenses}**")

    st.header("",divider="rainbow")
    st.dataframe(data)
    st.header("",divider='rainbow')
#----------------------------------------------------------------------------------------------------------
# Map month names to their corresponding numeric values
    month_mapping = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }

    data['Month'] = data['Month'].map(month_mapping)
    
    
    # Combine the day, month, and year columns into a single datetime column
    data['date'] = pd.to_datetime(data[['Day', 'Month', 'Year']])
    col1,col2=st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=datetime.now())
    with col2:
        end_date = st.date_input("End date", value=datetime.now())

    

    # Filter the dataframe based on the selected date range
    mask = (data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))
    df2= data.loc[mask]
    st.error("You have selected dates from " + str(start_date)+ "  to  " + str(end_date))
    columns_to_display = ['date', 'Type', 'Particulars', 'Amount', 'Description']  # Change these to your actual column names
    df2 = df2[columns_to_display]
    st.dataframe(df2,use_container_width=True)
    expenses = df2[df2['Type'] == 'Expense'].groupby('Particulars', as_index=False)['Amount'].sum()
    receives = df2[df2['Type'] == 'Receive'].groupby('Particulars', as_index=False)['Amount'].sum()
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