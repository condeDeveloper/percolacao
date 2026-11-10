# Percolação de sítio em grade pequena, resolvida exatamente

Numa grade `n x n`, cada casa está **aberta** com probabilidade `p`. Existe
caminho de casas abertas da borda esquerda até a direita?

A resposta usual é simulação: sorteia-se um milhão de grades e conta-se a
fração. Aqui não há sorteio nenhum. A grade é pequena o bastante para ser
resolvida **inteira**, e o que sai não é uma estimativa: é o polinômio exato

    P(p) = soma de c_k * p^k * (1-p)^(n*n-k)

com os `c_k` em inteiros, contados um a um.

Dois contadores independentes calculam a mesma tabela: um abre as `2^(n*n)`
grades, o outro percorre a grade coluna por coluna e nunca abre nenhuma. Eles
concordam onde os dois cabem, e o segundo chega até o lado 7, onde as grades são
**562.949.953.421.312**.

Python puro, sem dependência. 37 testes.

```bash
pip install -e ".[dev]"
python -m pytest
python -m percolacao tabela 4
python -m percolacao meia 6
python -m percolacao dualidade 3
python ferramentas/medidor.py --tudo
```

## Os dois contadores

A **força bruta** abre todas as grades e pergunta a cada uma. Para no lado 4,
porque 2^25 já são trinta e três milhões e 2^36 seriam setenta bilhões. Ela não
existe para resolver o problema: existe para julgar o outro contador.

A **matriz de transferência** percorre coluna por coluna, carregando só o que
ainda pode mudar o resultado: quais casas da coluna atual estão abertas, quais
delas já chegaram da borda esquerda, e como as outras se agrupam. Componentes já
ligados à esquerda são fundidos num rótulo só — para a pergunta "existe caminho
da esquerda para a direita", dois caminhos que já chegaram valem o mesmo. É essa
fusão que faz o número de estados caber.

| n | estados que a tabela carrega | configurações da grade |
|---:|---:|---:|
| 4 | 46 | 65.536 |
| 5 | 120 | 33.554.432 |
| 6 | 316 | 68.719.476.736 |
| 7 | **841** | **562.949.953.421.312** |

As duas dão exatamente a mesma lista de coeficientes nos lados 1 a 4.

## A dualidade, e por que as vizinhanças têm de ser diferentes

As casas **abertas** atravessam da esquerda para a direita andando por quatro
vizinhos **se, e só se**, as casas **fechadas** não atravessam de cima para
baixo andando por **oito**.

| n | grades | violações com 4 contra 8 | violações com 4 dos dois lados |
|---:|---:|---:|---:|
| 2 | 16 | 0 | 2 |
| 3 | 512 | 0 | 118 |
| 4 | 65.536 | **0** | **21.150** |

Com quatro vizinhos dos dois lados, a afirmação falha em **32,3%** das grades da
ordem 4: existem grades em que ninguém atravessa, porque uma diagonal de casas
fechadas barra o caminho das abertas sem ser caminho ela mesma. A assimetria 4/8
não é escolha de gosto, é o que faz o teorema ser teorema.

## Os coeficientes, no lado 4

| k | atravessam | de C(16,k) |
|---:|---:|---:|
| 3 | 0 | 560 |
| 4 | 4 | 1.820 |
| 8 | 3.416 | 12.870 |
| 10 | **5.414** | 8.008 |
| 12 | 1.752 | 1.820 |
| 13 | 560 | **560** |

Os dois extremos da tabela saem da mesma regra, lida pelos dois lados:
**atravessar exige uma casa aberta em cada coluna** (então `c_k = 0` enquanto
`k < n`, e `c_n = n`, as `n` linhas retas), e **barrar exige uma casa fechada em
cada linha** (então `c_k` encosta no teto `C(n*n, k)` assim que `k` passa de
`n*n - n`). A segunda metade é a dualidade dita do outro lado.

## Quantas atravessam, e onde a chance é meio a meio

