import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

# Configuração da página
st.set_page_config(page_title='Dashboard Hospital Municipal Prontovida',
                   layout='wide',
                   page_icon='prontovida_favicon.png')

def trocar_por_ponto_virgula(lista):
    for i in range(len(lista)):
        if ', ' in lista[i]:
            lista[i] = lista[i].replace(', ', ';').strip()
        if ',' in lista[i]:
            lista[i] = lista[i].replace(',', ';').strip()
    return lista

# Título principal
with st.container():
    col_a, col_b = st.columns(2)

    col_a.image('prontovida_logo_copia.png', use_column_width='auto')
    col_b.image('prefeitura_logo.png', width=250)
    col_b.image('uniesp_logo.png')

# Criação e organização do menu lateral
with st.sidebar:
    st.header('Critérios a serem utilizados')
    st.write('')

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
        st.checkbox('Notificação de doença ou agravo'),
        st.checkbox('Finalização do caso')
    ]

# Limpeza do cache, conexão com o Google Sheets e criação da planilha
st.cache_data.clear()
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Página1", usecols=[i for i in range(0, 20)])

# Definição dos filtros de pesquisa
todos_generos = df['SEXO'].astype(str)
generos_unicos = sorted(set(todos_generos))

menor_idade = int(df['IDADE'].min())
maior_idade = int(df['IDADE'].max())

todos_municipios_residencia = df['MUNICIPIO DE RESIDENCIA'].astype(str)
municipios_residencia_unicos = sorted(set(todos_municipios_residencia))

# Leitura dos sintomas e separação de elementos. O prenchimento é multivalorado e deve ser separado
sintomas = df['SINTOMAS'].astype(str)
sintomas = trocar_por_ponto_virgula(sintomas)
todos_sintomas = ';'.join(sintomas).split(';')
sintomas_unicos = sorted(set(todos_sintomas))

# Leitura e separação das comorbidades. Preenchimento multivalorado e deve ser separado
comorbidades = df['COMORBIDADES'].astype(str)
comorbidades = trocar_por_ponto_virgula(comorbidades)
todas_comorbidades = ';'.join(comorbidades).split(';')
comorbidades_unicas = sorted(set(todas_comorbidades))

tipos_leitos = df['LEITO'].astype(str)
tipos_leitos_unicos = sorted(set(tipos_leitos))

# Leitura e separação da hipótese diagnóstica. Preenchimento multivalorado e deve ser separado
hipotese_diagnostica = df['HIPOTESE DIAGNOSTICA'].astype(str)
hipotese_diagnostica = trocar_por_ponto_virgula(hipotese_diagnostica)
todas_hipoteses_diagnosticas = ';'.join(hipotese_diagnostica).split(';')
hipoteses_diagnosticas_unicas = sorted(set(todas_hipoteses_diagnosticas))

# Leitura das notificações de doenças ou agravos. O prenchimento é multivalorado e deve ser separado
notificacoes = df['NOTIFICACAO DE DOENCA OU AGRAVO'].astype(str)
notificacoes = trocar_por_ponto_virgula(notificacoes)
todas_notificacoes = ';'.join(notificacoes).split(';')
notificacoes_unicas = sorted(set(todas_notificacoes))

finalizacoes_casos_limpos = []
finalizacoes_casos = df['FINALIZACAO DO CASO'].astype(str)

for item in finalizacoes_casos:
    if isinstance(item, str):
        finalizacoes_casos_limpos.append(item)

finalizacoes_casos_limpos_unicos = sorted(set(finalizacoes_casos_limpos))

criterios_selecionados = []

for i in range(len(checkboxes)):
    if checkboxes[i]:
        criterios_selecionados.append(i)

