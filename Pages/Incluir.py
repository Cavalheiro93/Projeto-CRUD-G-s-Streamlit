import streamlit as st
import pandas as pd
import Controllers.EstoqueController as EstoqueController
import models.Estoque as estoque

st.set_page_config(layout="centered")

username = st.session_state.get('NomeUsuario', '')
if username == '':
    # st.error('Você não está logado, Clique em Bem Vindo para logar')
    # st.stop()
    #ler o arquivo usuario_logado.txt
    with open('usuario_logado.txt', 'r') as f:
        username = f.read()


db = EstoqueController.Data_base('system.db')
dictCampos = {'DataHora': 'DATETIME', 
                'Usuário': 'TEXT', 
                'Produto': 'TEXT',
                'Fornecedor': 'TEXT',
                'Modelo': 'TEXT',
                'Quantidade': 'DOUBLE',
                'Entrada_Saida': 'TEXT',
                'TipoSaida': 'TEXT'
                }

db.CreateTable('FactEstoque', 'ID', dictCampos)

#teste Layout columns
col1, col2 = st.columns([5, 1])  

with col1:
    #mostrar st.selectbox com o usuario logado porém não deixar alterar
    st.title('Controle de Estoque')
    input_usuario = st.text_input('Usuário', value=username, disabled=True)
    input_data = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
    input_usuario = username
    input_produto = st.selectbox('Produto', options=['Gás', 'Água'])

    #Se for Agua, retorna as opções de fornecedores e modelos de Agua
    if input_produto == 'Água':
        input_fornecedor = st.selectbox('Fornecedor', options=['Bioleve', 'Cristal', 'Bonafont'])
        input_modelo = st.selectbox('Modelo', options=['Galão'])
    else:
        input_fornecedor = st.selectbox('Fornecedor', options=['Ultragaz', 'Liquigás', 'Nacional'])
        input_modelo = st.selectbox('Modelo', options=['P05', 'P13', 'P20', 'P45'])

    input_quantidade = st.number_input('Quantidade', 0)
    input_entrada_saida = st.selectbox('Entrada/Saída', options=['Entrada', 'Saída'])
    input_tipo_saida = st.selectbox('Tipo de Saída', options=['Revenda', 'Vale', 'Troca'])


    if st.button('Cadastrar'):
        RegistroEstoque = estoque.Estoque(
            id=0,  # Você pode manter o ID como 0, pois será ignorado ou substituído pelo banco de dados
            datahora=input_data,
            usuario=input_usuario,
            produto=input_produto,
            fornecedor=input_fornecedor,
            modelo=input_modelo,
            qtd=input_quantidade,
            tipo_envio=input_entrada_saida,
            tipo_saida=input_tipo_saida
        )

        # Extrair os atributos do objeto Estoque
        ListaRegistroEstoque = (
            RegistroEstoque.datahora, 
            RegistroEstoque.usuario, 
            RegistroEstoque.produto, 
            RegistroEstoque.fornecedor, 
            RegistroEstoque.modelo, 
            RegistroEstoque.qtd, 
            RegistroEstoque.tipo_envio, 
            RegistroEstoque.tipo_saida
                                )

        # Chamando a função RegisterValues da classe DB com os valores extraídos
        db.RegisterValues(ListaRegistroEstoque)
        st.success('Cadastrado com sucesso')


with col2:
    pass                