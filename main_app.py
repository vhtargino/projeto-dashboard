import streamlit as st
import pandas as pd
import datetime

# Configuração da página
st.set_page_config(page_title='Dashboard Prontovida',
                   layout='wide')

# Título principal
with st.container():
    st.header('Dashboard Prontovida', divider='red')
    st.write('')
    st.write('')

# Criação e organização do menu lateral
with st.sidebar:
    st.header('Critérios a serem utilizados')

    checkboxes = [
        st.checkbox('Data de Internação'),
        st.checkbox('Semana Epidemiológica'),
        st.checkbox('Gênero'),
        st.checkbox('Idade'),
        st.checkbox('Município de residência'),
        st.checkbox('Sintomas'),
        st.checkbox('Data dos sintomas'),
        st.checkbox('Comorbidades'),
        st.checkbox('Tipo de leito'),
        st.checkbox('Hipótese diagnóstica'),
        st.checkbox('Finalização do caso'),
    ]

# Colunas para centralizar o widget de carregamento do arquivo
col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:
    planilha_excel = st.file_uploader('Arraste e solte um arquivo no espaço abaixo:',
                                      type='xlsx',
                                      label_visibility='collapsed')
    st.write('')
    st.write('')

with col3:
    st.write('')

# Condicional para notificar o usuário que nenhum arquivo foi adicionado
# Caso o arquivo seja adicionado, cria a variável df
if planilha_excel is None:
    st.warning('Adicione um arquivo para carregar a planilha', icon="⚠️")
    st.write('')
else:
    df = pd.read_excel(planilha_excel)

