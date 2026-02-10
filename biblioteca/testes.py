import json
from datetime import datetime


open("dados.json", "r")
ARQUIVO = "dados.json"

def carregar_dados():
    #abrindo arquivo "r" de read e encoding utf-8 para aceitar pontuação e portugues
    #as f = variavel criada
    #with garante abrir e fechar automaticamente
    with open(ARQUIVO, "r",encoding='utf-8') as f:
        return json.load(f)


def mostrar_livros(lista_livros):
    if not lista_livros:
        print("Nenhum livro encontrado.")
        return
    for livro in lista_livros:
        print('-' * 40)
        print(f'nome: {livro["nome"]}')
        print(f'autor: {livro["autor"]}')
        print(f'genero: {livro["genero"]}')
        print(f'publicação: {livro["publicação"]}')
        print(f'acessos: {livro["acessos"]}')

def filtrar_por_genero (dados):
    genero = input("Digite o genero que deseja filtrar: ").strip()

    livros_filtrados = [
        livro for livro in dados["livros"]
        if livro["genero"].lower() == genero.lower()
    ]

    mostrar_livros(livros_filtrados)

def chave_data (livro):
    try:
        data = datetime.strptime(livro["publicação"], "%d/%m/%Y")
        return data.year
    except ValueError:
        return int(livro["publicação"])

#filtros de mais recente e mais antigo

def ordenar_por_mais_recente (dados):
    livros_ordenados = sorted(
        dados["livros"],
        key=chave_data,
        reverse=True
    )
    mostrar_livros(livros_ordenados)

def ordenar_por_mais_antigo (dados):
    livros_ordenados = sorted(
    dados["livros"],
    key = chave_data
 )
    mostrar_livros(livros_ordenados)


def menu_ordenacao():
    dados = carregar_dados()

    while True:
        print("\n ORDENAR LIVROS")
        print("1 - Mais recentes")
        print("2 - Mais antigos")
        print("3 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            ordenar_por_mais_recente(dados)

        elif opcao == "2":
            ordenar_por_mais_antigo(dados)

        elif opcao == "3":
            break

menu_ordenacao()