| n | configurações | atravessam | fração | p de meia travessia |
|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 50,00% | 0,50000000 |
| 3 | 512 | 197 | 38,48% | 0,55929632 |
| 5 | 33.554.432 | 10.056.959 | 29,97% | 0,57581007 |
| 6 | 68.719.476.736 | 18.287.614.751 | 26,61% | 0,57970276 |
| 7 | 562.949.953.421.312 | 133.267.613.878.665 | 23,67% | **0,58235130** |

O limiar conhecido da percolação de sítio na grade quadrada é **0,59274605**,
estimado por simulação.

## Quatro achados

**1. A varredura exata chega a 0,0104 do limiar de percolação com uma grade de
lado 7.** O `p` em que a chance de atravessar é exatamente um meio sobe de
`0,50000000` (lado 1) para `0,58235130` (lado 7), monótono, na direção de
`0,59274605`. Nenhum sorteio foi feito: o número sai de um polinômio de
coeficientes inteiros. Um limiar que normalmente se estima com milhões de
amostras aparece aqui contando.

**2. A fração de grades que atravessam CAI enquanto o ponto de meia travessia
SOBE — e as duas coisas são a mesma.** Com metade das casas abertas, 50% das
grades de lado 1 atravessam e só 23,67% das de lado 7. Parece que a travessia
fica mais difícil com o tamanho; o que acontece é que o limiar é 0,5927 e não
0,5, então `p = 1/2` está do lado errado, e quanto maior a grade mais ela se
decide.

**3. A dualidade só fecha com vizinhanças diferentes dos dois lados.** Quatro
vizinhos para as abertas e oito para as fechadas: **zero violações em 65.536
grades**. Quatro dos dois lados: **21.150 violações**, uma em cada três grades.
É o tipo de detalhe que some num enunciado em prosa e derruba um programa
inteiro.

**4. O pico da tabela não está no meio.** Na grade 4 x 4 o maior coeficiente
está em `k = 10` (5.414 de 8.008, **67,6%**), não em `k = 8`, onde estão as
grades mais numerosas. O deslocamento é o mesmo 0,5927 aparecendo em forma
discreta: `10/16 = 0,625`, e não `0,5`.

## O que as medidas me corrigiram

- **Eu esperava que a fração de grades que atravessam convergisse para alguma
  coisa.** Ela cai e vai para zero, e a pergunta estava mal feita: a fração é
  `P(1/2)`, um ponto só da curva, e `1/2` não é o limiar. O que converge é o
  **ponto de meia travessia**, que é outra conta. Trocar uma pela outra é trocar
  o eixo da pergunta.
- **A primeira travessia usava pilha de casas e a varredura do lado 5 não
  terminava.** Trocar por crescimento de máscara — a fronteira inteira avança de
  uma vez com um OU sobre a tabela de vizinhos — resolveu sem mudar uma resposta.
- **Eu escrevi a dualidade com quatro vizinhos dos dois lados**, que é como ela
  costuma ser dita de boca, e o verificador acusou 21.150 grades de desacordo no
  lado 4. Achei que o verificador estivesse errado. Estava certo: faltava a
  vizinhança de oito do lado fechado. Virou o achado número 3 e uma função
  própria, que mede exatamente o tamanho do erro.
- **Achei que o pico da tabela estivesse no meio**, onde o binomial é máximo.
  Está em `k = 10` de 16. O binomial puxa para o meio e a travessia puxa para
  cima, e quem ganha é a travessia.
- **A matriz de transferência guardava componentes ligados à esquerda
  separadamente**, cada um com seu nome. Os estados explodiam sem necessidade:
  para a pergunta que se faz, dois caminhos que já chegaram da esquerda são o
  mesmo caminho. Fundir os dois num rótulo só é o que faz o lado 7 caber em 841
  estados.

## Arquivos

```
percolacao/grade.py          a grade num inteiro, e a pergunta "atravessa?"
percolacao/forcabruta.py     abre as 2^(n*n) grades, uma por uma
percolacao/transferencia.py  a mesma tabela coluna por coluna
percolacao/juiz.py           as regras que toda tabela correta cumpre
percolacao/medidas.py        as tabelas deste README
ferramentas/medidor.py
testes/                      37 testes, os pesados separados
```

O `juiz.py` não importa nenhum dos dois contadores, e os dois contadores não se
importam um ao outro.
