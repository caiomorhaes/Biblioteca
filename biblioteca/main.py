import json
from datetime import datetime
import time
from datetime import timedelta

ARQUIVO = "dados.json"

#função carregar arquivos
def carregar_dados():
    #abrindo arquivo "r" de read e encoding utf-8 para aceitar pontuação e portugues
    #as f = variavel criada
    #with garante abrir e fechar automaticamente
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

#função salvar arquivos
def salvar_dados(dados):
    #"w" para escrever, apaga tudo que tive dentro e escreve um novo conteudo
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        #json.dump escreve algo dentro do documento
        #indent 4 = organização visual
        #ensure_ascii = false, deixa com que ele leia acentos
        json.dump(dados, f, indent=4, ensure_ascii=False)

#função cadastrar usuario
def cadastrar_usuario(nome, email, senha):
    dados = carregar_dados()
    #checar para ver se o email ja n foi cadastrado
    for usuario in dados["usuarios"]:
        if usuario["email"] == email:
            print("Este Email já foi cadastrado!")
            return
    #criar novo usuario com nome email e senha
    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "livros_alugados": []
    }
    #dar append para o json e salvar os dados
    dados["usuarios"].append(novo_usuario)
    salvar_dados(dados)
    print("Usuário cadastrado com sucesso!")

#função para o login de contas ja existentes
def login(email, senha):
    dados = carregar_dados()
    for i, usuario in enumerate(dados["usuarios"]):
        if usuario["email"] == email and usuario["senha"] == senha:
            print(f'\nBem vindo(a) {usuario["nome"]}!')
            return i  # RETORNA O ÍNDICE
    print("Email ou senha incorretos.")
    return None

#filtros de gramatica (sem destruir o codigo kekekekskssk)
ROTULOS = {
    "nome": "Nome",
    "autor": "Autor",
    "genero": "Gênero",
    "publicação": "Publicação",
    "acessos": "Acessos",
    "id": "ID"
}

#função de mostrar livros
def mostrar_livros(lista_livros):
    #se nao estiver livro possivel
    if not lista_livros:
        print("\nNenhum livro encontrado.")
        input("\nPressione <enter> para continuar...")
        return
    # para cada livro em lista de livro
    for livro in lista_livros:
        print('\n' + '-' * 40)
        for chave, rotulo in ROTULOS.items():
            print(f'{rotulo}: {livro[chave]}')
        print('-' * 40)
        time.sleep(0.5)

#filtrar por genero
def filtrar_por_genero(dados):
    genero = input("Digite o genero que deseja filtrar: ").strip()
    livros_filtrados = [
        livro for livro in dados["livros"]
        if livro["genero"].lower() == genero.lower()
    ]
    mostrar_livros(livros_filtrados)

#transformar as datas de str em data
def chave_data(livro):
    try:
        data = datetime.strptime(livro["publicação"], "%d/%m/%Y")
        return data.year
    except ValueError:
        return int(livro["publicação"])

#filtros de mais recente e mais antigo
def ordenar_por_mais_recente(dados):
    livros_ordenados = sorted(
        dados["livros"],
        key=chave_data,
        reverse=True
    )
    mostrar_livros(livros_ordenados)

def ordenar_por_mais_antigo(dados):
    livros_ordenados = sorted(
        dados["livros"],
        key=chave_data
    )
    mostrar_livros(livros_ordenados)

def selecionar_livro(dados, indice_usuario):
    usuario = dados["usuarios"][indice_usuario]

    try:
        id_escolhido = int(input("\nDigite o ID do livro que deseja alugar: "))
    except ValueError:
        print("\nDigite um ID valido!")
        return

    livro_encontrado = None
    for livro in dados["livros"]:
        if livro["id"] == id_escolhido:
            livro_encontrado = livro
            break

    if not livro_encontrado:
        print("Livro não encontrado.")
        return

    for l in usuario["livros_alugados"]:
        if l["id"] == id_escolhido:
            print("Você já alugou este livro.")
            return

    data_aluguel = datetime.now()
    data_devolucao = data_aluguel + timedelta(days=7)

    usuario["livros_alugados"].append({
        "id": livro_encontrado["id"],
        "nome": livro_encontrado["nome"],
        "data_aluguel": data_aluguel.strftime("%d/%m/%Y"),
        "data_devolucao": data_devolucao.strftime("%d/%m/%Y")
    })

    livro_encontrado["acessos"] += 1
    salvar_dados(dados)

    print(f'\nLivro "{livro_encontrado["nome"]}" alugado com sucesso!')
    print(f'Devolução até: {data_devolucao.strftime("%d/%m/%Y")}')

#menu no terminal
def inicio():
    print('\n1 - Cadastrar')
    print('2 - Login')
    print('3 - Sair')

    opção = input("Escolha: ")

    #opção 1 para cadastrar
    if opção == "1":
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")
        cadastrar_usuario(nome, email, senha)

    #opção 2 para fazer login
    elif opção == "2":
        email = input("Email: ")
        senha = input("Senha: ")
        indice_usuario = login(email, senha)
        if indice_usuario is not None:
            print("Você está logado!")
            menu_principal(indice_usuario)

    #opção 3 para sair
    elif opção == "3":
        print("\nObrigado por utilizar o programa!")

def menu_principal(indice_usuario):
    while True:
        dados = carregar_dados()
        usuario = dados["usuarios"][indice_usuario]

        print('\n1 - Alugar Livros')
        print('2 - Livros Alugados')
        print('3 - Pagamentos')
        print('4 - Sair')

        opção = input("Escolha: ")

        if opção == "1":
            menu_filtro(indice_usuario)

        elif opção == "2":
            if not usuario["livros_alugados"]:
                print("\nVocê não possui livros alugados.")
            else:
                for l in usuario["livros_alugados"]:
                    print('-' * 40)
                    print(f'Nome: {l["nome"]}')
                    print(f'Alugado em: {l["data_aluguel"]}')
                    print(f'Devolução: {l["data_devolucao"]}')
                    print('-' * 40)

        elif opção == "3":
            print("Área de pagamentos ainda não implementada.")

        elif opção == "4":
            print("\nObrigado por utilizar o programa!")
            break

def menu_filtro(indice_usuario):
    while True:
        dados = carregar_dados()

        print("\n ORDENAR LIVROS")
        print("1 - Selecione livros")
        print("2 - Mais recentes")
        print("3 - Mais antigos")
        print("4 - Gênero")
        print("5 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            selecionar_livro(dados, indice_usuario)

        elif opcao == "2":
            ordenar_por_mais_recente(dados)

        elif opcao == "3":
            ordenar_por_mais_antigo(dados)

        elif opcao == "4":
            filtrar_por_genero(dados)

        elif opcao == "5":
            break

inicio()
