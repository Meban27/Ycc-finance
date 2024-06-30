import streamlit as st
def app():
    
    
    st.header('About this Dashboard',divider='rainbow')

    st.markdown("""
    Welcome to the **YCC Finance Dashboard**! This tool is designed to help YCC effectively track and manage our finances. Here's a quick overview of what you can find on each page:""")
    st.write('---')
    st.markdown("""
    ### 📊 Pages Overview
    1. **Home**: 
        - View detailed financial records of Offerings,Mission,Donations etc.
        - See the expenses for all activities.
    
   
    2. **Details**: 
        - Select a start and end date to visualize inflow of funds and expenses data over time.
    
    
    3. **Events**: 
        - Explore the expenses associated with our major projects,events and mission trips.
    
    
    4. **Coffee Machine**: 
        - See the revenue from Coffee Machine.
        - Check out the related expenses.""")

    
    st.write('---')
    st.markdown("""            
    ### 🔑 Key Features
    - **Interactive Widgets**: Customize your data view by selecting specific dates.
    - **Detailed Reports**: Access comprehensive records of offerings,donations, fundraising revenue,expenses and much more.
    - **User-Friendly Interface**: Navigate easily between pages to find the information you need.

    
    ### 📅 Data Coverage
    - **Time Period**: Our data ranges from **1st March 2020, to the present**.""")


    st.write('---')
    st.markdown("""#### Thank you for using the **YCC Finance Dashboard**. We hope it helps you better understand and manage our  finances.""")
    
