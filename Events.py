import streamlit as st
import altair as alt
from babel.numbers import format_currency
from streamlit_gsheets import GSheetsConnection

def app():
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
    st.header("Events/Mission Trips", divider='rainbow')

    # Authentication and access setup for Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Manually specify the worksheet names if they are known
    worksheet_names = ["Victory Run ", "Delhi Mission Trip", "Sikkim-Nepal Mission Trip"," Delhi Mission Trip 2022-23","Thanksgiving 2023"]  # Replace with your actual worksheet names

    # Create a widget to select a worksheet
    selected_worksheet = st.selectbox("Select Events", options=worksheet_names)

    # Read data from the selected worksheet
    data = conn.read(worksheet=selected_worksheet, usecols=list(range(7)),ttl=3)

    # Display the dataframe
    st.dataframe(data,use_container_width=True)

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
    st.markdown(f"""<h1>{selected_worksheet}</h1>""",unsafe_allow_html=True)
    st.header('',divider='rainbow')
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