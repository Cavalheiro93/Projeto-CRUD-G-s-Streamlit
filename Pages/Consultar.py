import streamlit as st
import Controllers.EstoqueController as EstoqueController
import pandas as pd

username = st.session_state.get('NomeUsuario', '')
if username == '':
    # st.error('Você não está logado, Clique em Bem Vindo para logar')
    # st.stop()
    #ler o arquivo usuario_logado.txt
    with open('usuario_logado.txt', 'r') as f:
        username = f.read()

st.set_page_config(layout="wide")

st.write("Voce entrou com usuario", username)

db = EstoqueController.Data_base('system.db')
resultado_consulta = db.QuerySelectALL()

if resultado_consulta:  # Verifica se há resultados para evitar erros ao criar o DataFrame vazio
    st.title('Consultar Estoque')
    st.write('Aqui você pode consultar o estoque')

    # Definindo os nomes das colunas
    nomes_colunas = ['ID', 'DataHora', 'Usuário', 'Produto', 'Fornecedor', 'Modelo', 'Quantidade', 'Entrada_Saida', 'TipoSaida']

    df = pd.DataFrame(resultado_consulta, columns=nomes_colunas)  # Convertendo os resultados em DataFrame

    # Remover o índice da esquerda
    df = df.set_index('ID')

    # Ajustar a largura da tabela
    st.dataframe(df, width=1000)

else:
    st.write('Nenhum resultado encontrado.')