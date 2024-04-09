import streamlit as st
import pandas as pd
import Controllers.EstoqueController as EstoqueController
import models.Estoque as estoque
from streamlit_card import card

st.set_page_config(layout="wide")

nome_usuario = st.session_state.get('NomeUsuario', '')

st.title('Resumo do Estoque')

db = EstoqueController.Data_base('system.db')
resultado_consulta = db.QuerySelectALL()
nomes_colunas = ['ID', 'DataHora', 'Usuário', 'Produto', 'Fornecedor', 'Modelo', 'Quantidade', 'Entrada_Saida', 'TipoSaida']
df = pd.DataFrame(resultado_consulta, columns=nomes_colunas)  # Convertendo os resultados em DataFrame

# Remover o índice da esquerda
df = df.set_index('ID')


#Subtrair o que é Entrada de Saída de cada produto
df['Quantidade'] = df.apply(lambda x: x['Quantidade'] if x['Entrada_Saida'] == 'Entrada' else -x['Quantidade'], axis=1)

#Agrupar por Produto, Fornecedor e Modelo
df = df.groupby(['Produto', 'Fornecedor', 'Modelo']).sum()

#Exibir somente Produto Forncedor Modelo e Quantidade
df = df[['Quantidade']]
df = df.reset_index()

#Estilo do card
styles = {
    "card": {
        "width": "95%",  # Reduced width to 95% to leave a small margin
        "height": "98%",  # Reduced height to 98% to leave a small margin
        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
        "margin": "2px 0",  # Reduced margin to reduce space between cards
        "font-size": "16px",  # Increase the font size here
    },
    "text": {
        "margin": "8px 0",  # Reduced margin to reduce space between cards
        "font-size": "24px",  # Decrease the font size here
    }
}

tab1, tab2 = st.tabs(["Gás", "Água"])

with tab1:
    Fornecedores_gas = ['Ultragaz', 'Liquigás', 'Nacional']
    Fornecedores_gas_colors = ['rgb(0,84,151)', 'rgb(0,111,78)', 'rgb(218,37,28)']
    models = ["P05", "P13", "P20", "P45"]

    for fornecedor, color in zip(Fornecedores_gas, Fornecedores_gas_colors):
        st.markdown(f"<h1 style='text-align: center; color: {color};'>{fornecedor}</h1>", unsafe_allow_html=True)
        columns = st.columns(len(models))
        for col, model in zip(columns, models):
            with col:
                quantity = int(df.loc[(df['Fornecedor'] == fornecedor) & (df['Modelo'] == model), 'Quantidade'].sum())
                hasClicked = card(
                    title=model,
                    text="QTD: " + str(quantity),
                    styles=styles,
                    key=f'{fornecedor}_{model}'  # chave única para cada widget card
                )

with tab2:
    #ULTRAGRAZ
    Fornecedores_gas = ['Bioleve', 'Cristal', 'Bonafonte']
    Fornecedores_gas_colors = ['rgb(0,84,151)', 'rgb(0,111,78)', 'rgb(218,37,28)']
    models = ["Galão"]

    for fornecedor, color in zip(Fornecedores_gas, Fornecedores_gas_colors):
        st.markdown(f"<h1 style='text-align: center; color: {color};'>{fornecedor}</h1>", unsafe_allow_html=True)
        columns = st.columns(len(models))
        for col, model in zip(columns, models):
            with col:
                quantity = int(df.loc[(df['Fornecedor'] == fornecedor) & (df['Modelo'] == model), 'Quantidade'].sum())
                hasClicked = card(
                    title=model,
                    text="QTD: " + str(quantity),
                    styles=styles,
                    key=f'{fornecedor}_{model}'  # chave única para cada widget card
                )
