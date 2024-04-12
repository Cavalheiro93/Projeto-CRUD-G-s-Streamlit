import streamlit as st
import pandas as pd
import Controllers.EstoqueController as EstoqueController
import models.Estoque as estoque

username = st.session_state.get('NomeUsuario', '')
if username == '':
    # st.error('Você não está logado, Clique em Bem Vindo para logar')
    # st.stop()
    #ler o arquivo usuario_logado.txt
    with open('usuario_logado.txt', 'r') as f:
        username = f.read()

st.set_page_config(layout="wide")

st.write("Voce entrou com usuario", username)
st.title('Alterar e Excluir')

db = EstoqueController.Data_base('system.db')

# Definindo os nomes das colunas
#nomes_colunas = ['ID', 'DataHora', 'Usuário', 'Produto', 'Fornecedor', 'Modelo', 'Quantidade', 'Entrada_Saida', 'TipoSaida']

largura_colunas = st.columns((1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

# for col, campo_nome in zip(largura_colunas, nomes_colunas):
#     col.write(campo_nome)


for item in db.QueryChangeDelete():
   # Adicionar uma linha em branco entre cada registro  
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = largura_colunas
    col1.write(item.id)
    col2.write(item.datahora)
    col3.write(item.usuario)
    col4.write(item.produto)
    col5.write(item.fornecedor)
    col6.write(item.modelo)
    col7.write(item.qtd)
    col8.write(item.tipo_envio)
    col9.write(item.tipo_saida)


    on_click_excluir = col10.button('Excluir', 'btnExcluir' + str(item.id))
    on_click_alterar = col11.button('Alterar', 'btnAlterar' + str(item.id))

    if on_click_excluir:
        #db.Excluir(item.id)
        st.write(f'Item excluído com sucesso! {item.id}')
        #
        st.experimental_rerun()

    if on_click_alterar:
        #st.experimental_set_query_params(id=[item.id])
        st.experimental_rerun()

    # Add a line break for spacing
    st.write("")