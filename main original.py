import streamlit as st
import streamlit_authenticator as stauth
from st_pages import Page, show_pages, add_page_title, Section

# Definindo as páginas
pages = [
    Page("main.py", "Login", "🔐"),            
    Page("Pages/Home.py", "Pagina Inicial", "🏠"),
    Page("Pages/Incluir.py", "Incluir", "➕️"),
    Page("Pages/Consultar.py", "Consultar", "🔍️")
]

# Definindo as credenciais
names = ['John Smith', 'Rebecca Briggs', 'Caio Cavalheiro', 'Nayara Cavalheiro']
usernames = ['jsmith', 'rbriggs', 'ccavalheiro', 'ncavalheiro']
passwords = ['123', '456', '110593', '210993']

show_pages([pages[0]])  # Mostrar apenas as páginas de Login e Pagina Inicial

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

# Autenticação do usuário
name, authentication_status, username = authenticator.login('Usuario', 'main')
if authentication_status:
    # Botão de logout
    authenticator.logout('Logout', 'main')  # Realizar logout
    st.title(f'Bem Vindo(a) {name}')
    
    # Mostrar páginas de acordo com a autenticação
    if username == 'jsmith':  # Exemplo de condição, você pode ajustar conforme necessário
        show_pages(pages)  # Mostrar todas as páginas
    elif username == 'rbriggs':
        show_pages([pages[0], pages[2]])  # Mostrar apenas as páginas de Login e Pagina Inicial
    elif username == 'ccavalheiro':
        show_pages([pages[0], pages[1]])  # Mostrar apenas as páginas de Login e Pagina Inicial
    elif username == 'ncavalheiro':
        st.error('Você não tem permissão para acessar esta página')
        show_pages([pages[0], pages[1]])  # Mostrar apenas as páginas de Login e Pagina Inicial        
    # Adicione mais condições conforme necessário
    else:
        st.error('Você não tem permissão para acessar esta página')
        show_pages([pages[0], pages[1]])  # Mostrar apenas as páginas de Login e Pagina Inicial

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
