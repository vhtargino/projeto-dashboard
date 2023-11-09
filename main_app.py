import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from unidecode import unidecode
import matplotlib.pyplot as plt
import biblioteca as bib

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
    checkboxes = [st.checkbox(criterio) for criterio in ['Data de Internação', 'Semana Epidemiológica', 'Paciente', 'Sexo', 'Idade', 'Município de residência', 'Sintomas', 'Data dos sintomas', 'Comorbidades', 'Vacina', 'Tipo de leito', 'Evolução do Paciente', 'Exames', 'Data do exame', 'Hipótese diagnóstica', 'Notificação de Doença ou Agravo', 'Data da notificação', 'Finalização do caso', 'Detalhe da finalização do caso', 'Data da finalização do caso']]

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
    #criterio 0 - data
    #criterio 1 - semana numero, tratado diretamento no criterio
    #criterio 2
    todos_pacientes = df['PACIENTE']
    pacientes_unicos = sorted(set(todos_pacientes))
    #criterio 3
    todos_generos = df['SEXO']
    generos_unicos = sorted(set(todos_generos))
    #criterio 4
    menor_idade = df['IDADE'].min()
    maior_idade = df['IDADE'].max()
    #criterio 5
    todos_municipios_residencia = df['MUNICIPIO DE RESIDENCIA'].astype(str) #força a conversão de todos os valores para strings
    municipios_residencia_unicos = sorted(set(todos_municipios_residencia))
    #criterio 6
    sintomas = df['SINTOMAS']
    todos_sintomas = ';'.join(sintomas).split(';')
    todos_sintomas_2 = ','.join(todos_sintomas).split(',')
    sintomas_unicos = sorted(set(todos_sintomas_2))
    #criterio 7 - data
    #criterio 8
    comorbidades = df['COMORBIDADES'].astype(str)
    todas_comorbidades = ';'.join(comorbidades).split(';')
    todas_comorbidades_2 = ','.join(todas_comorbidades).split(',')
    comorbidades_unicas = sorted(set(todas_comorbidades_2))
    #criterio 9
    vacinas = df['VACINA'].astype(str)
    numero_vacinas = sorted(set(vacinas))
    #criterio 10
    tipos_leitos = df['LEITO'].astype(str)
    tipos_leitos_unicos = sorted(set(tipos_leitos))
    #criterio 11
    tipos_evolucao = df['EVOLUCAO'].astype(str)
    evolucao_unica = sorted(set(tipos_evolucao))
    #criterio 12
    tipos_exames = df['EXAMES'].astype(str)
    tipos_exames_unicos = sorted(set(tipos_exames))
    
    #criterio 13 - data
    #criterio 14
    hipotese_diagnostica = df['HIPOTESE DIAGNOSTICA'].astype(str)
    todas_hipoteses_diagnosticas = ';'.join(hipotese_diagnostica).split(';')
    todas_hipoteses_diagnosticas_2 = ','.join(todas_hipoteses_diagnosticas).split(',')
    hipoteses_diagnosticas_unicas = sorted(set(todas_hipoteses_diagnosticas_2))
    #criterio 15
    tipos_notificacao = df['NOTIFICACAO DE DOENCA OU AGRAVO'].astype(str)
    notificacao_unica = sorted(set(tipos_notificacao))
    #criterio 16 - data
    #criterio 17
    finalizacoes_casos_limpos = []
    finalizacoes_casos = df['FINALIZACAO DO CASO']
    #criterio 18
    detalhe_finalizacao = df['DETALHE DA FINALIZAÇÃO'].astype(str)
    todos_detalhes = ';'.join(detalhe_finalizacao).split(';')
    detalhe_finalizacao_2 = ','.join(detalhe_finalizacao).split(',')
    detalhe_finalizacao_unico = sorted(set(detalhe_finalizacao_2))
    #crtiterio 19 - data

    for item in finalizacoes_casos: #logica para add a lista itens novos, fazer funcao em biblioteca e chamar aqui
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
                data_inicio, data_fim = bib.input_periodo()
                data_inicio, data_fim = datetime.datetime.combine(data_inicio, datetime.time.min), datetime.datetime.combine(data_fim, datetime.time.max)
                filtro_data_internacao = (df['INTERNAÇÃO'] >= data_inicio) & (df['INTERNAÇÃO'] <= data_fim)
                resultado_final = resultado_final[filtro_data_internacao]

            if criterio == 1:
                st.subheader('Semana Epidemiológica\n')
                semana_epidemiologica_comeco = st.number_input('Escolha o número da semana epidemiológica inicial', min_value=1, max_value=52, step=1)
                semana_epidemiologica_termino = st.number_input('Escolha o número da semana epidemiológica final',min_value=semana_epidemiologica_comeco, max_value=52, step=1)
                filtro_semana_epidemiologica = (df['SEMANA Nº'] >= semana_epidemiologica_comeco) & (df['SEMANA Nº'] <= semana_epidemiologica_termino)
                resultado_final = resultado_final[filtro_semana_epidemiologica]
            #corrigir
            if criterio == 2:
                st.subheader('Paciente\n')
                nome_paciente = st.selectbox('Filtrar por Nome do Paciente', pacientes_unicos)
                if nome_paciente:
                    resultado_final = resultado_final[resultado_final['PACIENTE'].str.contains(nome_paciente, case=False)]
                else:
                    resultado_final == resultado_final
                    
            if criterio == 3:
                st.subheader('Sexo\n')
                genero_paciente = st.selectbox(
                    'Qual o gênero declarado do/da paciente?',
                    generos_unicos
                )
                resultado_final = resultado_final[resultado_final['SEXO'] == genero_paciente]

            if criterio == 4:
                st.subheader('Idade\n')
                faixa_etaria = st.slider('Faixa etária', min_value=menor_idade, max_value=maior_idade, value=[menor_idade, maior_idade], step=1)
                filtro_faixa_etaria = (df['IDADE'] >= faixa_etaria[0]) & (df['IDADE'] <= faixa_etaria[1])
                resultado_final = resultado_final[filtro_faixa_etaria]

            if criterio == 5:
                st.subheader('Município de residência\n')
                opcao_municipio_residencia = st.multiselect('Qual o município de residência do paciente?', municipios_residencia_unicos)
                resultado_final = resultado_final[resultado_final['MUNICIPIO DE RESIDENCIA'].isin(opcao_municipio_residencia)]

            if criterio == 6:
                st.subheader('Sintomas\n')
                opcoes_sintomas = st.multiselect(
                    'Quais os sintomas do paciente?',
                    sintomas_unicos
                )
                if opcoes_sintomas:
                    filtro_sintomas = df['SINTOMAS'].str.contains('|'.join(opcoes_sintomas), case=False, na=False)
                    resultado_final = resultado_final[filtro_sintomas]

            if criterio == 7:
                st.subheader('Data dos sintomas\n')
                opcao_data_sintomas = bib.input_periodo()

                data_inicio_sintomas = datetime.datetime(opcao_data_sintomas[0].year, opcao_data_sintomas[0].month, opcao_data_sintomas[0].day)
                data_fim_sintomas = datetime.datetime(opcao_data_sintomas[1].year, opcao_data_sintomas[1].month, opcao_data_sintomas[1].day)

                df['DATA DOS SINTOMAS'] = pd.to_datetime(df['DATA DOS SINTOMAS'], format="%d.%m.%Y")

                filtro_data_sintomas = (df['DATA DOS SINTOMAS'] >= data_inicio_sintomas) & (df['DATA DOS SINTOMAS'] <= data_fim_sintomas)
                resultado_final = resultado_final[filtro_data_sintomas]
            
            if criterio == 8:
                st.subheader('Comorbidades\n')
                opcoes_comorbidades = st.multiselect(
                    'Informe as comorbidades',
                    comorbidades_unicas
                )
                if opcoes_comorbidades:
                    filtro_comorbidades = df['COMORBIDADES'].str.contains('|'.join(opcoes_comorbidades), case=False, na=False)
                    resultado_final = resultado_final[filtro_comorbidades]
                    
            if criterio == 9:
                st.subheader('Vacina\n')
                quantidade_vacinas = st.selectbox('Qual a quantidade de vacinas?', numero_vacinas)
                resultado_final= resultado_final[resultado_final['VACINA'] == quantidade_vacinas]
                
            if criterio == 10:
                st.subheader('Tipos de leitos\n')
                opcao_tipo_leito = st.selectbox(
                    'Qual o tipo de leito?',
                    tipos_leitos_unicos
                )
                resultado_final = resultado_final[resultado_final['LEITO'] == opcao_tipo_leito]
            #criterio 11 - evolucao do paciente
            if criterio == 11:
                st.subheader('Tipos de evolução\n')
                opcao_tipo_evolucao = st.selectbox(
                    'Qual o tipo de evolução',
                    evolucao_unica
                )
                resultado_final = resultado_final[resultado_final['EVOLUCAO'] == opcao_tipo_evolucao]
            #criterio 12 - exames
            if criterio == 12:
                st.subheader('Tipos de exames\n')
                opcao_tipo_exame = st.selectbox(
                    'Qual o tipo de exame',
                    tipos_exames_unicos
                )
                resultado_final = resultado_final[resultado_final['EXAMES'] == opcao_tipo_exame]
            # criterio 13 - data dos exames
            if criterio == 13:
                st.subheader('Data dos exames\n')
                data_exames = bib.input_periodo()

                data_inicio_exames = datetime.datetime(data_exames[0].year, data_exames[0].month, data_exames[0].day)
                data_fim_exames = datetime.datetime(data_exames[1].year, data_exames[1].month, data_exames[1].day)

                df['DATA DO EXAME'] = pd.to_datetime(df['DATA DO EXAME'], format="%d.%m.%Y")

                filtro_data_exames = (df['DATA DO EXAME'] >= data_inicio_exames) & (df['DATA DO EXAME'] <= data_fim_exames)
                resultado_final = resultado_final[filtro_data_exames]
            if criterio == 14:
                st.subheader('Hipótese diagnóstica\n')
                opcao_hipotese_diagnostica = st.multiselect(
                    'Informe a hipótese diagnóstica',
                    hipoteses_diagnosticas_unicas
                )
                filtro_hipotese_diagnostica = df['HIPOTESE DIAGNOSTICA'].str.contains('|'.join(opcao_hipotese_diagnostica), case=False, na=False)
                resultado_final = resultado_final[filtro_hipotese_diagnostica]
            #criterio 15 - notificacao de doenca ou agravo
            if criterio == 15:
                st.subheader('Notificação de doença ou agravo\n')
                opcao_tipo_notificacao = st.selectbox(
                    'Qual o tipo de notificação: ',
                    notificacao_unica
                )
                resultado_final = resultado_final[resultado_final['NOTIFICACAO DE DOENCA OU AGRAVO'] == opcao_tipo_notificacao] 
            #criterio 16 - data da notificacao do caso
            if criterio == 16:
                st.subheader('Data da notificação\n')
                data_notificacao = bib.input_periodo()

                data_inicio_notificacao = datetime.datetime(data_notificacao[0].year, data_notificacao[0].month, data_notificacao[0].day)
                data_fim_notificacao = datetime.datetime(data_notificacao[1].year, data_notificacao[1].month, data_notificacao[1].day)

                df['DATA DA NOTIFICAÇÃO'] = pd.to_datetime(df['DATA DA NOTIFICAÇÃO'], format="%d.%m.%Y")

                filtro_data_notificacao = (df['DATA DA NOTIFICAÇÃO'] >= data_inicio_notificacao) & (df['DATA DA NOTIFICAÇÃO'] <= data_fim_notificacao)
                resultado_final = resultado_final[filtro_data_notificacao]
            if criterio == 17:
                st.subheader('Finalização do caso\n')
                opcao_finalizacao_caso = st.selectbox(
                    'Informe a finalização do caso',
                    finalizacoes_casos_limpos_unicos
                )
                resultado_final = resultado_final[resultado_final['FINALIZACAO DO CASO'] == opcao_finalizacao_caso]
            #criterio 18 - detalhe da finalizacao(string)
            if criterio == 18:
                st.subheader('Detalhe da finalização do caso\n')
                opcao_detalhe = st.multiselect(
                    'Selecione o detalhe',
                    detalhe_finalizacao_unico
                )
                if opcao_detalhe:
                    filtro_detalhe = df['DETALHE DA FINALIZAÇÃO'].str.contains('|'.join(opcao_detalhe), case=False, na=False)
                    resultado_final = resultado_final[filtro_detalhe]
            #criterio 19 - data da finalizacao do caso
            if criterio == 19:
                st.subheader('Data da finalizacao do caso\n')
                data_finalizacao = bib.input_periodo()

                data_inicio_finalizacao = datetime.datetime(data_finalizacao[0].year, data_finalizacao[0].month, data_finalizacao[0].day)
                data_fim_finalizacao = datetime.datetime(data_finalizacao[1].year, data_finalizacao[1].month, data_finalizacao[1].day)

                df['DATA DA FINALIZACAO DO CASO'] = pd.to_datetime(df['DATA DA FINALIZACAO DO CASO'], format="%d.%m.%Y")

                filtro_data_finalizacao = (df['DATA DA FINALIZACAO DO CASO'] >= data_inicio_finalizacao) & (df['DATA DA FINALIZACAO DO CASO'] <= data_fim_finalizacao)
                resultado_final = resultado_final[filtro_data_finalizacao]
                
        st.divider()
        st.write("\nResultados da pesquisa:")
        st.write(resultado_final)
