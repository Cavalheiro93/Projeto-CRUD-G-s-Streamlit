from typing import List
import services.database as database;
import models.Estoque as Estoque
import numpy as np
import sqlite3

class Data_base:
    # Construtor da classe
    def __init__(self, name='system.db'):
        self.name = name


    def start_connection(self):
        """ Inicia a conexão com o banco de dados SQLite3 """
        self.connection = sqlite3.connect(self.name)


    def close_connection(self):
        """ Fecha a conexão com o banco de dados SQLite3 """
        try:
            self.connection.close()
        except:
            pass


    def CreateTable(self, TableName, PrimaryKeyField, TableFields):
        """
        Cria uma nova tabela no banco de dados SQLite3.

            Parâmetros:
            - TableName (str): O nome da tabela a ser criada.
            - PrimaryKeyField (str): O nome do campo que será definido como chave primária da tabela.            
            - TableFields (dict): Um dicionário onde as chaves são os nomes dos campos e os valores são os tipos de dados correspondentes.

            Exemplo de uso:

            - NomeTabela = 'FactEstoque'
            - CampoPrimaryKey = 'ID'            
            - CamposTabela = {DataHora: 'DATETIME', 
                              Usuário: 'TEXT', 
                              Produto: 'TEXT', 
                              Fornecedor: 'TEXT',
                              Modelo: 'TEXT',
                              Quantidade: 'DOUBLE',
                              Entrada_Saida: 'TEXT',
                              TipoSaida: 'TEXT'} 
            - db.CreateTable(NomeTabela, CamposTabela, CampoPrimaryKey)
        """
        #A. Inicializando a conexão
        self.start_connection()
        #B. Criando um cursor para executar comandos SQL
        cursor = self.connection.cursor()

        #C. Construindo a string de criação de tabela dinamicamente
        #C1. Inicializa a string com o comando SQL       
        #C2. Adiciona o campo de chave primária
        #C3. Adiciona os demais campos da tabela
        #C4. Remove a última vírgula e fecha a instrução SQL
        #C5. Adiciona o ponto e vírgula no final da instrução SQL         
        create_table_query = f"CREATE TABLE IF NOT EXISTS {TableName} ("                    #C1
        create_table_query += f"{PrimaryKeyField} INTEGER PRIMARY KEY AUTOINCREMENT, "      #C2
        for field, field_type in TableFields.items():                                       #C3
            create_table_query += f"{field} {field_type}, "
        create_table_query = create_table_query.rstrip(", ")                                #C4
        create_table_query += ");"                                                          #C5                       
        
        #D. Executando a instrução SQL
        cursor.execute(create_table_query)
        #E. Commitando a transação
        self.close_connection()
    

    def RegisterValues(self, fullDataSet):
        """ Registra uma nova empresa no banco de dados SQLite3.
                
                Parâmetros:
                - fullDataSet (list): Uma lista contendo os valores que deverão ser adicionados na tabela. Não é necessario passar o ID, pois ele é autoincrementado.

                Exemplo de uso:

                - fullDataSet = ['2022-10-10 10:10:10', 
                                    'Caio', 
                                    'Nacional', 
                                    'P40', 
                                    10,
                                    'Saida',
                                    'Revenda']
                - db.register_company(fullDataSet)
            
        """
        #A. Inicializando a conexão
        self.start_connection()
        #B. Construindo a string de inserção de dados dinamicamente
        campos_tabela = ('DataHora', 'Usuário', 'Produto', 'Fornecedor', 'Modelo', 'Quantidade', 'Entrada_Saida', 'TipoSaida')
        #C. Definindo as interrogacoes para a quantidade de campos
        qntd = ("?,?,?,?,?,?,?,?")        

        #D. Criando um cursor para executar comandos SQL
        cursor = self.connection.cursor()
        #E. Executando a instrução SQL para inserir os dados na tabela
        cursor.execute(f"""INSERT INTO FactEstoque {campos_tabela} VALUES({qntd})""", fullDataSet)
        #F. Commitando a transação
        self.connection.commit()


    def QuerySelectALL(self):
        try:
        #A. Inicializando a conexão
            self.start_connection()
            #B. Criando um cursor para executar comandos SQL
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM FactEstoque")
            return cursor.fetchall()
        except:
            pass