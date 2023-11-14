import os
import json
from datetime import datetime
import timeit
from dotenv import load_dotenv
import openai
import wandb
from langchain.chat_models import ChatOpenAI
import random
from datetime import datetime


#Logging etc
#from gen_logger.logger_util import setup_logger
from langchain.globals import set_verbose, set_debug
from langchain.callbacks import WandbCallbackHandler, StdOutCallbackHandler  
from langchain.callbacks import wandb_tracing_enabled
#from logs.wandb_langchain import wandb_callback
#from wandb_langchain import wandb_callback, callbacks
import textstat
import spacy


from operator import itemgetter
from langchain.schema.runnable import RunnableParallel
from langchain.schema import StrOutputParser
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.output_parsers.list import NumberedListOutputParser
from langchain.output_parsers import ListOutputParser
from langchain.schema import messages_to_dict 
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap, RunnablePassthrough

#from humanloop import Humanloop


#Input placeholders 

load_dotenv()
#_logger=setup_logger("langllm")
os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
os.environ["WANDB_PROJECT"] = "avin-midi"
#humanloop = Humanloop(api_key=os.getenv("HUMANLOOP_API_KEY"))

#set_debug(True)
set_verbose(True)

def mlops_config():
    
    '''

    Initialize MLOps and LLMOps tools.

    '''    

    try:
        wandb.login(key=os.getenv("WANDB_API_KEY"))
        wandb.init(project=os.getenv("WANDB_PROJECT"))
        
        
        prediction_table = wandb.Table(columns=["logTime", "func" "prompt", "prompt_tokens", "completion", 
                                                "completion_tokens", "time"])
    except Exception as e:
        _logger.error(e)

    try:
        _logger.info(f"Adding openAI API key")
        #callbacks = [StdOutCallbackHandler(), wandb_callback]
        model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo") 
        _logger.info("init llm complete. Model is {}".format(model.model_name))
    except AuthenticationError as e:
        _logger.error(e)
    try:
        project_response = humanloop.projects.create(name="{{audiato}}-gavinMIDI")
        project_id = project_response.body["id"]
        _logger.info(project_id.body["id"])
    except humanloop.errors.HumanloopError as e:
        _logger.error(e)
    try: 
        humanloop.projects.update_feedback_types(
        id=project_id,
        body=[{
        "type": "action", 
        "class": "multi_select", 
        "values": [
          {"value": "copied"}, {"value": "saved"}
        ],
        }]
    )
        humanloop.model_configurations.register(
        project="{{audiato}}-gavinMIDI",
        model="gpt-3.5-turbo",
        prompt_template="Write a snappy introduction about {{topic}}:",
        temperature=0.3,
)
    except humanloop.errors.HumanloopError as e:
        _logger.error(e)
            


    
    

def image_of_description(description):
    #Make an image of the song description
    image_req = openai.Image.create(prompt=f"A futuristic anime image vibrants representative of a song that is: {description}",
    n=0,
    size="1024x1024"
    )

    image_res = image_req["data"][0]
    
    print(image_res)
    return image_res

def final_dump(chain):   
    '''
    Add the final outputs to the json files
    '''
    try:
        json_path = f"{getattr(chain,__name__)}_{datetime.now().date()}.json"
        with open(os.path.join('./data/json/', json_path), 'w', encoding='json') as f:
            json.dump({getattr(chain,__name__)}, f, indent=4)
        _logger.info(f"All Complete and final JSON saved to: {os.path.abspath(json_path)}")
    except Exception as error:
        _logger.error(error, exc_info=True)
    
    return _logger.info(f"{getattr(chain,__name__)} saved to {json_path}")


'''

Prompt Templates for the chain of calls to the model of choice:

'''

model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-3.5-turbo") 
prompt1 = ChatPromptTemplate.from_template(
    """You are an expert product manager. The business you are managing is {type_business} \
        You will be given a list of requirements. \
        Using the requirements you will analyze the project and break the requirements into user stories. \
        The user stories will have the form of "As a role, I want goal so that description" \
        Roles include: %[Developer, User, Project Manager, Business_Owner] \
        Goals will be in alignment with the requirements.   \ 
        Descriptions will be short and concise, but accurate. \
        Write the user stories into a numbered list.
        ********************
        The Requirements are:
        %{requirements}%
        Remove all new line markers.
        Output only a numbered list.
        1.
    """
)
prompt2 = ChatPromptTemplate.from_template(
    """You are an expert at translating user stories into Cucumber Feature Files in the Gherkin Langugage. 
        Feature files outline the test conditions for evaluating each user story. 
        The user stories are:
        {user_stories}
        
        Feature files are plain text files with a .feature extension. 
        Each Feature file has the format: 
        Given: 
        When: 
        Then: 
        Go through all the user stories and write a feature file for each. 
        Do not repeat the user story. Output the feature files in a numbered list.
        ***********
        Output only each feature file in the format given. Remove all new line markers. Numbered list.
        1.
        **********
    """)

#Can generate the colors of the song and make a User Interface.
prompt3 = ChatPromptTemplate.from_template(
    """You are an expert at writing MIDI for songs. Take the following chords:
    ********
    {chords}
    ********* 
    - Use MIDI notation. Write the synth, bass and drum MIDI notes for the {element} with random and rhythmic velocity.
    - Choose a Key Based on the.
    Synth:
    Bass:
    - Velocity will move with the lyrics and chords
    - Leave Rhythm empty for the next step
    - Remove all new line characters "\n"
    - Prepare only 4 bars
    - Output onky the JSON ObjectMIDI.
    """)

