import streamlit as st
from streamlit_option_menu import option_menu
import Details, Events, Coffee, Home, About

st.set_page_config(
    page_title="YCC Finance",
)

class Multiapp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):  # Added 'self' as the first parameter
        hide_st_style = """
        <style>
           header{
              
              padding-top:0px;
              border-top:0px;
              padding-top:0px;
           }
        </style>
        """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        with st.sidebar:
            app = option_menu(
                menu_title='YCC',
                options=['Home', 'Details', 'Events', 'Coffee Machine', 'About'],
                menu_icon='house-fill',
                default_index=0,
                styles={
                    "container": {"padding": "100px", "background_color": "red", "height": "100%", },
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "#080558"},
                    "nav-link-selected": {"background-color": "#02a21"},
                }
            )

            st.markdown("""**Note:** For the best experience, please view this dashboard in **landscape** mode on **mobile devices**. ***Thank you!***""")

        # Correct indentation of 'if' statements
        if app == "Home":
            Home.app()
        elif app == "Details":
            Details.app()
        elif app == "Events":
            Events.app()
        elif app == "Coffee Machine":
            Coffee.app()
        elif app == "About":
            About.app()

# Create an instance of Multiapp
multi_app = Multiapp()

# Add apps to the Multiapp instance
multi_app.add_app("Home", Home.app)
multi_app.add_app("Details", Details.app)
multi_app.add_app("Events", Events.app)
multi_app.add_app("Coffee Machine", Coffee.app)
multi_app.add_app("About", About.app)

# Call the run() method
multi_app.run()
 
