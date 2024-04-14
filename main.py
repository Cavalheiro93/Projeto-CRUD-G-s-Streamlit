import streamlit as st
import streamlit_authenticator as stauth
from st_pages import Page, show_pages
import pandas as pd

# Leitura do arquivo de usuários e geração de senhas criptografadas apenas uma vez
@st.cache_data()
def load_user_data():
    df_users = pd.read_csv('myusers.csv', sep=';')
    names = df_users['name'].tolist()
    usernames = df_users['username'].tolist()
    passwords = df_users['password'].astype(str).tolist()
    kind_access = df_users['kind of access'].tolist()
    hashed_passwords = stauth.Hasher(passwords).generate()
    return names, usernames, hashed_passwords, kind_access

names, usernames, hashed_passwords, kind_access = load_user_data()

# Função para criar e armazenar as páginas em cache
@st.cache_data()
def create_pages():
    return [
        Page("main.py", "Bem Vindo", "🏠"),            
        Page("Pages/Incluir.py", "Incluir", "➕️"),
        Page("Pages/Consultar.py", "Consultar", "🔍️",),
        Page("Pages/Resumo.py", "Resumo", "📊️"),
        Page("Pages/AlterarExcluir.py", "Alterar e Excluir", "🔄️"),
    ]

# Função para carregar e exibir as páginas, sem cache
def authenticate_and_display_pages():
    pages = create_pages()
    show_pages([pages[0]])

    with st.sidebar:
        authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                            'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
        name, authentication_status, username = authenticator.login('Usuario', 'main')
        
        if authentication_status:
            authenticator.logout('Logout', 'main')

            st.session_state["NomeUsuario"] = name
            my_session = st.session_state["NomeUsuario"]

            st.write(f'Você está logado como {my_session}')

            user_access = dict(zip(usernames, kind_access))
            user_access = user_access.get(username)

            st.session_state["AcessoUsuario"] = user_access

            #gerar um arquivo txt com o nome do usuario logado
            with open('usuario_logado.txt', 'w') as f:
                f.write(name + '\n')
                f.write(user_access)

            if user_access == 'admin':
                show_pages(pages)
            elif user_access == 'regular':
                show_pages([pages[0], pages[1]])
            else:
                st.error('Você não tem permissão para acessar esta página')
                show_pages([pages[0], pages[1]])

        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.warning('Please enter your username and password')

    if authentication_status:
        st.title(f'Bem vindo ao Sistema de Controle de Estoque {my_session} - MAIN')
    else:
        st.title('Essa Tela que está carregando MAIN')

authenticate_and_display_pages()
