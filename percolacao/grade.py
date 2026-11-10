# -*- coding: utf-8 -*-
"""A grade n x n guardada num inteiro, e a pergunta "atravessa?".

Uma configuracao e um numero: o bit `linha * n + coluna` ligado quer dizer que a
casa esta ABERTA. Com n = 5 cabem 25 bits, e as 33.554.432 configuracoes da
grade inteira cabem num laco.

Atravessar, aqui, e ir da coluna da esquerda ate a coluna da direita andando so
por casas abertas. A vizinhanca pode ser de quatro casas (cima, baixo, esquerda,
direita) ou de oito (com as diagonais) -- e a diferenca entre as duas nao e
enfeite: e ela que faz a dualidade do `juiz.py` fechar.
"""
from __future__ import annotations


def bit(n: int, linha: int, coluna: int) -> int:
    return 1 << (linha * n + coluna)


def de_linhas(n: int, linhas) -> int:
    """Monta a configuracao a partir de uma lista de strings de '#' e '.'."""
    mascara = 0
    for i, texto in enumerate(linhas):
        for j, c in enumerate(texto):
            if c == "#":
                mascara |= bit(n, i, j)
    return mascara


def para_linhas(n: int, mascara: int) -> list[str]:
    return ["".join("#" if mascara >> (i * n + j) & 1 else "."
                    for j in range(n)) for i in range(n)]


def abertas(n: int, mascara: int) -> int:
    return bin(mascara & ((1 << (n * n)) - 1)).count("1")


def _vizinhos(n: int, oito: bool) -> list[int]:
    """Para cada casa, a mascara das casas vizinhas. Calculada uma vez por grade."""
    passos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if oito:
        passos += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    tabela = []
    for i in range(n):
        for j in range(n):
            m = 0
            for di, dj in passos:
                a, b = i + di, j + dj
                if 0 <= a < n and 0 <= b < n:
                    m |= bit(n, a, b)
            tabela.append(m)
    return tabela


_cache_vizinhos: dict[tuple[int, bool], list[int]] = {}


def vizinhos(n: int, oito: bool = False) -> list[int]:
    chave = (n, oito)
    if chave not in _cache_vizinhos:
        _cache_vizinhos[chave] = _vizinhos(n, oito)
    return _cache_vizinhos[chave]


def _coluna(n: int, j: int) -> int:
    m = 0
    for i in range(n):
        m |= bit(n, i, j)
    return m


def _linha(n: int, i: int) -> int:
    return ((1 << n) - 1) << (i * n)


def atravessa_horizontal(n: int, mascara: int, oito: bool = False) -> bool:
    """Existe caminho de casas abertas da coluna 0 ate a coluna n-1?

    Crescimento de mascara, nao pilha de casas: a fronteira inteira avanca de uma
    vez com um OU sobre a tabela de vizinhos. Com pilha, a varredura de 2^25
    configuracoes da grade 5 x 5 passava de meia hora.
    """
    esquerda = _coluna(n, 0) & mascara
    if not esquerda:
        return False
    direita = _coluna(n, n - 1)
    tabela = vizinhos(n, oito)
    alcancado = esquerda
    fronteira = esquerda
    while fronteira:
        nova = 0
        f = fronteira
        while f:
            b = f & -f
            nova |= tabela[b.bit_length() - 1]
            f ^= b
        nova &= mascara & ~alcancado
        if nova & direita:
            return True
        alcancado |= nova
        fronteira = nova
    return bool(alcancado & direita)


def atravessa_vertical(n: int, mascara: int, oito: bool = False) -> bool:
    """O mesmo, da linha de cima ate a linha de baixo."""
    cima = _linha(n, 0) & mascara
    if not cima:
        return False
    baixo = _linha(n, n - 1)
    tabela = vizinhos(n, oito)
    alcancado = cima
    fronteira = cima
    while fronteira:
        nova = 0
        f = fronteira
        while f:
            b = f & -f
            nova |= tabela[b.bit_length() - 1]
            f ^= b
        nova &= mascara & ~alcancado
        if nova & baixo:
            return True
        alcancado |= nova
        fronteira = nova
    return bool(alcancado & baixo)


def transposta(n: int, mascara: int) -> int:
    """A mesma grade virada na diagonal: troca linha com coluna."""
    saida = 0
    for i in range(n):
        for j in range(n):
            if mascara >> (i * n + j) & 1:
                saida |= bit(n, j, i)
    return saida


def complemento(n: int, mascara: int) -> int:
    return ~mascara & ((1 << (n * n)) - 1)
