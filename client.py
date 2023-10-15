import xmlrpc.client
import datetime
from os import system
from time import sleep


dados_sessao = []

def limpar_terminal():
    system('cls')

def esperar_segundos(segundos: int):
    sleep(segundos)

def esperar_enter():
    print('\nPressione enter...')
    input()

def menu():
    limpar_terminal()
    print('Menu')
    print(' 1 - Listar usuários existentes')
    print(' 2 - Criar documento')
    print(' 3 - Associar usuário ao documento')
    print(' 4 - Listar documentos')
    print(' 5 - Listar documentos por data de alteraçao')
    print(' 6 - Detalhes de um documento')
    print(' 7 - Criar uma nota em um documento')
    print(' 8 - Editar uma nota em um documento')
    print(' 9 - Listar o conteudo de uma nota')
    print(' 10 - Listar notas de um documento')
    print(' 0 - Sair')

    return int(input('Opção: '))

def autenticar_usuario():
    global dados_sessao
    while True:
        limpar_terminal()
        nome = input('Usuario: ')
        senha = input('Senha: ')

        dados_sessao = proxy.autenticar_usuario(nome, senha)
        if len(dados_sessao) > 1:
            break
        else:
            print('Credenciais invalidas.')
            esperar_segundos(2)


with xmlrpc.client.ServerProxy('http://192.168.1.35:8000/', allow_none=True) as proxy:
    autenticar_usuario()

    while True:
        opcao = menu()
        if opcao == 1:
            limpar_terminal()
            print('Usuarios Cadastrados')
            usuarios = proxy.pegar_usuarios()
            for usuario in usuarios:
                print(' ' + str(usuario[0]) + ' - ' + usuario[1])

            esperar_enter()
        elif opcao == 2:
            limpar_terminal()
            print('Criar Documento')
            nome_documento = input(' Nome do documento: ')
            resposta = proxy.criar_documento(nome_documento, int(dados_sessao[0]))
            print(resposta)

            esperar_segundos(2)
        elif opcao == 3:
            limpar_terminal()
            print('Associar Usuario ao Documento')
            print(' Usuarios:')
            usuarios = proxy.pegar_usuarios()
            for usuario in usuarios:
                print('  ', usuario[0], ' - ' + usuario[1])
            id_usuario = int(input(' ID do usuario: '))
            print(' Documentos:')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print('  ' + documento['titulo'])
                nome_documento = input(' Nome do documento: ')
                resposta = proxy.associar_usuario_documento(nome_documento, id_usuario)
                print(resposta)
            else:
                print('  Sem documentos.')
            
            esperar_enter()
        elif opcao == 4:
            limpar_terminal()
            print('Documentos')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print(' ' + documento['titulo'])
            else:
                print(' Sem documentos.')

            esperar_enter()
        elif opcao == 5:
            limpar_terminal()
            print('Documentos por Data de Alteraçao')
            date = datetime.datetime.strptime(input(' Data e hora (Ex. DD-MM-AAAA H):'), '%d-%m-%Y %H')
            documentos = proxy.pegar_documentos_data(date)
            if documentos:
                for documento in documentos:
                    print(' ' + documento['titulo'])
            else:
                print(' Sem documentos.')

            esperar_enter()
        elif opcao == 6:
            limpar_terminal()
            print('Detalhes do Documento')
            print(' Documentos:')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print('  - ' + documento['titulo'])
                nome_documento = input(' Nome do documento: ')
                resposta = proxy.pegar_documento(nome_documento)
                if resposta != {}:
                    print('\n Titulo: ', resposta['titulo'])
                    print(' Data da ultima alteraçao: ', resposta['data'])
                    print(' Usuarios com acesso a nota: ')
                    usuarios = proxy.pegar_usuarios()
                    for usuario_documento in resposta['usuarios']:
                        for usuario in usuarios:
                            if usuario[0] == usuario_documento:
                                print('  - ' + usuario[1])
                    print(' Notas: ')
                    if resposta['notas'] != []:
                        contador = 0
                        for nota in resposta['notas']:
                            contador += 1
                            print(' - Nota: ', contador)
                            print('    | Titulo da nota: ', nota['titulo'])
                            print('    | Sendo editada: ', 'Sim' if nota['status_edicao'] else 'Não')
                    else:
                        print('  Nao ha notas no documento.')
                else:
                    print('Nome do documento incorreto.')
            else:
                print('  Sem documentos.')

            esperar_enter()
        elif opcao == 7:
            limpar_terminal()
            print('Criar uma Nota no Documento')
            print(' Documentos:')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print('  - ' + documento['titulo'])
                nome_documento = input(' Nome do documento: ')
                resposta = proxy.pegar_documento(nome_documento)
                if resposta != {}:
                    titulo = input(' - Titulo: ')
                    conteudo = input(' - Conteudo:')
                    resposta = proxy.adicionar_nota(nome_documento, titulo, conteudo)
                    if resposta:
                        print(' \nNota criada com sucesso!')
                    else:
                        print(' \nErro ao criar nota')
            
            esperar_enter()
        elif opcao == 8:
            limpar_terminal()
            print('Alterar uma Nota no Documento')
            print(' Documentos:')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print('  - ' + documento['titulo'])
                nome_documento = input(' Nome do documento: ')
                resposta = proxy.pegar_documento(nome_documento)
                if resposta != {}:
                    print(' Data da ultima alteraçao: ', resposta['data'])
                    if resposta['notas'] != []:
                        contador = 0
                        for nota in resposta['notas']:
                            contador += 1
                            print(' - Nota: ', contador)
                            print('    | Titulo da nota: ', nota['titulo'])
                            print('    | Sendo editada: ', 'Sim' if nota['status_edicao'] else 'Não')
                        titulo_nota = input(' Titulo da nota: ')
                        status_edicao = proxy.verificar_status_edicao_nota(nome_documento, titulo_nota)
                        status_alterado = False
                        if not status_edicao:
                            status_alterado = proxy.mudar_status_edicao_nota(nome_documento, titulo_nota)
                        if status_alterado:
                            alteracao_titulo = input(' Alterar titulo da nota: ')
                            alteracao_conteudo = input(' Alterar conteudo da nota: ')
                            resposta_nota_alterada = proxy.alterar_nota(nome_documento, titulo_nota, alteracao_titulo, alteracao_conteudo)
                            if titulo_nota != alteracao_titulo and alteracao_titulo != '':
                                titulo_nota = alteracao_titulo
                            if resposta_nota_alterada:
                                print('\n Nota alterada com sucesso!')
                            else:
                                print('\n Erro ao alterar nota.')
                            
                            proxy.mudar_status_edicao_nota(nome_documento, titulo_nota)
                        else:
                            print('  \nA nota não pode ser edita, pois ela já está em processo de alteracao')
                    else:
                        print('  Nao ha notas no documento.')
            
            esperar_enter()
        elif opcao == 9:
            limpar_terminal()
            print('Listar o conteudo de uma nota')
            print(' Documentos:')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print('  - ' + documento['titulo'])
                nome_documento = input(' Nome do documento: ')
                resposta = proxy.pegar_documento(nome_documento)
                if resposta != {}:
                    print(' Data da ultima alteraçao: ', resposta['data'])
                    if resposta['notas'] != []:
                        contador = 0
                        for nota in resposta['notas']:
                            contador += 1
                            print(' - Nota: ', contador)
                            print('    | Titulo da nota: ', nota['titulo'])
                        titulo_nota = input(' Titulo da nota: ')

                        for nota in resposta['notas']:
                            if nota['titulo'] == titulo_nota:
                                print('Conteudo da nota: ', nota['conteudo'])
                                break
                    else:
                        print('  Nao ha notas no documento.')
            
            esperar_enter()
        elif opcao == 10:
            limpar_terminal()
            print('Listar o conteudo de todas as nota')
            print(' Documentos:')
            documentos = proxy.pegar_documentos_usuario(int(dados_sessao[0]))
            if documentos:
                for documento in documentos:
                    print('  - ' + documento['titulo'])
                nome_documento = input(' Nome do documento: ')
                resposta = proxy.pegar_documento(nome_documento)
                if resposta != {}:
                    print(' Data da ultima alteraçao: ', resposta['data'])
                    if resposta['notas'] != []:
                        contador = 0
                        for nota in resposta['notas']:
                            contador += 1
                            print(' - Nota: ', contador)
                            print('    | Titulo da nota: ', nota['titulo'])
                            print('    | Conteudo da nota: ', nota['conteudo'])
                    else:
                        print('  Nao ha notas no documento.')
            
            esperar_enter()
        elif opcao == 0:
            limpar_terminal()
            print('Ate logo!')
            esperar_segundos(2)
            break
        else:
            print('Opçao invalida.')
            esperar_segundos(2)
