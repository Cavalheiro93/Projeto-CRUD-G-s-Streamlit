import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import Controllers.EstoqueController as EstoqueController
import models.Estoque as estoque
import Pages.Consultar as Consultar

col1, col2, col3 = st.columns(3)

with col1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.title('Controle de Estoque')

    input_data = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    input_usuario = st.text_input('Usuário')
    input_fornecedor = st.text_input('Fornecedor')
    input_modelo = st.text_input('Modelo')
    input_quantidade = st.number_input('Quantidade', 0)
    input_entrada_saida = st.selectbox('Entrada/Saída', options=['Entrada', 'Saída'])
    input_tipo_saida = st.selectbox('Tipo de Saída', options=['Revenda', 'Vale', 'Troca'])

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")