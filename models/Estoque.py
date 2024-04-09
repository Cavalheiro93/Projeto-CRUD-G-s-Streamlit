class Estoque:
    def __init__(self, id, datahora, usuario, produto, fornecedor, modelo, qtd, tipo_envio, tipo_saida):
        self.id = id
        self.datahora = datahora    
        self.usuario = usuario
        self.produto = produto
        self.fornecedor = fornecedor
        self.modelo = modelo
        self.qtd = qtd
        self.tipo_envio = tipo_envio
        self.tipo_saida = tipo_saida