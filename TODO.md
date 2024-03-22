NOW:
-Finish integrating Streamlit-Authenticator:
    - Without this we cannot do multi-user.
    - https://github.com/mkhorasani/Streamlit-Authenticator

- Integrate https://github.com/blackary/st_pages
    - This will allow us to manage multiple pages better and faster updates.
    - It has a really cool option to create menus from config files!
    - https://github.com/blackary/st_pages?tab=readme-ov-file#method-two-declare-pages-inside-of-a-config-file
    - I can change the pages\*.** so that each has a folder with a viewmodel!!! BIG WIN!!!

- Complete Prompt Library
    - Where do I store data (multi-tenant)?

        - CosmosDB (multi-tenant)

- Complete Prompt Wizard
    - Some of the toggles are not functioning now. Fix this.

-Port the llama-index work to MemoryBank
    This is necessary to store the data that AI will use in the various screens.

    - Can we use in-memory vector stuff for now?
        Installing ES shared is complicated. We could do this later.
        
    - Does CosmosDB support vector indexing?

    - Make sure we get data from:
        - YouTube
        - Google Drive
        - File Uploads (local data)

- Complete the prompt editor

- Complete the prompt wizard

    


LATER:
-Replace authentication and switch to OpenID Connect (OIDC)
    -https://github.com/mstaal/msal_streamlit_authentication
    -https://github.com/dentro-innovation/msal_streamlit_authentication