# Implementação da pesquisa dentro de um try-except para tratamento de erro
try: 
    todos_generos = df['SEXO']
    generos_unicos = sorted(set(todos_generos))

    menor_idade = df['IDADE'].min()
    maior_idade = df['IDADE'].max()

    todos_municipios_residencia = df['MUNICIPIO DE RESIDENCIA']
    municipios_residencia_unicos = sorted(set(todos_municipios_residencia))

    sintomas = df['SINTOMAS']
    todos_sintomas = ';'.join(sintomas).split(';')
    sintomas_unicos = sorted(set(todos_sintomas))

    comorbidades = df['COMORBIDADES']
    todas_comorbidades = ';'.join(comorbidades).split(';')
    comorbidades_unicas = sorted(set(todas_comorbidades))

    tipos_leitos = df['LEITO']
    tipos_leitos_unicos = sorted(set(tipos_leitos))

    hipotese_diagnostica = df['HIPOTESE DIAGNOSTICA']
    todas_hipoteses_diagnosticas = ';'.join(hipotese_diagnostica).split(';')
    hipoteses_diagnosticas_unicas = sorted(set(todas_hipoteses_diagnosticas))

    finalizacoes_casos_limpos = []
    finalizacoes_casos = df['FINALIZACAO DO CASO']

    for item in finalizacoes_casos:
        if isinstance(item, str):
            finalizacoes_casos_limpos.append(item)

    finalizacoes_casos_limpos_unicos = sorted(set(finalizacoes_casos_limpos))

    criterios_selecionados = []

    for i in range(len(checkboxes)):
        if checkboxes[i]:
            criterios_selecionados.append(i)

    if len(criterios_selecionados) == 0:
        st.warning('Informe pelo menos um critério de busca', icon="⚠️")

    if len(criterios_selecionados) > 0:
        st.header('Critérios escolhidos\n')
        st.divider()

        resultado_final = df.copy()

        for criterio in criterios_selecionados:

            if criterio == 0:
                st.subheader('Período de internação\n')
                periodo_internacao = st.date_input(
                    "Selecione o período desejado",
                    (datetime.date(datetime.datetime.now().year, 1, 1), datetime.date.today()),
                    datetime.date(datetime.datetime.now().year, 1, 1),
                    datetime.date(datetime.datetime.now().year, 12, 31),
                    format="DD.MM.YYYY",
                )

                data_inicio, data_fim = periodo_internacao
                data_inicio = datetime.datetime.combine(data_inicio, datetime.time.min)
                data_fim = datetime.datetime.combine(data_fim, datetime.time.max)

                if periodo_internacao:
                    filtro_data_internacao = (df['INTERNAÇÃO'] >= data_inicio) & (df['INTERNAÇÃO'] <= data_fim)
                    resultado_final = resultado_final[filtro_data_internacao]

            if criterio == 1:
                st.subheader('Semana Epidemiológica\n')
                semana_epidemiologica_comeco = st.number_input('Escolha o número da semana epidemiológica inicial', min_value=1, max_value=52, step=1)
                semana_epidemiologica_termino = st.number_input('Escolha o número da semana epidemiológica final',min_value=semana_epidemiologica_comeco, max_value=52, step=1)
                filtro_semana_epidemiologica = (df['SEMANA Nº'] >= semana_epidemiologica_comeco) & (df['SEMANA Nº'] <= semana_epidemiologica_termino)
                resultado_final = resultado_final[filtro_semana_epidemiologica]

            if criterio == 2:
                st.subheader('Gênero\n')
                genero_paciente = st.selectbox(
                    'Qual o gênero declarado do/da paciente?',
                    generos_unicos
                )
                resultado_final = resultado_final[resultado_final['SEXO'] == genero_paciente]

            if criterio == 3:
                st.subheader('Idade\n')
                faixa_etaria = st.slider('Faixa etária', min_value=menor_idade, max_value=maior_idade, value=[menor_idade, maior_idade], step=1)
                filtro_faixa_etaria = (df['IDADE'] >= faixa_etaria[0]) & (df['IDADE'] <= faixa_etaria[1])
                resultado_final = resultado_final[filtro_faixa_etaria]

            if criterio == 4:
                st.subheader('Município de residência\n')
                opcao_municipio_residencia = st.multiselect('Qual o município de residência do paciente?', municipios_residencia_unicos)
                resultado_final = resultado_final[resultado_final['MUNICIPIO DE RESIDENCIA'].isin(opcao_municipio_residencia)]

            if criterio == 5:
                st.subheader('Sintomas\n')
                opcoes_sintomas = st.multiselect(
                    'Quais os sintomas do paciente?',
                    sintomas_unicos
                )
                if opcoes_sintomas:
                    filtro_sintomas = df['SINTOMAS'].str.contains('|'.join(opcoes_sintomas), case=False, na=False)
                    resultado_final = resultado_final[filtro_sintomas]

            if criterio == 6:
                st.subheader('Data dos sintomas\n')
                opcao_data_sintomas = st.date_input(
                    "Selecione o período desejado da data de início dos sintomas",
                    (datetime.date(datetime.datetime.now().year, 1, 1), datetime.date.today()),
                    datetime.date(datetime.datetime.now().year, 1, 1),
                    datetime.date(datetime.datetime.now().year, 12, 31),
                    format="DD.MM.YYYY",
                )

                data_inicio_sintomas = datetime.datetime(opcao_data_sintomas[0].year, opcao_data_sintomas[0].month, opcao_data_sintomas[0].day)
                data_fim_sintomas = datetime.datetime(opcao_data_sintomas[1].year, opcao_data_sintomas[1].month, opcao_data_sintomas[1].day)

                df['DATA DOS SINTOMAS'] = pd.to_datetime(df['DATA DOS SINTOMAS'], format="%d.%m.%Y")

                filtro_data_sintomas = (df['DATA DOS SINTOMAS'] >= data_inicio_sintomas) & (df['DATA DOS SINTOMAS'] <= data_fim_sintomas)
                resultado_final = resultado_final[filtro_data_sintomas]

            if criterio == 7:
                st.subheader('Comorbidades\n')
                opcoes_comorbidades = st.multiselect(
                    'Informe as comorbidades',
                    comorbidades_unicas
                )
                if opcoes_comorbidades:
                    filtro_comorbidades = df['COMORBIDADES'].str.contains('|'.join(opcoes_comorbidades), case=False, na=False)
                    resultado_final = resultado_final[filtro_comorbidades]

            if criterio == 8:
                st.subheader('Tipos de leitos\n')
                opcao_tipo_leito = st.selectbox(
                    'Qual o tipo de leito?',
                    tipos_leitos_unicos
                )
                resultado_final = resultado_final[resultado_final['LEITO'] == opcao_tipo_leito]

            if criterio == 9:
                st.subheader('Hipótese diagnóstica\n')
                opcao_hipotese_diagnostica = st.multiselect(
                    'Informe a hipótese diagnóstica',
                    hipoteses_diagnosticas_unicas
                )
                filtro_hipotese_diagnostica = df['HIPOTESE DIAGNOSTICA'].str.contains('|'.join(opcao_hipotese_diagnostica), case=False, na=False)
                resultado_final = resultado_final[filtro_hipotese_diagnostica]

            if criterio == 10:
                st.subheader('Finalização do caso\n')
                opcao_finalizacao_caso = st.selectbox(
                    'Informe a finalização do caso',
                    finalizacoes_casos_limpos_unicos
                )
                resultado_final = resultado_final[resultado_final['FINALIZACAO DO CASO'] == opcao_finalizacao_caso]

        st.divider()
        st.write("\nResultados da pesquisa:")
        st.write(resultado_final)
except:
    st.write('')