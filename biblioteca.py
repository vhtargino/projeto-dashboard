# funcoes.py
import streamlit as st
import datetime

#funcao utilizada pelos criterios [0, 7, 13, 16, 19]:
#função para obter um intervalo de datas a partir da 
#entrada do usuário em um formato específico (DD.MM.YYYY).
def input_periodo():
    st.subheader('Período: \n')
    periodo = st.date_input(
        "Selecione o período desejado",
        (datetime.date(datetime.datetime.now().year, 1, 1), datetime.date.today()),
        datetime.date(datetime.datetime.now().year, 1, 1),
        datetime.date(datetime.datetime.now().year, 12, 31),
        format="DD.MM.YYYY",
    )
    return periodo
