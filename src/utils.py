import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def execute_plt_code(code: str, df: pd.DataFrame):
    ''' execute the code generated from agent to draw plot of figure 
     Args:
     code (str): action string ( contain plt code)
     df (pd.DataFrame): our dataframe

     Returns:
     _type: plt figure
     '''
    try:
        local_vars= {'plt':plt, "df":df}
        compiled_code= compile(code, '<string>', 'exec')
        exec(compiled_code, globals(),local_vars)

    except Exception as e:
        st.error('Error executing plt code: {e}')
        return None