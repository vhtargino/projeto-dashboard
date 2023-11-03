import streamlit as st
import pandas as pd
import os

st.set_page_config()

def file_selector(diretorio="C:\Planilhas"):
    arquivos = os.listdir(diretorio)
    arquivo_selecionado = st.selectbox("Escolha um arquivo", arquivos)
    return os.path.join(diretorio, arquivo_selecionado)


with st.container():
    st.header("Dashboard")
    st.write("Por favor, armazene a planilha no diretório C:\\Planilhas. Caso o diretório não exista, crie-o.")

with st.container():
    st.write("---")
    diretorio_planilha = file_selector()  # Leitura do diretório da planilha
    st.write("Você escolheu `%s`" % diretorio_planilha)
    df = pd.read_excel(diretorio_planilha)

with st.container():
    st.write("---")
    st.dataframe(df)
