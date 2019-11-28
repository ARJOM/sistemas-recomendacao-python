from notas import avaliacoes as avaliacoesNota
from filmes import avaliacoes as avaliacoesFilme
from math import sqrt


def euclidiana(base, usuario1, usuario2):
    si = {}
    for item in base[usuario1]:
        if item in base[usuario2]:
            si[item] = item

    if len(si) == 0:
        return 0

    soma = 0
    for item in si:
        soma += pow(base[usuario1][item] - base[usuario2][item], 2)

    return 1 / (1 + sqrt(soma))


def getSimilaridade(base, usuario):
    similaridade = []
    for outro in base:
        if outro != usuario:
            similaridade.append([euclidiana(base, usuario, outro), outro])

    similaridade.sort()
    similaridade.reverse()
    return similaridade[0:30]


def getRecomendacoesUsuario(base, usuario):
    totais = {}
    somaSimilaridade = {}
    for outro in base:
        if outro == usuario:
            continue
        similaridade = euclidiana(base, usuario, outro)

        if similaridade == 0:
            continue

        for filme in base[outro]:
            if filme not in base[usuario]:
                totais.setdefault(filme, 0)
                totais[filme] += base[outro][filme] * similaridade
                somaSimilaridade.setdefault(filme, 0)
                somaSimilaridade[filme] += similaridade

    rankings = []
    for filme, total in totais.items():
        rankings.append(((total / somaSimilaridade[filme]), filme))
    rankings.sort()
    rankings.reverse()
    return rankings[0:30]


def carregaMovieLens(path='/home/ricart/ml-100k'):
    filmes = {}
    for linha in open(path + '/u.item', encoding="ISO-8859-1"):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    base = {}
    for linha in open(path + '/u.data', encoding="ISO-8859-1"):
        (usuario, idFilme, nota, tempo) = linha.split("\t")
        base.setdefault(usuario, {})
        base[usuario][filmes[idFilme]] = float(nota)
    return base


def calculaItensSimilares(base):
    resultado = {}
    for item in base:
        notas = getSimilaridade(base, item)
        resultado[item] = notas
    return resultado


# def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
#     notasUsuario = baseUsuario[usuario]
#     notas = {}
#     totalSimilaridade = {}
#     for (item, nota) in notasUsuario.items():
#         for (similaridade, item2) in similaridadeItens[item]:
#             if item2 in notasUsuario:
#                 continue
#             notas.setdefault(item2, 0)
#             notas[item2] += similaridade * nota
#             totalSimilaridade.setdefault(item2, 0)
#             totalSimilaridade[item2] += similaridade
#         rankings = []
#         for item, score in notas.items():
#             rankings.append(((score/totalSimilaridade[item]), item))
#         rankings.sort()
#         rankings.reverse()
#         return rankings

def getRecomendacoesItens(baseUsuario, similaridadeItens, usuario):
    notasUsuario = baseUsuario[usuario]
    notas={}
    totalSimilaridade={}
    for (item, nota) in notasUsuario.items():
        for (similaridade, item2) in similaridadeItens[item]:
            if item2 in notasUsuario: continue
            notas.setdefault(item2, 0)
            notas[item2] += similaridade * nota
            totalSimilaridade.setdefault(item2,0)
            totalSimilaridade[item2] += similaridade
    rankings=[(score/totalSimilaridade[item], item) for item, score in notas.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


