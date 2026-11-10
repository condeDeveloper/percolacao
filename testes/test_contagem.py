# -*- coding: utf-8 -*-
"""Os dois contadores, um contra o outro, e as regras que os dois obedecem."""
from math import comb

from percolacao import forcabruta
from percolacao.juiz import (coeficientes_plausiveis, cresce_com_p,
                             extremos_da_tabela, meia_travessia, probabilidade)
from percolacao.transferencia import (contagem_por_abertas, estados_por_coluna,
                                      total_que_atravessa)


def test_forca_bruta_e_matriz_de_transferencia_dao_a_mesma_tabela():
    for n in (1, 2, 3, 4):
        assert forcabruta.contagem_por_abertas(n) == contagem_por_abertas(n), n


def test_totais_conhecidos():
    esperado = {1: 1, 2: 7, 3: 197, 4: 22193, 5: 10056959, 6: 18287614751}
    for n, total in esperado.items():
        assert total_que_atravessa(n) == total, n


def test_a_simetria_da_grade_quadrada():
    for n in (1, 2, 3, 4):
        assert forcabruta.contagem_vertical(n) == forcabruta.contagem_por_abertas(n)


def test_as_regras_aritmeticas_valem_em_toda_grade_medida():
    for n in range(1, 7):
        c = contagem_por_abertas(n)
        assert coeficientes_plausiveis(n, c), n
        assert c[n] == n
        assert c[n * n] == 1
        assert all(c[k] == 0 for k in range(n))


def test_os_dois_extremos_da_tabela():
    # Sai do zero em n (uma casa aberta por coluna) e encosta no teto em
    # n*n - n + 1 (uma casa fechada por linha para barrar).
    for n in range(1, 7):
        ultimo_zero, primeiro_cheio = extremos_da_tabela(n, contagem_por_abertas(n))
        assert ultimo_zero == n - 1, n
        assert primeiro_cheio == n * n - n + 1, n


def test_a_probabilidade_cresce_e_vai_de_zero_a_um():
    for n in range(1, 7):
        assert cresce_com_p(n, contagem_por_abertas(n)), n


def test_probabilidade_em_pontos_exatos():
    c = contagem_por_abertas(1)
    assert abs(probabilidade(1, c, 0.3) - 0.3) < 1e-12
    c4 = contagem_por_abertas(4)
    assert abs(probabilidade(4, c4, 0.0)) < 1e-12
    assert abs(probabilidade(4, c4, 1.0) - 1.0) < 1e-9


def test_fracao_em_meio_a_meio_e_a_soma_dividida_por_dois_elevado_a_n2():
    for n in range(1, 7):
        c = contagem_por_abertas(n)
        direto = sum(c) / (1 << (n * n))
        assert abs(probabilidade(n, c, 0.5) - direto) < 1e-9, n


def test_meia_travessia_sobe_com_o_lado():
    valores = [meia_travessia(n, contagem_por_abertas(n)) for n in range(1, 7)]
    assert valores == sorted(valores)
    assert abs(valores[0] - 0.5) < 1e-9


def test_estados_da_matriz_de_transferencia():
    esperado = {1: 2, 2: 7, 3: 18, 4: 46, 5: 120, 6: 316}
    for n, quantos in esperado.items():
        assert max(estados_por_coluna(n)) == quantos, n
        assert quantos < (1 << (n * n)) or n == 1


def test_grade_de_lado_zero_e_recusada():
    for f in (contagem_por_abertas, forcabruta.contagem_por_abertas):
        try:
            f(0)
        except ValueError:
            continue
        raise AssertionError("lado 0 passou em %s" % f)


def test_coeficientes_da_grade_4():
    c = contagem_por_abertas(4)
    assert c[4] == 4
    assert c[5] == 60
    assert c[9] == 5272
    assert c[10] == 5414          # o pico nao esta no meio
    assert c[13] == comb(16, 13)
    assert max(range(17), key=lambda k: c[k]) == 10