# Critérios da planilha
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

        try:
            data_inicio, data_fim = periodo_internacao
            data_inicio = datetime.datetime.combine(data_inicio, datetime.time.min)
            data_fim = datetime.datetime.combine(data_fim, datetime.time.max)

            if periodo_internacao:
                filtro_data_internacao = ((pd.to_datetime(df['INTERNAÇÃO'], dayfirst=True)) >= data_inicio) & ((pd.to_datetime(df['INTERNAÇÃO'], dayfirst=True)) <= data_fim)
                resultado_final = resultado_final[filtro_data_internacao]
        except:
            st.write('Selecione a data de encerramento')

    if criterio == 1:
        st.subheader('Semana Epidemiológica\n')
        semana_epidemiologica_comeco = st.number_input('Escolha o número da semana epidemiológica inicial', min_value=1, max_value=52, step=1)
        semana_epidemiologica_termino = st.number_input('Escolha o número da semana epidemiológica final',min_value=semana_epidemiologica_comeco, max_value=52, step=1)
        filtro_semana_epidemiologica = (df['SEMANA Nº'].astype(float) >= semana_epidemiologica_comeco) & (df['SEMANA Nº'].astype(float) <= semana_epidemiologica_termino)
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
        filtro_faixa_etaria = (df['IDADE'].astype(float) >= faixa_etaria[0]) & (df['IDADE'].astype(float) <= faixa_etaria[1])
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

        try:
            data_inicio_sintomas = datetime.datetime(opcao_data_sintomas[0].year, opcao_data_sintomas[0].month, opcao_data_sintomas[0].day)
            data_fim_sintomas = datetime.datetime(opcao_data_sintomas[1].year, opcao_data_sintomas[1].month, opcao_data_sintomas[1].day)

            df['DATA DOS SINTOMAS'] = pd.to_datetime(df['DATA DOS SINTOMAS'], dayfirst=True)

            filtro_data_sintomas = (pd.to_datetime(df['DATA DOS SINTOMAS'], dayfirst=True) >= data_inicio_sintomas) & (pd.to_datetime(df['DATA DOS SINTOMAS'], dayfirst=True) <= data_fim_sintomas)
            resultado_final = resultado_final[filtro_data_sintomas]
        except:
            st.write('Selecione a data de encerramento')

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
        st.subheader('Notificação de doença ou agravo\n')
        opcao_notificacao = st.multiselect(
            'Informe a notificação de doença ou agravo do caso',
            notificacoes_unicas
        )
        if opcao_notificacao:
            filtro_notificacao = df['NOTIFICACAO DE DOENCA OU AGRAVO'].str.contains('|'.join(opcao_notificacao), case=False, na=False)
            resultado_final = resultado_final[filtro_notificacao]
    
    if criterio == 11:
        st.subheader('Finalização do caso\n')
        opcao_finalizacao_caso = st.selectbox(
            'Informe a finalização do caso',
            finalizacoes_casos_limpos_unicos
        )
        resultado_final = resultado_final[resultado_final['FINALIZACAO DO CASO'] == opcao_finalizacao_caso]

# Criação de abas para exibição da planilha e dos gráficos
aba1, aba2 = st.tabs(["Planilha", "Gráficos"])

# Filtragem de dados para gráficos e estatísticas
# Contagem de casos
total_casos = resultado_final['PACIENTE'].astype(str)
total_casos_numero = sorted(set(total_casos))

# Semana com mais pacientes
lista_coluna_semanas = resultado_final['SEMANA Nº'].astype(str).tolist()
contagem = {}

for i in lista_coluna_semanas:
    if i in contagem:
        contagem[i] += 1
    else:
        contagem[i] = 1

try:
    semana_mais_frequente = max(contagem, key=contagem.get)
    pacientes_semana_mais_frequente = contagem[semana_mais_frequente]
except:
    st.write('')

# Contagem de sexo
total_mulheres = len(resultado_final[resultado_final['SEXO'] == 'FEMININO'])
total_homens = len(resultado_final[resultado_final['SEXO'] == 'MASCULINO'])

# Contagem leito
total_enf_clinica = len(resultado_final[resultado_final['LEITO'] == 'ENF CLINICA'])
total_enf_onco = len(resultado_final[resultado_final['LEITO'] == 'ENF ONCO'])
total_uti_geral = len(resultado_final[resultado_final['LEITO'] == 'UTI GERAL'])
total_uti_cardio = len(resultado_final[resultado_final['LEITO'] == 'UTI CARDIO'])

