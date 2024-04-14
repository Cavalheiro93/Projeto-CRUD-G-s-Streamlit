import streamlit as st
import pandas as pd
import Controllers.EstoqueController as EstoqueController
import models.Estoque as estoque

username = st.session_state.get('NomeUsuario', '')
if username == '':
    with open('usuario_logado.txt', 'r') as f:
        username = f.read()
st.set_page_config(layout="centered")

st.write("Voce entrou com usuario", username)
st.title('Alterar e Excluir')

if "upda" not in st.session_state:
    st.session_state.upda = False



update_id = st.number_input(label='Insira o Id', format='%d', step=1)
button_update_select = st.button('Consultar')

if button_update_select:
    st.session_state.upda = True

if st.session_state.upda == True:
    item = EstoqueController.Data_base('system.db').SelectID(update_id)

    if item:  # Check if item is not empty
        input_usuario = st.text_input('Usuário', value=item[2], disabled=True)
        input_data = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
        input_produto = st.selectbox('Produto', options=['Gás', 'Água'],
                                    index=0 if item[3] == 'Gás' else 1)

        #Se for Agua, retorna as opções de fornecedores e modelos de Agua
        if input_produto == 'Água':
            input_fornecedor = st.selectbox('Fornecedor', 
                                            options=['Bioleve', 'Cristal', 'Bonafont'],
                                            index=['Bioleve', 'Cristal', 'Bonafont'].index(item[4]))
            input_modelo = st.selectbox('Modelo', 
                                        options=['Galão'],
                                        index=0)
        else:
            input_fornecedor = st.selectbox('Fornecedor', 
                                            options=['Ultragaz', 'Liquigás', 'Nacional'],
                                            index=['Ultragaz', 'Liquigás', 'Nacional'].index(item[4]))
            input_modelo = st.selectbox('Modelo', 
                                        options=['P05', 'P13', 'P20', 'P45'],
                                        index=['P05', 'P13', 'P20', 'P45'].index(item[5]))

        input_quantidade = st.number_input('Quantidade', value=item[6])
        input_entrada_saida = st.selectbox('Entrada/Saída', 
                                        options=['Entrada', 'Saída'],
                                        index=0 if item[7] == 'Entrada' else 1)
        input_tipo_saida = st.selectbox('Tipo de Saída', 
                                        options=['Revenda', 'Vale', 'Troca'],
                                        index=['Revenda', 'Vale', 'Troca'].index(item[8]))
    
        col1, col2, col3 = st.columns([2, 2, 3]) 
        with col1:
            if st.button('Alterar'):

                #onde colocar o fullDataSet ?
                fullDataSet = (input_data, input_usuario, input_produto, input_fornecedor, input_modelo, input_quantidade, input_entrada_saida, input_tipo_saida, item[0])             
                EstoqueController.Data_base('system.db').UpdateValues(fullDataSet)
                st.success('Alterado com sucesso!!!')
                st.session_state.upda = False
        with col2:
            if st.button('Excluir'):
                EstoqueController.Data_base('system.db').DeleteValues(update_id)
                st.warning('Excluído com sucesso!!!')
                st.session_state.upda = False
        with col3:
            pass
    else:
        st.write('No item found with the provided ID.')


