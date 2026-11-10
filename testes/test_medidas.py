# -*- coding: utf-8 -*-
"""Os numeros do README, presos aqui.

Se um contador mudar e um numero mudar, este arquivo quebra antes de o README
mentir. Nenhum valor daqui foi estimado: todos sairam do
`ferramentas/medidor.py`.

A grade 7 x 7, que leva quase um minuto, mora no `test_pesados.py`.
"""
from percolacao.juiz import LIMIAR_CONHECIDO
from percolacao.medidas import (curva, tabela_coeficientes, tabela_dois_caminhos,
                                tabela_dois_sentidos, tabela_dualidade,
                                tabela_estados, tabela_travessia)


def test_os_dois_caminhos_dao_a_mesma_tabela():
    for n, iguais, _total in tabela_dois_caminhos():
        assert iguais, n


def test_dualidade_fecha_com_quatro_contra_oito():
    linhas = {l[0]: l for l in tabela_dualidade()}
    for n, _grades, boas, _ruins in tabela_dualidade():
        assert boas == 0, n
    assert linhas[2][3] == 2
    assert linhas[3][3] == 118
    assert linhas[4][3] == 21150
    assert linhas[4][1] == 65536


def test_a_dualidade_com_quatro_dos_dois_lados_falha_em_um_terco():
    linhas = {l[0]: l for l in tabela_dualidade()}
    _n, grades, _boas, ruins = linhas[4]
    assert round(100 * ruins / grades, 1) == 32.3
    _n, grades, _boas, ruins = linhas[3]
    assert round(100 * ruins / grades, 1) == 23.0


def test_travessia_ate_o_lado_6():
    esperado = {
        1: (2, 1), 2: (16, 7), 3: (512, 197), 4: (65536, 22193),
        5: (33554432, 10056959), 6: (68719476736, 18287614751),
    }
    for n, total, atravessam, _f, _m, _falta in tabela_travessia(range(1, 7)):
        assert (total, atravessam) == esperado[n], n


def test_meia_travessia_ate_o_lado_6():
    esperado = {
        1: 0.50000000, 2: 0.54119610, 3: 0.55929632, 4: 0.56972413,
        5: 0.57581007, 6: 0.57970276,
    }
    for n, _t, _a, _f, meia, falta in tabela_travessia(range(1, 7)):
        assert round(meia, 8) == esperado[n], n
        assert round(falta, 8) == round(LIMIAR_CONHECIDO - esperado[n], 8), n


def test_a_fracao_que_atravessa_cai_enquanto_o_ponto_de_meia_sobe():
    linhas = tabela_travessia(range(1, 7))
    fracoes = [l[3] for l in linhas]
    meias = [l[4] for l in linhas]
    assert fracoes == sorted(fracoes, reverse=True)
    assert meias == sorted(meias)
    assert round(100 * fracoes[-1], 4) == 26.6120


def test_estados_contra_configuracoes():
    esperado = {1: 2, 2: 7, 3: 18, 4: 46, 5: 120, 6: 316}
    for n, quantos, total in tabela_estados(range(1, 7)):
        assert quantos == esperado[n], n
        if n > 1:
            assert quantos < total


def test_coeficientes_da_grade_4_e_o_pico_fora_do_meio():
    linhas = {k: (ck, possiveis) for k, ck, possiveis in tabela_coeficientes(4)}
    assert linhas[4][0] == 4
    assert linhas[8][0] == 3416
    assert linhas[10][0] == 5414
    assert linhas[13][0] == linhas[13][1] == 560
    pico = max(linhas, key=lambda k: linhas[k][0])
    assert pico == 10
    assert round(100 * 5414 / 8008, 1) == 67.6


def test_atravessar_nos_dois_sentidos():
    esperado = {1: (1, 1), 2: (7, 5), 3: (197, 123), 4: (22193, 12563)}
    for n, h, dois, _f in tabela_dois_sentidos():
        assert (h, dois) == esperado[n], n
    assert round(100 * 12563 / 22193, 1) == 56.6


def test_a_curva_do_lado_6():
    pontos = dict(curva(6))
    assert round(pontos[0.5], 6) == 0.266120
    assert round(pontos[0.6], 6) == 0.564492
    assert round(pontos[0.4], 6) == 0.080716
    assert pontos[0.0] == 0.0
    assert round(pontos[1.0], 9) == 1.0
