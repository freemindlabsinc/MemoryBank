import streamlit as st
import src.components.page_header as page_config
from st_pages import add_page_title, show_pages, Page, Section

add_page_title()


page_config.initialize_page(
    desc="""
    This is the home page of the application.
    """,
    menu_items={
        # TODO: point it to our WebSite
        'Get Help': 'https://www.extremelycoolapp.com/help',
        # TODO: point it to our Discord
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        # TODO: point it to our About page on the main website 
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

show_pages(
    [
        #Section("Home", "🏚️"),
        Page("app.py", "Home", "🏚️"),
        Page("pages/chat/chat.py", "Chat", "💬"),
        
        #Section("Prompts", "📜"), # This is a section title, not a page
        Page("pages/prompts/library.py", "Prompt Library", "📚"),
        Page("pages/prompts/wizard.py", "Prompt Wizard", "🪄"),   
        
        #Section("Data", "📜"), # This is a section title, not a page
        Page("pages/files/import.py", "Import", "📥"),        
        Page("pages/files/file_manager.py", "File Manager", "🗃️"),
                
        Page("pages/dictate/dictate.py", "Dictate", "🎙️"),        
    ]    
)

#st.write("Welcome to A.I. Of You! ")
st.write("""
This is the home page of the application. At some point it will show useful information about the app
and some diagrams or charts.

You can navigate to different modules using the sidebar on the left.
Only the following modules are (kinda) functional right now:
""")

st.page_link("pages/chat/chat.py", label=":blue[Chat]", icon="📚")
st.page_link("pages/prompts/wizard.py", label=":orange[Prompt Wizard]", icon="🪄")
st.page_link("pages/prompts/library.py", label=":green[Prompt Library]", icon="💬")