''' Miscellanous utilities for use by the application'''
import os
import streamlit as st

def add_created_files(filename):
    count = 0
    if count == 0:
        cr_files = []
        cr_files.append(filename)
        count += 1
    else:
        cr_files.append(filename)
    return cr_files

def list_files_in_subdirectory(subdirectory_name):
    """
    Lists files in a specified sub-directory.

    :param subdirectory_name: Name of the sub-directory.
    :return: A list of file names within the sub-directory.
    """
    subdirectory_path = os.path.join('.', subdirectory_name)  # Adjust the path as needed
    if not os.path.exists(subdirectory_path):
        print(f"No such directory: {subdirectory_path}")
        return []

    files = [f for f in os.listdir(subdirectory_path) 
             if os.path.isfile(os.path.join(subdirectory_path, f))]
    return files

def process_reqs(list_reqs, app_name):
    print(list_reqs)
    if os.path.join('.', f'{app_name}_CucumberGPT' f"{app_name}_requirements.txt"):
        pass
    with open(os.path.join('.', f'{app_name}_CucumberGPT', f'{app_name}_requirements.txt'), 'w') as f:
        f.write(f"Requirements for {app_name}\n\n")
        idx = 1
        for req in list_reqs:
            req=req.strip()
            f.write(f"{idx}. {req}\n")
            idx = idx + 1

def create_app_folder(app_name):
    """
    Creates a new folder for the application in the same folder.
    
    :param app_name: Name of the application provided by the user.
    """
    folder_name = f"{app_name}_CucumberGPT"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def create_step_file(app_folder, app_name, step):
    """
    Creates a new file for a specific step in the application process.
    
    :param app_folder: The folder where the file will be created.
    :param app_name: Name of the application.
    :param step: The current step of the application process.
    """
    file_name = f"{app_name}_{step}.txt"
    file_path = os.path.join(app_folder, file_name)
    with open(file_path, 'w') as file:
        file.write(f"{step} for {app_name}\n\n")
    return file_path

def chat_display(usr, data, proc):
    with st.chat_message(usr):
        if type(data) is list:
            for x in data:
                st.write(x)
        elif type(data) is str:
            st.write(data)
        elif type(data) is bytes:
            st.write(data.decode('utf-8'))
        
        st.session_state.messages.append({"role": usr, "content": data})

        if proc == "requirements":
            st.write("-----------")
            st.write("Voila - Requirements processed by CucumberGPT")
        elif proc == "featureFiles":
            st.write("-----------")
            st.write("Voila - Feature files processed by CucumberGPT")



    