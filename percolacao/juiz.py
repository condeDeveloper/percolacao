# -*- coding: utf-8 -*-
"""O juiz: o que a tabela de coeficientes e obrigada a obedecer.

Nada aqui chama a matriz de transferencia nem a forca bruta. Sao regras que
qualquer tabela correta cumpre, e que uma tabela errada quase sempre quebra:

- `c[k]` nunca passa de C(n*n, k): nao da para ter mais grades que atravessam
  com k casas abertas do que grades com k casas abertas;
- `c[k]` e zero enquanto k < n: atravessar exige pelo menos uma casa por coluna;
- `c[n]` e exatamente n: com n casas so, o unico jeito e uma linha reta, e ha n
  linhas;
- `c[n*n]` e 1: a grade toda aberta atravessa, e e uma so;
- `c[k]` e C(n*n, k) assim que k passa de n*n - n: com menos de n casas
  FECHADAS nao da para barrar, porque uma barreira precisa de uma casa fechada
  em cada linha -- e isso e a dualidade dita do outro lado;
- a lista nao decresce enquanto `c[k] < C(n*n, k)`... isso NAO e verdade, e por
  isso nao esta aqui: o que vale e a monotonicidade da PROBABILIDADE, nao dos
  coeficientes.

E ha a regra que nao e aritmetica nenhuma: a probabilidade de atravessar cresce
com p, vale 0 em p = 0 e 1 em p = 1.
"""
from __future__ import annotations

from math import comb

# Limiar da percolacao de sitio na grade quadrada, estimado por simulacao em
# 2008 (Feng, Deng e Blote) com oito casas decimais. Nao e usado em conta
# nenhuma: e so o alvo contra o qual o ponto de meia travessia e comparado.
LIMIAR_CONHECIDO = 0.59274605


def coeficientes_plausiveis(n: int, c) -> bool:
    """Confere as regras aritmeticas que toda tabela correta cumpre."""
    total = n * n
    if len(c) != total + 1:
        return False
    if any(v < 0 for v in c):
        return False
    if any(c[k] > comb(total, k) for k in range(total + 1)):
        return False
    if any(c[k] != 0 for k in range(n)):
        return False
    if c[n] != n:
        return False
    for k in range(total - n + 1, total + 1):
        if c[k] != comb(total, k):
            return False
    return c[total] == 1


def extremos_da_tabela(n: int, c):
    """Onde a tabela sai do zero e onde ela encosta no teto.

    Devolve `(ultimo_zero, primeiro_cheio)`. Os dois sao previstos pela mesma
    coisa, por lados opostos: para atravessar e preciso uma casa ABERTA em cada
    coluna, e para barrar e preciso uma casa FECHADA em cada linha.
    """
    total = n * n
    ultimo_zero = max([k for k in range(total + 1) if c[k] == 0], default=-1)
    cheios = [k for k in range(total + 1)
              if all(c[j] == comb(total, j) for j in range(k, total + 1))]
    return (ultimo_zero, min(cheios))


def probabilidade(n: int, c, p: float) -> float:
    """A probabilidade de atravessar quando cada casa abre com probabilidade p."""
    total = n * n
    soma = 0.0
    for k, v in enumerate(c):
        if v:
            soma += v * (p ** k) * ((1.0 - p) ** (total - k))
    return soma


def cresce_com_p(n: int, c, passos: int = 200) -> bool:
    """A probabilidade de atravessar nunca desce quando p sobe.

    Nao e obvio a partir dos coeficientes: e consequencia de abrir mais casas
    nunca atrapalhar, e um erro de sinal na tabela costuma quebrar isto antes de
    quebrar qualquer soma.
    """
    anterior = -1.0
    for i in range(passos + 1):
        atual = probabilidade(n, c, i / passos)
        if atual < anterior - 1e-12:
            return False
        anterior = atual
    return abs(probabilidade(n, c, 0.0)) < 1e-12 and \
        abs(probabilidade(n, c, 1.0) - 1.0) < 1e-9


def meia_travessia(n: int, c, voltas: int = 200) -> float:
    """O p em que a probabilidade de atravessar e exatamente 1/2, por bissecao.

    A funcao cresce com p e vai de 0 a 1, entao o ponto existe e e unico. E este
    numero, e nao a fracao de grades, que deveria se aproximar do limiar.
    """
    baixo, alto = 0.0, 1.0
    for _ in range(voltas):
        meio = (baixo + alto) / 2.0
        if probabilidade(n, c, meio) < 0.5:
            baixo = meio
        else:
            alto = meio
    return (baixo + alto) / 2.0
