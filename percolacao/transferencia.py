# -*- coding: utf-8 -*-
"""Matriz de transferencia: o polinomio inteiro sem abrir as 2^(n*n) grades.

A forca bruta do `forcabruta.py` para na grade 5 x 5, porque 2^25 ja sao trinta e
tres milhoes de configuracoes e 2^36 seriam setenta bilhoes. Aqui a grade e
percorrida COLUNA POR COLUNA, carregando so o que ainda pode mudar o resultado.

O estado e a coluna atual com um rotulo por casa:

    -1   casa fechada
     0   casa aberta e ligada a borda ESQUERDA por casas ja vistas
     1, 2, ...  casa aberta, ainda solta, numerada por componente

Dois componentes soltos diferentes precisam continuar diferentes, porque mais a
frente eles podem se juntar um ao outro ou ao 0. Ja os componentes ligados a
esquerda podem ser fundidos num rotulo so: para a pergunta "existe caminho da
esquerda para a direita", dois caminhos que ja chegaram da esquerda valem o
mesmo. E essa fusao que faz o numero de estados caber.

Um componente solto que nao aparece na coluna seguinte morre, e e jogado fora:
casa nenhuma pode mais alcanca-lo.

A contagem e por numero de casas abertas, nao por probabilidade: a tabela sai em
inteiros exatos, e o polinomio e montado depois. Nada de ponto flutuante no meio
da conta.
"""
from __future__ import annotations


def _normaliza(rotulos: list[int]) -> tuple[int, ...]:
    """Renumera os componentes soltos pela ordem de aparicao.

    Sem isso o mesmo estado apareceria com nomes diferentes e a tabela cresceria
    sem motivo.
    """
    troca: dict[int, int] = {}
    saida = []
    proximo = 1
    for r in rotulos:
        if r <= 0:
            saida.append(r)
            continue
        if r not in troca:
            troca[r] = proximo
            proximo += 1
        saida.append(troca[r])
    return tuple(saida)


def _junta(pai: dict, x: int) -> int:
    while pai[x] != x:
        pai[x] = pai[pai[x]]
        x = pai[x]
    return x


def _une(pai: dict, a: int, b: int) -> None:
    ra, rb = _junta(pai, a), _junta(pai, b)
    if ra == rb:
        return
    # O componente 0 (ligado a esquerda) sempre absorve o outro.
    if rb == 0:
        ra, rb = rb, ra
    pai[rb] = ra


def _primeira_coluna(n: int):
    """Os estados possiveis da coluna 0, com quantas casas abertas cada um.

    Toda casa aberta da coluna 0 ja encosta na borda esquerda, entao todas levam
    o rotulo 0 -- inclusive as que estao separadas por casas fechadas.
    """
    saida = {}
    for padrao in range(1 << n):
        rotulos = tuple(0 if padrao >> i & 1 else -1 for i in range(n))
        k = bin(padrao).count("1")
        saida.setdefault((rotulos, k), 0)
        saida[(rotulos, k)] += 1
    return saida


def _transicao(n: int, estado: tuple[int, ...], padrao: int) -> tuple[int, ...]:
    """O estado da coluna seguinte, dado o estado atual e quem abre na nova.

    As casas abertas da nova coluna entram como componentes proprios; depois se
    juntam a quem esta na mesma linha da coluna anterior (ligacao horizontal) e
    a quem esta em cima ou embaixo na propria coluna (ligacao vertical).

    O componente 0, que e o "ligado a esquerda", sempre engole o outro na uniao:
    e por isso que `_une` troca a ordem quando encontra o 0.

    Quem fica de fora da nova coluna morre junto com a coluna velha, e e por
    isso que o estado nao cresce sem parar.
    """
    pai: dict = {0: 0}
    novo: list = [-1] * n
    for i in range(n):
        if padrao >> i & 1:
            marca = ("novo", i)
            novo[i] = marca
            pai[marca] = marca
    for r in estado:
        if r > 0 and r not in pai:
            pai[r] = r

    for i in range(n):
        if novo[i] != -1 and estado[i] != -1:
            _une(pai, novo[i], estado[i])
    for i in range(n - 1):
        if novo[i] != -1 and novo[i + 1] != -1:
            _une(pai, novo[i], novo[i + 1])

    nomes: dict = {}
    final: list[int] = []
    proximo = 1
    for i in range(n):
        if novo[i] == -1:
            final.append(-1)
            continue
        raiz = _junta(pai, novo[i])
        if raiz == 0:
            final.append(0)
            continue
        if raiz not in nomes:
            nomes[raiz] = proximo
            proximo += 1
        final.append(nomes[raiz])
    return _normaliza(final)


def contagem_por_abertas(n: int) -> list[int]:
    """Quantas grades n x n atravessam da esquerda para a direita, por casas abertas.

    Devolve uma lista `c` com `c[k]` = numero de configuracoes com exatamente k
    casas abertas que atravessam. Inteiros exatos, sem probabilidade no meio.
    """
    if n < 1:
        raise ValueError("a grade comeca em 1")
    if n == 1:
        return [0, 1]

    tabela: dict = {}
    for (rotulos, k), quantas in _primeira_coluna(n).items():
        chave = (rotulos, k)
        tabela[chave] = tabela.get(chave, 0) + quantas

    for _coluna in range(1, n):
        nova: dict = {}
        for (estado, k), quantas in tabela.items():
            for padrao in range(1 << n):
                # Coluna inteira fechada nao e descartada: as colunas seguintes
                # ainda contam configuracoes, elas e que nunca vao atravessar.
                destino = _transicao(n, estado, padrao)
                chave = (destino, k + bin(padrao).count("1"))
                nova[chave] = nova.get(chave, 0) + quantas
        tabela = nova

    saida = [0] * (n * n + 1)
    for (estado, k), quantas in tabela.items():
        if 0 in estado:
            saida[k] += quantas
    return saida


def total_que_atravessa(n: int) -> int:
    return sum(contagem_por_abertas(n))


def estados_por_coluna(n: int) -> list[int]:
    """Quantos estados diferentes a tabela carrega depois de cada coluna.

    E a medida de quanto a matriz de transferencia economiza: a forca bruta
    carrega 2^(n*n) configuracoes, e esta lista mostra o que de fato precisa
    ficar de pe.
    """
    if n == 1:
        return [2]
    tabela: dict = {}
    for (rotulos, k), quantas in _primeira_coluna(n).items():
        tabela[(rotulos, k)] = tabela.get((rotulos, k), 0) + quantas
    saida = [len({e for e, _ in tabela})]
    for _coluna in range(1, n):
        nova: dict = {}
        for (estado, k), quantas in tabela.items():
            for padrao in range(1 << n):
                destino = _transicao(n, estado, padrao)
                chave = (destino, k + bin(padrao).count("1"))
                nova[chave] = nova.get(chave, 0) + quantas
        tabela = nova
        saida.append(len({e for e, _ in tabela}))
    return saida
