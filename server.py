from xmlrpc.server import SimpleXMLRPCServer
import json
import datetime
import os


NOME_ARQUIVO_USERS = 'users.json'

dados_autenticacao = []
dados_documentos = []


def carregar_dados_usuarios():
    global dados_autenticacao
    with open(NOME_ARQUIVO_USERS, 'r') as arquivo:
        dados_autenticacao = json.load(arquivo)

def carregar_dados_documentos():
    global dados_documentos
    dados_documentos.clear()
    documentos = os.listdir('docs/')
    for documento in documentos:
        with open('docs/' + documento, 'r') as arquivo:
            dados_documentos.append(json.load(arquivo))

def autenticar_usuario(nome: str, senha: str) -> list:
    for registro in dados_autenticacao:
        if registro['nome'] == nome and registro['senha'] == senha:
            return [registro['id'], registro['nome']]
    return ['']

def pegar_usuarios():
    usuarios = []
    for registro in dados_autenticacao:
        usuarios.append([registro['id'], registro['nome']])
    return usuarios

def pegar_documentos_usuario(id_usuario: int) -> list:
    documentos = []
    for documento in dados_documentos:
        if id_usuario in documento['usuarios']:
            documentos.append(documento)
    return documentos

def verificar_documento_existente(nome_documento: str) -> bool:
    documentos = os.listdir('docs/')
    for documento in documentos:
        if documento == nome_documento + '.json':
            return True
    return False

def criar_documento(nome_documento: str, id_usuario: int) -> str:
    if not verificar_documento_existente(nome_documento):
        with open('docs/' + nome_documento + '.json', 'w') as arquivo:
            dados = {
                'titulo': nome_documento,
                'data': datetime.datetime.now().strftime('%d-%m-%Y %H'),
                'usuarios': [id_usuario],
                'notas': []
            }
            json.dump(dados, arquivo, indent=4)

            dados_documentos.append(dados)
            return 'Documento criado.'
    else:
        return 'O documento ja existe.'

def associar_usuario_documento(nome_documento: str, id_usuario: int) -> str:
    documentos = []
    for documento in dados_documentos:
        if documento['titulo'] == nome_documento:
            documento['usuarios'].append(id_usuario)
            with open('docs/' + nome_documento + '.json', 'w') as arquivo:
                json.dump(documento, arquivo, indent=4)
            return 'Usuario adicionado ao documento.'
    return 'Erro ao adicionar usuario ao documento.'

def pegar_documentos_data(data: datetime.datetime) -> list:
    documentos = []
    for documento in dados_documentos:
        data_documento = datetime.datetime.strptime(documento['data'], '%d-%m-%Y %H')
        if data_documento == data:
            documentos.append(documento)
    return documentos

def pegar_documento(nome_documento: str) -> dict:
    carregar_dados_documentos()
    documento = {}
    for doc in dados_documentos:
        if doc['titulo'] == nome_documento:
            documento = doc
    return documento

def adicionar_nota(nome_documento: str, titulo: str, conteudo: str) -> bool:
    documento = pegar_documento(nome_documento)
    if documento:
        nota = {
            'titulo': titulo,
            'conteudo': conteudo,
            'status_edicao': False
        }
        documento['notas'].append(nota)

        with open('docs/' + nome_documento + '.json', 'w') as arquivo:
            dados = {
                'titulo': nome_documento,
                'data': datetime.datetime.now().strftime('%d-%m-%Y %H'),
                'usuarios': documento['usuarios'],
                'notas': documento['notas']
            }
            json.dump(dados, arquivo, indent=4)

            return True
    
    return False

def verificar_status_edicao_nota(nome_documento: str, titulo_nota: str) -> bool:
    documento = pegar_documento(nome_documento)
    if documento:
        for nota in documento['notas']:
            if nota['titulo'] == titulo_nota:
                if nota['status_edicao']:
                    return True

        return False

def desbloquear_edicao(nome_documento: str, titulo_nota: str) -> bool:
    documento = pegar_documento(nome_documento)
    if documento:
        for nota in documento['notas']:
            if nota['titulo'] == titulo_nota:
                nota['status_edicao'] = False
                with open('docs/' + nome_documento + '.json', 'w') as arquivo:
                    dados = {
                        'titulo': nome_documento,
                        'data': datetime.datetime.now().strftime('%d-%m-%Y %H'),
                        'usuarios': documento['usuarios'],
                        'notas': documento['notas']
                    }
                    json.dump(dados, arquivo, indent=4)

                    return True

        return False

def bloquear_edicao(nome_documento: str, titulo_nota: str) -> bool:
    documento = pegar_documento(nome_documento)
    if documento:
        for nota in documento['notas']:
            if nota['titulo'] == titulo_nota:
                nota['status_edicao'] = True
                with open('docs/' + nome_documento + '.json', 'w') as arquivo:
                    dados = {
                        'titulo': nome_documento,
                        'data': datetime.datetime.now().strftime('%d-%m-%Y %H'),
                        'usuarios': documento['usuarios'],
                        'notas': documento['notas']
                    }
                    json.dump(dados, arquivo, indent=4)

                    return True

        return False

def alterar_nota(nome_documento: str, titulo_nota: str, titulo_alterado: str, conteudo_alterado: str) -> bool:
    documento = pegar_documento(nome_documento)
    if documento:
        for nota in documento['notas']:
            if nota['titulo'] == titulo_nota:
                if nota['titulo'] != titulo_alterado and titulo_alterado != '':
                    nota['titulo'] = titulo_alterado
                if nota['conteudo'] != conteudo_alterado and conteudo_alterado != '':
                    nota['conteudo'] = conteudo_alterado
                
                with open('docs/' + nome_documento + '.json', 'w') as arquivo:
                    dados = {
                        'titulo': nome_documento,
                        'data': datetime.datetime.now().strftime('%d-%m-%Y %H'),
                        'usuarios': documento['usuarios'],
                        'notas': documento['notas']
                    }
                    json.dump(dados, arquivo, indent=4)

                    return True

        return False


# Criando o server
server = SimpleXMLRPCServer(('192.168.1.35', 8000))
# Inicializaçao dados do server
carregar_dados_usuarios()
carregar_dados_documentos()

# Registrando as funções
server.register_function(autenticar_usuario, 'autenticar_usuario')
server.register_function(pegar_usuarios, 'pegar_usuarios')
server.register_function(criar_documento, 'criar_documento')
server.register_function(pegar_documentos_usuario, 'pegar_documentos_usuario')
server.register_function(associar_usuario_documento, 'associar_usuario_documento')
server.register_function(pegar_documentos_data, 'pegar_documentos_data')
server.register_function(pegar_documento, 'pegar_documento')
server.register_function(adicionar_nota, 'adicionar_nota')
server.register_function(desbloquear_edicao, 'desbloquear_edicao')
server.register_function(bloquear_edicao, 'bloquear_edicao')
server.register_function(verificar_status_edicao_nota, 'verificar_status_edicao_nota')
server.register_function(alterar_nota, 'alterar_nota')

print('Escutando na porta 8000...')
server.serve_forever()