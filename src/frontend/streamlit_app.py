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


# Sidebar
st.sidebar.header("API Key")
api_key = st.sidebar.text_input("OpenAI_API_Key")
if api_key[0:3] == "sk-":
    # Validate and add the API key to the session (implement validation)
    st.session_state['api_key'] = api_key
    st.sidebar.text("(not stored)")
else:
    raise Exception("Invalid API Key")

# Sidebar - Cucumber GPT info
st.sidebar.markdown("### Cucumber GPT")
st.sidebar.markdown("A tool to create feature files and test steps. [GitHub](Your_GitHub_Link)")

# Main Page
st.title("Cucumber GPT" + (" -- " + st.session_state.get('app_name', '') if 'app_name' in st.session_state else ''))
st.subheader("Create feature files and test steps using the requirements of your project.")

# Name of Application Input
app_name = st.text_input("Name of Application", value="your application name here")

# Submit Button for Application Name
if st.button("Submit Application Name"):
    st.session_state['app_name'] = app_name
    st.experimental_rerun()

# File Upload
uploaded_file = st.file_uploader("Upload your requirements", type="txt")
if uploaded_file is not None:
    # Process and display uploaded file
    st.write("Uploaded Requirements:")
    st.text(uploaded_file.getvalue().decode("utf-8"))

# Instructions for file upload
st.write("📄 Please go ahead and upload your requirements as a .txt file, one requirement per line.")

# Submit Button for Processing Requirements
if st.button("Process Requirements"):
    with st.spinner('Processing...'):
        process_reqs(uploaded_file)
        time.sleep(5)  # Simulate processing time
    st.success('Processing Complete!')

# Output Box
output_container = st.empty()
if 'requirements' in st.session_state:
    output_container.text_area("Output", value=st.session_state['requirements'], height=300)

# GoCucumberGo Button
if st.button("GoCucumberGo"):
    with st.spinner('Working...'):
        # Implement the logic for GoCucumberGo
        time.sleep(5)  # Simulate processing time
    st.success('Done!')

# Display created files
st.markdown("### Created Files")
for file in get_created_files():
    st.write(file)

# Link to GitHub
st.markdown("[GitHub Repository](Your_GitHub_Link)")