# Contagem de finalizações dos casos
total_alta = len(resultado_final[resultado_final['FINALIZACAO DO CASO'] == 'ALTA'])
total_obito = len(resultado_final[resultado_final['FINALIZACAO DO CASO'] == 'ÓBITO'])
total_transferencia = len(resultado_final[resultado_final['FINALIZACAO DO CASO'] == 'TRANSFERENCIA'])

with aba1:
    col1, col2 = st.columns(2)

    try:
        # Display de dados na tela
        col1.subheader("Dados:")
        col1.markdown(f'''**Total de casos dentro do filtro selecionado:** {str(len(total_casos_numero))}  
                      **Semana com maior número de pacientes:** Semana nº {semana_mais_frequente}  
                      **Total de pacientes na semana nº {semana_mais_frequente}:** {pacientes_semana_mais_frequente}  
                      **Total de pacientes do sexo feminino:** {total_mulheres}  
                      **Total de pacientes do sexo masculino:** {total_homens}  
                      **Total de leitos Enfermaria Clínica:** {total_enf_clinica}  
                      **Total de leitos Enfermaria Onco:** {total_enf_onco}  
                      **Total de leitos UTI Geral:** {total_uti_geral}  
                      **Total de leitos UTI Cardio:** {total_uti_cardio}''')

        st.divider()

        # Display da planilha
        if len(criterios_selecionados) > 0:
            st.write('Resultados da pesquisa:')

        st.write(resultado_final)

        # Devs
        st.divider()

        st.subheader('Equipe de desenvolvedores:')

        st.markdown('''Andrezza Almeida  
                    Camila Cruz  
                    Leonardo Eggers  
                    Maísa Akiko Guimarães  
                    Victor Hugo Targino
                    ''')
    except:
        st.write('Dados indisponíveis. Verifique os filtros selecionados.')

