# -*- coding: utf-8 -*-
"""As tabelas do README, calculadas aqui e em lugar nenhum mais.

Nenhum numero deste projeto foi digitado a mao: o `ferramentas/medidor.py`
imprime o que sai daqui, e os testes prendem os mesmos valores.

A tabela da grade 7 x 7 leva quase um minuto e fica guardada por lado: pedir a
mesma grade duas vezes no mesmo processo nao paga a conta duas vezes.
"""
from __future__ import annotations

from . import forcabruta
from .juiz import LIMIAR_CONHECIDO, meia_travessia, probabilidade
from .transferencia import contagem_por_abertas, estados_por_coluna

_cache: dict[int, list[int]] = {}


def coeficientes(n: int) -> list[int]:
    if n not in _cache:
        _cache[n] = contagem_por_abertas(n)
    return _cache[n]


def tabela_travessia(lados=range(1, 8)):
    """Uma linha por lado da grade.

    `(n, configuracoes, atravessam, fracao, meia_travessia, erro_ate_o_limiar)`.
    """
    linhas = []
    for n in lados:
        c = coeficientes(n)
        total = 1 << (n * n)
        atravessam = sum(c)
        meia = meia_travessia(n, c)
        linhas.append((n, total, atravessam, atravessam / total, meia,
                       LIMIAR_CONHECIDO - meia))
    return linhas


def tabela_coeficientes(n: int = 4):
    """Os coeficientes da grade `n`: `(k, c_k, C(n*n, k))`."""
    from math import comb
    c = coeficientes(n)
    return [(k, c[k], comb(n * n, k)) for k in range(n * n + 1)]


def tabela_estados(lados=range(1, 8)):
    """Quanto a matriz de transferencia carrega, contra a forca bruta.

    `(n, maior_numero_de_estados, 2^(n*n))`.
    """
    return [(n, max(estados_por_coluna(n)), 1 << (n * n)) for n in lados]


def tabela_dualidade(lados=range(1, 5)):
    """A dualidade conferida grade por grade.

    `(n, configuracoes, violacoes_4_contra_8, violacoes_4_contra_4)`.
    """
    linhas = []
    for n in lados:
        linhas.append((n, 1 << (n * n),
                       forcabruta.violacoes_da_dualidade(n),
                       forcabruta.violacoes_com_quatro_dos_dois_lados(n)))
    return linhas


def tabela_dois_caminhos(lados=range(1, 5)):
    """Forca bruta contra matriz de transferencia: `(n, iguais, total)`."""
    linhas = []
    for n in lados:
        bruta = forcabruta.contagem_por_abertas(n)
        esperta = coeficientes(n)
        linhas.append((n, bruta == esperta, sum(bruta)))
    return linhas


def tabela_dois_sentidos(lados=range(1, 5)):
    """Quantas grades atravessam nos dois sentidos ao mesmo tempo.

    `(n, atravessam_horizontal, atravessam_nos_dois, fracao)`.
    """
    linhas = []
    for n in lados:
        h = sum(coeficientes(n))
        dois = forcabruta.atravessam_nos_dois_sentidos(n)
        linhas.append((n, h, dois, dois / h))
    return linhas


def curva(n: int, passos: int = 10):
    """A probabilidade de atravessar em alguns valores de p: `(p, P(p))`."""
    c = coeficientes(n)
    return [(i / passos, probabilidade(n, c, i / passos))
            for i in range(passos + 1)]
