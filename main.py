import streamlit as st
import streamlit_authenticator as stauth
from st_pages import Page, show_pages, add_page_title, Section

st.set_page_config(layout="wide")

# Definindo as páginas
pages = [
    Page("main.py", "Bem Vindo", "🏠"),            
    Page("Pages/Incluir.py", "Incluir", "➕️"),
    Page("Pages/Consultar.py", "Consultar", "🔍️",),
    Page("Pages/Resumo.py", "Resumo", "📊️"),
]

show_pages([pages[0]])  # Mostrar apenas as páginas de Login e Pagina Inicial

# Definindo as credenciais
names = ['John Smith', 'Rebecca Briggs', 'Caio Cavalheiro', 'Nayara Cavalheiro']
usernames = ['jsmith', 'rbriggs', 'ccavalheiro', 'ncavalheiro']
passwords = ['123', '456', '110593', '210993']

# Gerar senhas criptografadas apenas uma vez
hashed_passwords = stauth.Hasher(passwords).generate()

# Autenticação do usuário
with st.sidebar:
    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                        'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
    name, authentication_status, username = authenticator.login('Usuario', 'main')

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
        
        # Mostrar páginas de acordo com a autenticação
        if username == 'jsmith':
            show_pages(pages)  # Mostrar todas as páginas
        elif username == 'rbriggs':
            show_pages([pages[0], pages[2]])  # Mostrar apenas as páginas de Login e Pagina Inicial
        elif username == 'ccavalheiro':
            show_pages([pages[0], pages[1], pages[2], pages[3]])  # Mostrar apenas as páginas de Login e Pagina Inicial
        elif username == 'ncavalheiro':
            st.error('Você não tem permissão para acessar esta página')
            show_pages([pages[0], pages[1], pages[2]])  # Mostrar apenas as páginas de Login e Pagina Inicial        
        else:
            st.error('Você não tem permissão para acessar esta página')
            show_pages([pages[0], pages[1]])  # Mostrar apenas as páginas de Login e Pagina Inicial

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

if authentication_status:
    st.title(f'Bem vindo ao Sistema de Controle de Estoque {my_session}')
else:
    st.title('Você não está logado, Clique em Bem Vindo para logar')
