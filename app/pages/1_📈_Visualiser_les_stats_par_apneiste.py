import streamlit as st
import pandas as pd

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.title("ABO stats")

st.write(
    """
    Ce tableau contient tous les statistiques des résultats des apnéistes lors des compétitions AIDA.
    (filtrage : l'apnéiste a plus de 5 compétitions effectuées, la derniére est après le 01-01-2021)
    """
)
df = pd.read_csv(r'././data/diver_stat.csv')
# app\pages\1_📈_Generating_AIDA_Depth_results.py
# df_filter = filter_dataframe(df)
st.write(f'Le tableau résultant contient {df.shape[0]} lignes')
st.dataframe(df, hide_index=True)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='aida_results_by_freediver.csv',
    mime='text/csv',
)