with aba2:
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)

    try:
        # Display de dados na tela
        col1.subheader("Dados:")

        # if len(criterios_selecionados) == 0:
        #     col1.write('**Total de casos:** ' + str(len(total_casos_numero)))
        # elif len(criterios_selecionados) > 0:
        #     col1.write('**Total de casos dentro do filtro selecionado:** ' + str(len(total_casos_numero)))
        
        col1.markdown(f'''**Total de casos dentro do filtro selecionado:** {str(len(total_casos_numero))}  
                      **Semana com maior número de pacientes:** Semana nº {semana_mais_frequente}  
                      **Total de pacientes na semana nº {semana_mais_frequente}:** {pacientes_semana_mais_frequente}  
                      **Total de pacientes do sexo feminino:** {total_mulheres}  
                      **Total de pacientes do sexo masculino:** {total_homens}  
                      **Total de leitos Enfermaria Clínica:** {total_enf_clinica}  
                      **Total de leitos Enfermaria Onco:** {total_enf_onco}  
                      **Total de leitos UTI Geral:** {total_uti_geral}  
                      **Total de leitos UTI Cardio:** {total_uti_cardio}''')

        # ---------------------------------------------------------------------------------------------------------------
        # Agrupar os dados por Sexo e Finalizacao
        grouped_data = resultado_final.groupby(['SEXO', 'FINALIZACAO DO CASO']).size().reset_index(name='QUANTIDADE')

        # Criar gráfico de barras empilhadas interativo com Plotly Express
        fig1 = px.bar(grouped_data, x='SEXO', y='QUANTIDADE', color='FINALIZACAO DO CASO',
                    title='Distribuição de Finalizações por Sexo',
                    labels={'QUANTIDADE': 'Quantidade de Casos', 'SEXO': 'Sexo', 'FINALIZACAO DO CASO': 'Finalização'},
                    barmode='group')

        # Adicionar rótulo ao eixo y
        fig1.update_yaxes(title_text='Quantidade de Casos')

        fig1.update_layout(paper_bgcolor="#DBF3FA")

        col3.divider()
        col4.divider()

        # Exibir o gráfico no Streamlit
        col3.plotly_chart(fig1, use_container_width=True)

        # ---------------------------------------------------------------------------------------------------------------
        # CORRIGIR

        # quantidades_feminino_alta = grouped_data['QUANTIDADE'][0]
        # quantidades_feminino_transferencia = grouped_data['QUANTIDADE'][1]
        # quantidades_feminino_obito = grouped_data['QUANTIDADE'][2]
        # quantidades_masculino_alta = grouped_data['QUANTIDADE'][3]
        # quantidades_masculino_transferencia = grouped_data['QUANTIDADE'][4]
        # quantidades_masculino_obito = grouped_data['QUANTIDADE'][5]

        # col4.subheader('Dados:')
        # col4.markdown(f'''**Total de altas - SEXO FEMININO:** {quantidades_feminino_alta}  
        #         **Total de transferências - SEXO FEMININO:** {quantidades_feminino_transferencia}  
        #         **Total de óbitos - SEXO FEMININO:** {quantidades_feminino_obito}  
        #         -  
        #         **Total de altas - SEXO MASCULINO:** {quantidades_masculino_alta}  
        #         **Total de transferências - SEXO MASCULINO:** {quantidades_masculino_transferencia}  
        #         **Total de óbitos - SEXO MASCULINO:** {quantidades_masculino_obito}''')

        # ---------------------------------------------------------------------------------------------------------------
        # Definir as faixas etárias
        faixas_etarias = [0, 19, 29, 39, 49, 59, 69, 79, 150]
        labels_faixas_etarias = ['até 19 anos', '20 a 29 anos', '30 a 39 anos', '40 a 49 anos', '50 a 59 anos', '60 a 69 anos', '70 a 79 anos', 'mais de 80 anos']

        # Criar uma nova coluna 'Faixa Etária' no DataFrame
        resultado_final['Faixa Etária'] = pd.cut(resultado_final['IDADE'], bins=faixas_etarias, labels=labels_faixas_etarias, right=False)

        # Agrupar os dados por Faixa Etária e contar a quantidade de casos
        grouped_data = resultado_final.groupby('Faixa Etária').size().reset_index(name='Quantidade')

        fig2 = px.bar(grouped_data, x='Faixa Etária', y='Quantidade',
                    title='Distribuição de Casos por Faixa Etária',
                    labels={'Quantidade': 'Quantidade de Casos', 'Faixa Etária': 'Faixa Etária'},
                    color='Faixa Etária')

        # Adicionar rótulo ao eixo y
        fig2.update_yaxes(title_text='Quantidade de Casos')

        fig2.update_layout(paper_bgcolor="#DBF3FA")

        col4.plotly_chart(fig2, use_container_width=True)

        # ---------------------------------------------------------------------------------------------------------------
        # Contar a ocorrência de cada tipo de leito
        count_leitos = resultado_final['LEITO'].value_counts().reset_index(name='Quantidade')

        fig3 = px.pie(count_leitos, names='index', values='Quantidade',
                    title='Distribuição de Tipos de Leito',
                    labels={'index': 'Tipo de Leito', 'Quantidade': 'Quantidade'})

        fig3.update_layout(paper_bgcolor="#DBF3FA")

        col5.plotly_chart(fig3, use_container_width=True)

        # ---------------------------------------------------------------------------------------------------------------
        # Contar a ocorrência de cada semana
        count_semana = resultado_final['SEMANA Nº'].value_counts().reset_index(name='Quantidade')

        fig4 = px.pie(count_semana, names='index', values='Quantidade',
                    title='Distribuição de pacientes por Semana Epidemiológica',
                    labels={'index': 'Semana', 'Quantidade': 'Quantidade'})

        fig4.update_layout(paper_bgcolor="#DBF3FA")

        col6.plotly_chart(fig4, use_container_width=True)

        # Devs
        st.divider()

        st.subheader('Equipe de desenvolvedores:')

        st.markdown('''Andrezza Almeida  
                    Camila Cruz  
                    Leonardo Eggers  
                    Maísa Akiko Guimarães  
                    Victor Hugo Targino
                    ''')
    except:
        st.write('Dados indisponíveis. Verifique os filtros selecionados.')
