# -*- coding: utf-8 -*-
"""A varredura burra: abre as 2^(n*n) grades, uma por uma.

Nao serve para grade grande -- a de lado 6 teria 68.719.476.736 configuracoes --
e nao e para isso que ela existe. Ela existe para ser a SEGUNDA CABECA: o
`transferencia.py` calcula a mesma tabela por um caminho esperto, e so vale
confiar nele porque os dois dao exatamente a mesma lista nas grades em que os
dois cabem.

Tambem e aqui que a dualidade do `juiz.py` e conferida configuracao por
configuracao, o que o caminho esperto nao saberia fazer.
"""
from __future__ import annotations

from .grade import (abertas, atravessa_horizontal, atravessa_vertical,
                    complemento)


def contagem_por_abertas(n: int, oito: bool = False) -> list[int]:
    """Quantas grades n x n atravessam da esquerda para a direita, por casas abertas."""
    if n < 1:
        raise ValueError("a grade comeca em 1")
    saida = [0] * (n * n + 1)
    for mascara in range(1 << (n * n)):
        if atravessa_horizontal(n, mascara, oito):
            saida[abertas(n, mascara)] += 1
    return saida


def contagem_vertical(n: int, oito: bool = False) -> list[int]:
    """O mesmo, de cima para baixo. Tem de dar a mesma lista, por simetria."""
    saida = [0] * (n * n + 1)
    for mascara in range(1 << (n * n)):
        if atravessa_vertical(n, mascara, oito):
            saida[abertas(n, mascara)] += 1
    return saida


def violacoes_da_dualidade(n: int) -> int:
    """Quantas das 2^(n*n) grades desobedecem a dualidade. O esperado e zero.

    A dualidade: as casas ABERTAS atravessam da esquerda para a direita andando
    por quatro vizinhos se, e so se, as casas FECHADAS **nao** atravessam de
    cima para baixo andando por oito vizinhos.

    As duas vizinhancas diferentes nao sao detalhe: com quatro dos dois lados a
    afirmacao e falsa, e existem grades em que ninguem atravessa.
    """
    ruins = 0
    for mascara in range(1 << (n * n)):
        aberto_cruza = atravessa_horizontal(n, mascara, False)
        fechado_cruza = atravessa_vertical(n, complemento(n, mascara), True)
        if aberto_cruza == fechado_cruza:
            ruins += 1
    return ruins


def violacoes_com_quatro_dos_dois_lados(n: int) -> int:
    """A mesma conta com vizinhanca de quatro nos dois lados: quantas falham.

    Serve para mostrar que a vizinhanca de oito do lado fechado e necessaria,
    nao escolha de gosto.
    """
    ruins = 0
    for mascara in range(1 << (n * n)):
        aberto_cruza = atravessa_horizontal(n, mascara, False)
        fechado_cruza = atravessa_vertical(n, complemento(n, mascara), False)
        if aberto_cruza == fechado_cruza:
            ruins += 1
    return ruins


def atravessam_nos_dois_sentidos(n: int) -> int:
    """Quantas grades atravessam ao mesmo tempo na horizontal e na vertical."""
    total = 0
    for mascara in range(1 << (n * n)):
        if atravessa_horizontal(n, mascara) and atravessa_vertical(n, mascara):
            total += 1
    return total
