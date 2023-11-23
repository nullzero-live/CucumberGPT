''' Streamlit is a light weight front-end and will be used to:
- Upload a text file (todo other file)
- Process the lines and produce the list of requirements for the application

To be implemented externally and imported:
- Process files
- get created files
'''

import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import time
from utils.misc_utils import process_reqs, add_created_files, create_app_folder, create_step_file, list_files_in_subdirectory, chat_display
from utils.wait_emojis import wait_with_emoji
load_dotenv()

env_api_key = os.getenv("OPENAI_API_KEY")
requirements = None
st.session_state['messages'] = []


# Sidebar
st.sidebar.header("API Key")

if env_api_key != None:
    st.sidebar.text_input(type='password', help='sz-', label='OpenAI API Key')
    api_key = env_api_key
else:    
    api_key = st.sidebar.text_input('OpenAI_API_Key', type='password', help='sz-')
if api_key[0:3] == "sk-":
    # Validate and add the API key to the session (implement validation)
    st.session_state['api_key'] = api_key
    st.sidebar.text("(not stored)")
else:
    raise Exception("Invalid API Key")

# Sidebar - Cucumber GPT info
st.sidebar.markdown("### Cucumber GPT")
st.sidebar.markdown("A tool to create feature files and test steps.")
st.sidebar.markdown("[GitHub Repository](https://github.com/nullzero-live/CucumberGPT)")

# Main Page
st.title("Cucumber GPT" + (" -- " + st.session_state.get('app_name', '') if 'app_name' in st.session_state else ''))
st.text("Create feature files and test steps using the requirements of your project.")
app_name = st.text_input("Name of Application", help="your application name here")

# Submit Button for Application Name
if st.button("Submit"):
    st.session_state['app_name'] = app_name
    st.rerun()
    
if app_name is not None:
    proj_folder = create_app_folder(app_name)
    app_folder = str(os.path.join('.', proj_folder))
    

st.divider()

# Instructions for file upload
st.write("📄 Please go ahead and upload your requirements as a .txt file, one requirement per line.")

# File Upload
uploaded_file = st.file_uploader("Upload your requirements .txt file", type="txt")
if uploaded_file is not None:
    # Process and display uploaded file
    st.write("Uploaded Requirements:")
    st.text(uploaded_file.getvalue().decode("utf-8"))
    req_file = create_step_file(app_folder=app_folder, app_name=app_name, step="requirements")
    
    add_created_files(req_file)
    


# Submit Button for Processing Requirements
st.session_state['requirements'] = None
if st.button("Process Requirements", on_click=chat_display("ai", requirements, "requirements")):
    with st.spinner('Processing...'):
        print("processing reqs...")
        upload_parsed = uploaded_file.readlines()
        final_list = []
        for x in upload_parsed:
            x = x.decode('utf-8').replace('b','').strip()   
            final_list.append(x)
            
        upload_parsed = final_list
        requirements = process_reqs(upload_parsed, app_name)
        st.session_state['requirements'] = requirements
        
    st.success('Processing Complete!')
    
st.divider()    

# GoCucumberGo Button
if 'task_started' not in st.session_state:
    st.session_state['task_started'] = False
    
if st.button("GoCucumberGo🥒"):
    st.markdown("### Created Files")
    for file in list_files_in_subdirectory(f"{app_name}_CucumberGPT"):
        st.write(file)
    with st.spinner('Working...🥒🥒🥒🥒'):
        emojis = wait_with_emoji(5, time.sleep)
        st.write(f'{emojis}*🥒')
        # Implement the logic for GoCucumberGo    
    st.success('Done!')

# Chat interface
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Output Box
output_container = st.empty()
    
   
# Link to GitHub
st.markdown("[GitHub Repository](https://github.com/nullzero-live/CucumberGPT)")
st.markdown("Thanks :wave:")