except:
    st.write('')
    
# GRÁFICOS COMEÇA AQUI
st.divider()
st.header('Gráficos: ', divider='red')
st.write('')
st.write('')

# Lista de tipos de gráficos Plotly
available_charts =[
    "Gráfico de Barras",
    "Gráfico de Linha",
    "Gráfico de Pizza",
    "Gráfico de Dispersão",
    "Gráfico de Radar",
    "Gráfico de Caixas",
    "Gráfico de Histograma",
    "Gráfico de Área",
    "Gráfico de Mapa de Calor",
    "Gráfico de Violino",
    "Gráfico de Rosca",
    "Gráfico de Área Empilhada",
    "Gráfico de Gráfico Polar",
]

#ordena a lista de tipos de gráficos
available_charts = sorted(available_charts, key=lambda x: unidecode(x))


# Sidebar para seleção de tipo de gráfico e colunas de dados
st.sidebar.subheader('Configuração de Gráfico')
chart_type = st.sidebar.selectbox("Selecione o tipo de gráfico:", available_charts)

# Verifica se a seleção de colunas é relevante para o tipo de gráfico selecionado
if chart_type in ["Gráfico de Barras", "Gráfico de Linha", "Gráfico de Dispersão", "Gráfico de Área"]:
    selected_columns = st.sidebar.multiselect("Selecione as colunas de dados:", resultado_final.columns)
