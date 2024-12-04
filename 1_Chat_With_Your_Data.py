#1
import streamlit as st
# Test code
# st.header("TEST")

import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv # to read env file 

from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent #agent tool to work with pandas dataframe

from langchain_openai import ChatOpenAI #import open ai model

from src.logger.base import BaseLogger # import logger from src 
from src.model.llms import load_llm # import llm model from src
from src.utils import execute_plt_code # import function to execute plt code
#2
#load environment variables
load_dotenv()
logger = BaseLogger()
MODEL_NAME = 'gpt-3.5-turbo'

#5
def process_query(da_agent,query):
    response = da_agent(query) # process query with data analysis agent
    action= response['intermediate_steps'][-1][0].tool_input['query'] # create and display the code generated from agent 
    
    if 'plt' in action: 
        st.write(response['output']) # this only display the message , not the plot 
        
        fig= execute_plt_code(action, df= st.session_state.df) # function to execute the code from action
        if fig:
            st.pyplot(fig)

        st.write("**Executed Code:**")
        st.code(action)

        
    
    else: 
        st.write(response['output'])
        st.session_state.history.append(query,response['output']) # append query and response to chat history

#6
def display_chat_history():
    st.markdown('###Chat History:')
    for i, (query, response) in enumerate(st.session_state.history):
        st.markdown(f'**{i+1}. Query:** {query}')
        st.markdown(f'**{i+1}. Response:** {response}')
        st.write('---')

#4
def main():
    # Set up streamlit interface
    st.set_page_config(page_title='Let chat with your data', page_icon='📊', layout='centered', initial_sidebar_state='expanded') # page title for main webpage
    st.header('Smart Data Analyst Assistant')# header for main webpage
    st.write('### Welcome to our data analysis tool. This tool can assist you with data analysis and visualization. You can upload your data and ask questions about your data. The tool will help you to analyze and visualize your data. Let\'s get started!') # description of the tool



    # Load llm models (create separate function file to load llm model)
    llm= load_llm(model_name=MODEL_NAME)
    logger.info(f'### Successfull: Loaded {MODEL_NAME} model')

    # Upload CSV file

    with st.sidebar:  
        uploaded_file= st.file_uploader("Upload your csv file here",type='csv') # package of streamlit to upload file


    #Inital chat history
    if 'history' not in st.session_state:
        st.session_state['history']=[]  # Initialize chat history contain query and response to LLM

    #Read csv file
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)  # session state to store data from csv file
        st.write('### Your uploaded data: ', st.session_state.df.head()) # test and display data from csv file

    #Create data analysis agent to query with your data
    da_agent= create_pandas_dataframe_agent(
        llm= llm,
        df=st.session_state.df,
        agent_type = 'tool-calling', # tool calling is recommended
        allow_dangerous_code=True, # allow agent to run python code
        verbose= True, # display agent thingking process
        return_intermediate_steps= True, # return intermediate steps to view the code inside
    )

    logger.info('### Successfull: Created data analysis agent')
    #Input query and process query

    query = st.text_input('Ask me anything about your data: ') # input query from user

    if st.button('Run_query'): #after put query, click button to run query
        with st.spinner('Processing...'):  # when agent is processing, display processing message spinning
            process_query(da_agent, query)


    #Display chat history
    st.divider()
    display_chat_history()


#3
if __name__=='__main__':
    main()







