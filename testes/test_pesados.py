# -*- coding: utf-8 -*-
"""A grade 7 x 7: 562.949.953.421.312 configuracoes, resolvidas em um minuto.

A tabela roda UMA VEZ, guardada pelo `medidas.coeficientes`, e todos os testes
daqui leem a mesma lista.
"""
from math import comb

from percolacao.juiz import (LIMIAR_CONHECIDO, coeficientes_plausiveis,
                             cresce_com_p, extremos_da_tabela, meia_travessia)
from percolacao.medidas import coeficientes, tabela_estados


def test_a_grade_7_inteira():
    c = coeficientes(7)
    assert sum(c) == 133267613878665
    assert coeficientes_plausiveis(7, c)
    assert c[7] == 7
    assert c[49] == 1
    assert extremos_da_tabela(7, c) == (6, 43)


def test_meia_travessia_do_lado_7():
    meia = meia_travessia(7, coeficientes(7))
    assert round(meia, 8) == 0.58235130
    assert round(LIMIAR_CONHECIDO - meia, 8) == 0.01039475
    assert meia < LIMIAR_CONHECIDO


def test_a_fracao_do_lado_7():
    fracao = sum(coeficientes(7)) / (1 << 49)
    assert round(100 * fracao, 3) == 23.673


def test_a_probabilidade_do_lado_7_cresce():
    assert cresce_com_p(7, coeficientes(7))


def test_841_estados_contra_meio_quatrilhao_de_grades():
    linhas = {n: (q, t) for n, q, t in tabela_estados(range(1, 8))}
    quantos, total = linhas[7]
    assert quantos == 841
    assert total == 562949953421312
    assert round(total / quantos / 1e9) == 669


def test_o_teto_da_tabela_do_lado_7():
    c = coeficientes(7)
    for k in range(43, 50):
        assert c[k] == comb(49, k), k
    assert c[42] < comb(49, 42)
