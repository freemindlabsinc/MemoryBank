import streamlit as st
import src.components.page_configurator as page_config
from msal_streamlit_authentication import msal_authentication

page_config.initialize_page(
    icon="💠",
    title="AI Of You",
    desc="""
    This is the home page of the application.
    """,
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

login_token = msal_authentication(
    auth={
        "clientId": "aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",
        "authority": "https://login.microsoftonline.com/aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee",
        "redirectUri": "/",
        "postLogoutRedirectUri": "/"
    }, # Corresponds to the 'auth' configuration for an MSAL Instance
    cache={
        "cacheLocation": "sessionStorage",
        "storeAuthStateInCookie": False
    }, # Corresponds to the 'cache' configuration for an MSAL Instance
    login_request={
        "scopes": ["aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeee/.default"]
    }, # Optional
    logout_request={}, # Optional
    login_button_text="Login", # Optional, defaults to "Login"
    logout_button_text="Logout", # Optional, defaults to "Logout"
    class_name="css_button_class_selector", # Optional, defaults to None. Corresponds to HTML class.
    html_id="html_id_for_button", # Optional, defaults to None. Corresponds to HTML id.
    key=1 # Optional if only a single instance is needed
)

st.write("Welcome to A.I. Of You! ")
st.write("""
This is the home page of the application. At some point it will show useful information about the app
and some diagrams or charts.

You can navigate to different modules using the sidebar on the left.
Only the following modules are functional right now:
""")

st.page_link("pages/2_📚_Prompt_Library.py", label=":blue[Prompt Library]", icon="📚")
st.page_link("pages/3_🪄_Prompt_Wizard.py", label=":green[Prompt Wizard]", icon="🪄")