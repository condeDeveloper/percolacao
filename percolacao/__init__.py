# -*- coding: utf-8 -*-
"""Percolacao de sitio em grade pequena, resolvida exatamente.

O pacote tem cinco pedacos que nao se misturam:

    grade          a grade num inteiro, e a pergunta "atravessa?"
    forcabruta     abre as 2^(n*n) grades, uma por uma
    transferencia  a mesma tabela coluna por coluna, sem abrir todas
    juiz           as regras que toda tabela correta cumpre
    medidas        as tabelas que vao para o README

O `juiz` nao importa nenhum dos dois contadores, e os dois contadores nao se
importam um ao outro: e por isso que valem como conferencia um do outro.
"""
from .grade import (abertas, atravessa_horizontal, atravessa_vertical,
                    complemento, de_linhas, para_linhas, transposta, vizinhos)
from .juiz import (LIMIAR_CONHECIDO, coeficientes_plausiveis, cresce_com_p,
                   meia_travessia, probabilidade)
from .transferencia import (contagem_por_abertas, estados_por_coluna,
                            total_que_atravessa)

__all__ = [
    "LIMIAR_CONHECIDO", "abertas", "atravessa_horizontal",
    "atravessa_vertical", "coeficientes_plausiveis", "complemento",
    "contagem_por_abertas", "cresce_com_p", "de_linhas", "estados_por_coluna",
    "meia_travessia", "para_linhas", "probabilidade", "total_que_atravessa",
    "transposta", "vizinhos",
]

__version__ = "1.0.0"