# Verifica se a seleção de colunas é relevante para o tipo de gráfico de pizza
elif chart_type == "Gráfico de Pizza":
    selected_columns = [st.sidebar.multiselect("Selecione a coluna para rótulos:", resultado_final.columns)]
    if not selected_columns:
        st.sidebar.error("Selecione pelo menos uma coluna para rótulos.")
    elif len(selected_columns) == 1:
        st.sidebar.warning("Selecione uma segunda coluna para valores.")
    else:
        selected_columns.append(st.sidebar.selectbox("Selecione a coluna para valores:", resultado_final.columns))
    
# Outros tipos de gráficos não precisam de colunas selecionadas
else:
    selected_columns = []

# Função para criar o gráfico selecionado, recebendo parametros como o df, 
# tipo de grafico escolhido e colunas selecionadas da tabela já tratadas e filtradas
def create_chart(df, chart_type, selected_columns):
    try:
        if chart_type == "Gráfico de Barras":
            return px.bar(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Barras")
        elif chart_type == "Gráfico de Linha":
            return px.line(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Linha")
        elif chart_type == "Gráfico de Pizza":
            return px.pie(df, names=selected_columns[0], title="Gráfico de Pizza")
        elif chart_type == "Gráfico de Dispersão":
            return px.scatter(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Dispersão")
        elif chart_type == "Gráfico de Radar":
            return px.line_polar(df, r=selected_columns[0], theta=selected_columns[1], title="Gráfico de Radar")
        elif chart_type == "Gráfico de Caixas":
            return px.box(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Caixas")
        elif chart_type == "Gráfico de Histograma":
            return px.histogram(df, x=selected_columns[0], title="Gráfico de Histograma")
        elif chart_type == "Gráfico de Área":
            return px.area(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Área")
        elif chart_type == "Gráfico de Mapa de Calor":
            return px.density_heatmap(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Mapa de Calor")
        elif chart_type == "Gráfico de Violino":
            return px.violin(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Violino")
        elif chart_type == "Gráfico de Rosca":
            return px.pie(df, names=selected_columns[0], hole=0.3, title="Gráfico de Rosca")
        elif chart_type == "Gráfico de Área Empilhada":
            return px.area(df, x=selected_columns[0], y=selected_columns[1], title="Gráfico de Área Empilhada", facet_col=selected_columns[2])
        elif chart_type == "Gráfico de Gráfico Polar":
            return px.line_polar(df, r=selected_columns[0], theta=selected_columns[1], title="Gráfico Polar")
    except ValueError as e:
        st.error(f"Erro ao criar o gráfico: {e}")
    
# Botão para gerar o gráfico
if st.sidebar.button("Gerar Gráfico"):
    if not selected_columns:
        st.error("Selecione as colunas de dados relevantes para o tipo de gráfico.")
    elif len(selected_columns) != 2 and chart_type in ["Gráfico de Barras", "Gráfico de Linha", "Gráfico de Dispersão", "Gráfico de Área"]:
        st.error("Selecione exatamente duas colunas (X e Y) para este tipo de gráfico.")
    else:
        st.title("Gráfico Gerado: ")
        st.write(f"Visualizando os dados selecionados em um {chart_type}")
        chart = create_chart(resultado_final, chart_type, selected_columns)
        if chart is not None:
            st.plotly_chart(chart)

# Salvar o gráfico localmente
#fig.savefig("meu_grafico.png")
    