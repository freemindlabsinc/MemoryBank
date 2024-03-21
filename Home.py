import streamlit as st
import src.components.page_configurator as page_config
import streamlit_authenticator as stauth
from streamlit_authenticator.validator import Validator
import yaml
from yaml.loader import SafeLoader

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
#--------------

class FixedAuthenticate(stauth.Authenticate): 
  def _implement_logout(self):
        # Clears cookie and session state variables associated with the logged in user.
        try:
            self.cookie_manager.delete(self.cookie_name)
        except Exception as e: 
            print(e)
        self.credentials['usernames'][st.session_state['username']]['logged_in'] = False
        st.session_state['logout'] = True
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.session_state['authentication_status'] = None

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = FixedAuthenticate(
    credentials= config['credentials'],
    cookie_name= config['cookie']['name'],
    key= config['cookie']['key'],
    cookie_expiry_days= config['cookie']['expiry_days'],
    preauthorized= config['preauthorized']
)

name, authenticated, username = authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    #st.stop()
    
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    
#--------------

# reset password
if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)    

# update user details        
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"]):
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
                
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)        
        
# forgot user name
try:
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username()
    if username_of_forgotten_username:
        st.success('Username to be sent securely')
        # The developer should securely transfer the username to the user.
    elif username_of_forgotten_username == False:
        st.error('Email not found')
except Exception as e:
    st.error(e)        
    
# forgot password

try:
    username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
    if username_of_forgotten_password:
        st.success('New password to be sent securely')
        # The developer should securely transfer the new password to the user.
    elif username_of_forgotten_password == False:
        st.error('Username not found')
except Exception as e:
    st.error(e)