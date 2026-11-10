# -*- coding: utf-8 -*-
"""Imprime as tabelas que vao para o README. Nenhum numero sai daqui a mao.

    python ferramentas/medidor.py          ate o lado 6
    python ferramentas/medidor.py --tudo   inclui o lado 7

A grade 7 x 7 tem 562.949.953.421.312 configuracoes e leva quase um minuto pela
matriz de transferencia, por isso fica atras de um sinalizador.
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from percolacao.juiz import LIMIAR_CONHECIDO  # noqa: E402
from percolacao.medidas import (curva, tabela_coeficientes,  # noqa: E402
                                tabela_dois_caminhos, tabela_dois_sentidos,
                                tabela_dualidade, tabela_estados,
                                tabela_travessia)


def titulo(texto: str) -> None:
    print()
    print(texto)
    print("-" * len(texto))


def dois_caminhos() -> None:
    titulo("Forca bruta contra matriz de transferencia")
    print("  n   mesma tabela  atravessam")
    for n, iguais, total in tabela_dois_caminhos():
        print("  %-3d %-13s %d" % (n, "sim" if iguais else "NAO", total))


def dualidade() -> None:
    titulo("A dualidade, conferida grade por grade")
    print("  n   grades      4 contra 8   4 dos dois lados")
    for n, grades, boas, ruins in tabela_dualidade():
        print("  %-3d %-11d %-12d %d" % (n, grades, boas, ruins))


def travessia(ate_7: bool) -> None:
    titulo("Quantas atravessam, e onde a chance e um meio")
    print("  n   configuracoes       atravessam          fracao    meia travessia  falta")
    inicio = time.time()
    for n, total, atravessam, fracao, meia, falta in tabela_travessia(
            range(1, 8 if ate_7 else 7)):
        print("  %-3d %-19d %-19d %.6f  %.8f      %.8f"
              % (n, total, atravessam, fracao, meia, falta))
    print("  limiar conhecido: %.8f    (%.1fs)"
          % (LIMIAR_CONHECIDO, time.time() - inicio))


def estados(ate_7: bool) -> None:
    titulo("O que a matriz de transferencia carrega")
    print("  n   estados  configuracoes")
    for n, quantos, total in tabela_estados(range(1, 8 if ate_7 else 7)):
        print("  %-3d %-8d %d" % (n, quantos, total))


def coeficientes() -> None:
    titulo("Os coeficientes da grade 4 x 4")
    print("   k  atravessam  de C(16,k)")
    for k, ck, possiveis in tabela_coeficientes(4):
        if ck or k <= 4:
            print("  %2d  %-11d %d" % (k, ck, possiveis))


def sentidos() -> None:
    titulo("Atravessar nos dois sentidos ao mesmo tempo")
    print("  n   horizontal  nos dois  fracao")
    for n, h, dois, fracao in tabela_dois_sentidos():
        print("  %-3d %-11d %-9d %.6f" % (n, h, dois, fracao))


def desenho_da_curva() -> None:
    titulo("A chance de atravessar, lado 6")
    for p, valor in curva(6):
        print("  p=%.1f  P=%.6f" % (p, valor))


def main() -> int:
    tudo = "--tudo" in sys.argv
    dois_caminhos()
    dualidade()
    coeficientes()
    sentidos()
    estados(tudo)
    travessia(tudo)
    desenho_da_curva()
    if not tudo:
        print()
        print("(o lado 7 so com --tudo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
