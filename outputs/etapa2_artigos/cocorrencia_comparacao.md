# Cocorrência figural nos artigos teóricos (Etapa 2.4)

Data da execução: 15 de maio de 2026.

Apliquei `scripts/05_cooccurrence.py` aos dois artigos em duas configurações de janela:

- **Janela 200 palavras**: controle direto, mesma janela usada nos livros da Etapa 1. Permite comparação entre os artigos e os livros, mas em textos curtos cobre proporção alta do total (15% no *Recalling*, 2,5% no *Clarifications*), o que produz pares espúrios por aproximação física no texto.
- **Janela proporcional**: 2% das palavras totais por obra, arredondada. Recalling = 25 palavras; Clarifications = 157 palavras. Padroniza a fração textual da janela entre obras, ao custo de tornar a comparação direta com os livros indireta.

A decisão sobre qual janela apresentar na tese cabe à pesquisadora.

## Clarifications 1996 (7.848 palavras)

Janela controle: 200 palavras. Janela proporcional: 157 palavras (2% do texto).

Pares com cocorrência em pelo menos uma das duas janelas: 22.

| par (A, B) | j=200 | j=157 (prop.) |
|---|---:|---:|
| network, topologia | 783 | 616 |
| textil, topologia | 222 | 171 |
| actor_network, network | 162 | 138 |
| network, textil | 130 | 101 |
| actor_network, topologia | 102 | 84 |
| militar, network | 10 | 8 |
| topologia, translation | 8 | 7 |
| actor_network, textil | 7 | 6 |
| centre_of_calculation, network | 5 | 4 |
| centre_of_calculation, textil | 5 | 3 |
| actor_network, militar | 4 | 3 |
| network, translation | 5 | 2 |
| actor_network, construction | 3 | 3 |
| construction, network | 3 | 2 |
| construction, topologia | 3 | 1 |
| militar, textil | 2 | 2 |
| centre_of_calculation, topologia | 2 | 2 |
| construction, textil | 2 | 2 |
| militar, topologia | 3 | 0 |
| textil, translation | 2 | 1 |
| militar, translation | 1 | 1 |
| actor_network, translation | 1 | 1 |

## Recalling 1999 (1.241 palavras)

Janela controle: 200 palavras. Janela proporcional: 25 palavras (2% do texto).

Pares com cocorrência em pelo menos uma das duas janelas: 6.

| par (A, B) | j=200 | j=25 (prop.) |
|---|---:|---:|
| network, topologia | 20 | 2 |
| actor_network, network | 6 | 2 |
| militar, topologia | 5 | 1 |
| construction, topologia | 5 | 0 |
| construction, network | 1 | 0 |
| construction, militar | 1 | 0 |

## Leitura sintética dos contrastes

Em ambas as obras, os pares com maior força são consistentes entre as duas janelas: `network`–`topologia` lidera por margem larga (783/616 em *Clarifications*; 20/2 em *Recalling*), seguido por `actor_network`–`network` e `textil`–`topologia` (este último presente apenas no *Clarifications*, onde o campo têxtil tem ocorrências; no *Recalling* o campo têxtil é zero, então não há pares têxtil).

O campo `militar` ocupa posição periférica em ambas as obras. Pares envolvendo `militar` aparecem em ordens de grandeza menores que `network`–`topologia` (*Clarifications* j=157: `militar`–`network` = 8 versus `network`–`topologia` = 616). A leitura confirma o achado da Etapa 2.2: o vocabulário militar não articula a malha argumentativa central dos artigos metateóricos; a malha é estruturada por `network`–`topologia` e suas extensões `actor_network` e `textil`.

## Decisão recomendada (pendente Gate 2.4)

Para a tese, sugiro apresentar a **janela proporcional** como configuração principal, com a janela 200 como controle metodológico em nota de rodapé. A janela proporcional controla o problema do tamanho do texto e preserva o ranking dos pares centrais. A janela 200 fica disponível como ponto de comparação com os livros, dado que a Etapa 1 operou com janela 200.

A pesquisadora decide se a recomendação é aceita, ou se a tese apresenta as duas configurações lado a lado com nota metodológica explícita.

## Outputs gerados

- `outputs/<obra>/csv/cocorrencia_j200.csv` (controle).
- `outputs/<obra>/csv/cocorrencia_j025.csv` ou `_j157.csv` (proporcional).
- `outputs/<obra>/relatorios/cocorrencia_j200.md` e variantes.
- `outputs/<obra>/figuras/rede_cocorrencia_j200.png` e variantes (PNG + SVG).
- `outputs/etapa2_artigos/cocorrencia_comparacao.md` (este arquivo).