prompt4 = ChatPromptTemplate.from_template(
    """
    Write Rhythm of the Song in MIDI Notation. Use the following information as reference:
    ***************
    -{midi_dict} and 
    -{chords}
    ***************
    
    -Use 4/4 time in Traditional Western Notation at 
    - tempo is 65bpm.
    - For duration use floating points and quarter notes eg 0.25
    - Use standard MIDI notation to show the rhythm.
    - Remove all new line characters "\\n"
    -Insert the output into the rhythm key of the midi_dict JSON Object
    - Output nothing but a JSON Object.
    """
)

prompt5 = ChatPromptTemplate.from_template(
    """You are a MIDI expert and AI Assistant. You will perform the tasks in order and accurately.
    1. Merge the following two JSON Objects into one.
    2. Add the rhythm as a key to the midi JSON Object.
    3. Remove unnecessary information eg. new line characters
    4. Format correctly as JSON:
    **************
    1. {midi}
    merged with:
    2.{rhythm}
    ************
    Output a JSON object. Nothing Else.
    Example: {"midi":{...},"rhythm":{...}}
 """   
)

#Config:

song_name = "Eat Fresh Daisys"
description = "A warm blues vibe, beers on a sunny day."
model_parser = model | StrOutputParser()
json_parser = model | SimpleJsonOutputParser()
list_parser = model | NumberedListOutputParser()
song_add = f"{datetime.now().date()}_{song_name[0:4]}"
file_name = f"{song_add}_Gavin_agoodtime.txt"

#chains
user_stories_chain = {"requirements":RunnablePassthrough(), "type_business": RunnablePassthrough()} | prompt1 | {"user_stories":model_parser} 
feature_file_chain =  {"user_stories": user_stories_chain} | prompt2 | {"feature_files":list_parser}

'''chords_to_midi = {"element": itemgetter("element"), "chords": chords} | prompt3 | {"midi": json_parser}
midi_to_rhythm = {"midi_dict": chords_to_midi, "chords":chords} | prompt4 | {"rhythm":json_parser}
final_chain = {"midi": chords_to_midi, "rhythm": midi_to_rhythm} | prompt5 | json_parser'''


try:
    #_logger.info("starting chains")
    user_stories_run = user_stories_chain.invoke({"requirements": "['Login screen', 'Sign up screen', 'Home screen']", "type_business": "Music Application"})
    print(user_stories_run)
    #print(user_stories)
    feature_files = feature_file_chain.invoke({"user_stories": user_stories_run})
    print(feature_files)
except Exception as e:
    print(e)
    '''_logger.info(f"{song_desc}")
    song_desc_str = str(song_desc)
    _logger.info(f"song description complete")
    _logger.info(f"First 24 characters: {(song_desc_str.split())[0:25]}")
    chords_list, new_memory = chords.invoke({"song_name": song_name, "song_description": song_desc}, memory)
    _logger.info(f"Chords list complete")
    _logger.info(chords_list)
    midi_list, new_memory = chords_to_midi.invoke({"element": "verse", "chords": chords_list, "song_name": song_name}, memory)
    _logger.info(f"Midi list complete")
    _logger.info(midi_list)
    final_dump(midi_list)
    _logger.info("Midi list JSON dump complete")
    rhythm_midi, new_memory = midi_to_rhythm.invoke({"rhythm_dict": midi_list, "chords":chords_list, "element": "verse"}, memory)
    _logger.info(f"Rhythm list complete")
    _logger.info(rhythm_midi)
    final_dump(rhythm_midi)
    _logger.info("Rhythm list JSON dump complete")
    final_out, new_memory = final_chain.invoke({"midi":midi_list, "rhythm":rhythm_midi, "element":"verse", "description": description, "song_name": song_name}, memory)
    _logger.info("Final out complete...")
    _logger.info(final_out)
    final_dump(final_out)
    _logger.info("Complete....writing file")
except Exception as e:
    _logger.error(e, exc_info=True)
    os.remove('./data/cmd_chain_gav.txt')
    os.remove(file_name)
    with open('./data/partial.txt', 'w') as f:
        try:
            f.write(f"00----The Noble Song: {song_name} at 65 bpm----00\n\n")
            f.write(str(song_desc).splitlines())
            f.write(f"\n00----The Chords of {song_name}----00\n\n")
            f.write(str(chords_list))
            f.write("\n00----The MIDI----00\n\n")
            f.write(json.dumps(midi_list, indent=4))
            f.write("\n00----The Rhythm------00\n\n")
            f.write(json.dumps(rhythm_midi, indent=4))
            f.write("\n\n\n00----The Final Out------00\n\n\n")
            f.write(json.dumps(final_out, indent=4))
            f.write(f"\n\n\n00----The EDN------00\n\n\n")
        except Exception as err:
            _logger.error(err, exc_info=True)
            os.remove('./data/cmd_chain_gav.txt')
            if os.path.exists(file_name):
                os.remove(file_name)
            else:
                pass

#Write to final file
with open(os.path.join('./data/songs/', file_name), 'w') as f:
    f.write(f"00----The Noble Song: {song_name} at 65 bpm----00\n\n")
    f.write(str(song_desc[0].replace("\n", " ")))
    f.write(f"\n00----The Chords of {song_name}----00\n\n")
    f.write(str(chords_list))
    f.write("\n00----The MIDI----00\n\n")
    f.write(json.dumps(midi_list, indent=4))
    f.write("\n00----The Rhythm------00\n\n")
    f.write(json.dumps(rhythm_midi, indent=4))
    f.write("\n\n00----The Final Out------00\n\n")
    f.write(json.dumps(final_out, indent=4))
    f.write("\n\n\n00----The EDN------00\n\n\n")
    
_logger.info(f"All Complete and file saved to: {os.path.abspath(file_name)}")'''



    

    
    
    
    
    
   
