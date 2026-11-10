# -*- coding: utf-8 -*-
"""Linha de comando: `python -m percolacao <comando>`.

    tabela [n]      quantas grades de lado n atravessam, por casas abertas
    meia [n]        o p em que a chance de atravessar e um meio
    curva [n]       a chance de atravessar em p = 0, 0,1, ..., 1
    dualidade [n]   confere a dualidade nas 2^(n*n) grades de lado n
"""
from __future__ import annotations

import sys

from .forcabruta import violacoes_com_quatro_dos_dois_lados, violacoes_da_dualidade
from .juiz import LIMIAR_CONHECIDO, meia_travessia, probabilidade
from .transferencia import contagem_por_abertas


def _lado(args, padrao=4) -> int:
    return int(args[0]) if args else padrao


def _tabela(args) -> int:
    n = _lado(args)
    c = contagem_por_abertas(n)
    print("grade %d x %d: %d configuracoes, %d atravessam"
          % (n, n, 1 << (n * n), sum(c)))
    for k, v in enumerate(c):
        if v:
            print("  %2d casas abertas: %d" % (k, v))
    return 0


def _meia(args) -> int:
    n = _lado(args)
    c = contagem_por_abertas(n)
    meia = meia_travessia(n, c)
    print("lado %d: meia travessia em p = %.8f" % (n, meia))
    print("  limiar conhecido     %.8f" % LIMIAR_CONHECIDO)
    print("  falta                %.8f" % (LIMIAR_CONHECIDO - meia))
    return 0


def _curva(args) -> int:
    n = _lado(args)
    c = contagem_por_abertas(n)
    for i in range(11):
        p = i / 10
        print("  p=%.1f  P=%.6f" % (p, probabilidade(n, c, p)))
    return 0


def _dualidade(args) -> int:
    n = _lado(args, 3)
    print("lado %d, %d grades" % (n, 1 << (n * n)))
    print("  violacoes com 4 contra 8:        %d" % violacoes_da_dualidade(n))
    print("  violacoes com 4 dos dois lados:  %d"
          % violacoes_com_quatro_dos_dois_lados(n))
    return 0


COMANDOS = {"tabela": _tabela, "meia": _meia, "curva": _curva,
            "dualidade": _dualidade}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] not in COMANDOS:
        print(__doc__)
        return 0 if not argv else 2
    return COMANDOS[argv[0]](argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
