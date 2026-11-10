# -*- coding: utf-8 -*-
"""A grade e a travessia, medidas em desenhos escritos a mao."""
from percolacao.grade import (abertas, atravessa_horizontal,
                              atravessa_vertical, bit, complemento, de_linhas,
                              para_linhas, transposta, vizinhos)


def test_ida_e_volta_entre_desenho_e_numero():
    desenho = ["#.#", ".##", "#.."]
    m = de_linhas(3, desenho)
    assert para_linhas(3, m) == desenho
    assert abertas(3, m) == 5


def test_bit_na_posicao_certa():
    assert bit(3, 0, 0) == 1
    assert bit(3, 1, 0) == 1 << 3
    assert bit(3, 2, 2) == 1 << 8


def test_travessia_de_uma_linha_reta():
    m = de_linhas(3, ["###", "...", "..."])
    assert atravessa_horizontal(3, m)
    assert not atravessa_vertical(3, m)


def test_travessia_que_precisa_desviar():
    m = de_linhas(3, ["##.", ".#.", ".##"])
    assert atravessa_horizontal(3, m)
    assert atravessa_vertical(3, m)


def test_diagonal_so_atravessa_com_oito_vizinhos():
    m = de_linhas(3, ["#..", ".#.", "..#"])
    assert not atravessa_horizontal(3, m)
    assert atravessa_horizontal(3, m, oito=True)


def test_grade_vazia_e_grade_cheia():
    for n in (1, 2, 4):
        cheia = (1 << (n * n)) - 1
        assert atravessa_horizontal(n, cheia)
        assert atravessa_vertical(n, cheia)
        assert not atravessa_horizontal(n, 0)
        assert complemento(n, cheia) == 0
        assert complemento(n, 0) == cheia


def test_transposta_troca_os_dois_sentidos():
    for desenho in (["##.", ".#.", ".##"], ["#..", "##.", ".##"],
                    ["...", "###", "..."]):
        m = de_linhas(3, desenho)
        t = transposta(3, m)
        assert atravessa_horizontal(3, m) == atravessa_vertical(3, t)
        assert transposta(3, t) == m


def test_vizinhanca_de_quatro_e_de_oito():
    q = vizinhos(3, False)
    o = vizinhos(3, True)
    centro = 1 * 3 + 1
    assert bin(q[centro]).count("1") == 4
    assert bin(o[centro]).count("1") == 8
    canto = 0
    assert bin(q[canto]).count("1") == 2
    assert bin(o[canto]).count("1") == 3


def test_uma_casa_fechada_corta_a_unica_ponte():
    aberta = de_linhas(3, ["#.#", "###", "#.#"])
    assert atravessa_horizontal(3, aberta)
    sem_meio = aberta & ~bit(3, 1, 1)
    assert not atravessa_horizontal(3, sem_meio)
