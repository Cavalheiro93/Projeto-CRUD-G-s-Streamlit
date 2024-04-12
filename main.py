import streamlit as st
import streamlit_authenticator as stauth
from st_pages import Page, show_pages, add_page_title, Section
import pandas as pd

# Define function to authenticate user
def authenticate_user(names, usernames, hashed_passwords, kind_access):
    with st.sidebar:
        authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                            'some_cookie_name', 'some_signature_key', cookie_expiry_days=0)
        name, authentication_status, username = authenticator.login('Usuario', 'main')
        return name, authentication_status, username

# Define function to display pages based on user access
def display_pages(pages, authentication_status, username, name):
    if authentication_status:
        # Botão de logout
        authenticator.logout('Logout', 'main')  # Realizar logout

        #colocar no session.state o nome do usuario logado
        st.session_state["NomeUsuario"] = name
        my_session = st.session_state["NomeUsuario"]

        st.write(f'Você está logado como {my_session}')

        #gerar um arquivo txt com o nome do usuario logado
        with open('usuario_logado.txt', 'w') as f:
            f.write(name)
        
        #combine o usuario autenticado com o tipo de acesso e entao as paginas serao mostradas de acordo com o tipo de acesso
        user_access = dict(zip(usernames, kind_access))                         #gerando um dicionario com os usuarios e seus respectivos acessos
        user_access = {k: v for k, v in user_access.items() if k == username}   #filtrando o dicionario para pegar apenas o usuario autenticado
        user_access = list(user_access.values())[0]                             #pegando o valor do tipo de acesso do usuario autenticado

        if user_access == 'admin':
            show_pages(pages)
        elif user_access == 'regular':
            show_pages([pages[0], pages[1]])
        else:
            st.error('Você não tem permissão para acessar esta página')
            show_pages([pages[0], pages[1]])  # Mostrar apenas as páginas de Login e Pagina Inicial

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

# Main function
def main():
    # Definindo as páginas
    pages = [
        Page("main.py", "Bem Vindo", "🏠"),            
        Page("Pages/Incluir.py", "Incluir", "➕️"),
        Page("Pages/Consultar.py", "Consultar", "🔍️",),
        Page("Pages/Resumo.py", "Resumo", "📊️"),
        Page("Pages/AlterarExcluir.py", "Alterar e Excluir", "🔄️"),
    ]

    show_pages([pages[0]])  # Mostrar apenas as páginas de Login e Pagina Inicial

    # Definindo as credenciais
    df_users = pd.read_csv('myusers.csv', sep=';')
    names = df_users['name'].tolist()
    usernames = df_users['username'].tolist()
    passwords = df_users['password'].astype(str).tolist()
    kind_access = df_users['kind of access'].tolist()

    # Gerar senhas criptografadas apenas uma vez
    hashed_passwords = stauth.Hasher(passwords).generate()
    
    # Authenticate user
    name, authentication_status, username = authenticate_user(names, usernames, hashed_passwords, kind_access)

    # Display pages based on authentication
    display_pages(pages, authentication_status, username, name)

if __name__ == "__main__":
    main()
