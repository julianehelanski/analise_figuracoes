# Relatório de extração e qualidade — Etapa 1

Consolidação técnica da etapa de preparação textual antes do KWIC. Gerado por `scripts/01b_normalize_text.py` (normalização) e contadores subsequentes. Os arquivos crus em `corpus/txt/` permanecem como artefato auditável; a análise opera sobre `corpus/txt_norm/`.

## 1. Volume e qualidade global por obra

| Obra | Páginas | Palavras | Qualidade global | Taxa qualidade boa | Taxa qualidade baixa |
|---|---:|---:|:---:|---:|---:|
| `latour_woolgar_1986_lab_life_en` | 296 | 105.749 | boa | 0,949 | 0,034 |
| `latour_1987_science_action_en` | 314 | 139.861 | boa | 0,990 | 0,006 |
| `latour_1999_pandora_en` | 337 | 128.001 | boa | 0,979 | 0,018 |
| **Total** | **947** | **373.611** |  |  |  |

Métrica `qualidade_pagina` por página avalia proporção de caracteres estranhos e de linhas curtas. Critérios herdados de `scripts/01_extract_text.py`: qualidade global "boa" exige ≥80% das páginas como qualidade `boa` e ≤5% como `baixa`. As três obras passam.

## 2. Operações de normalização aplicadas

Detalhes em `docs/decisoes_metodologicas.md`, Adendo 1 (14/05/2026). Contagem por operação:

| Obra | Soft hyphen | Hifenização EOL | Marcadores `((NN))` | Cabeçalhos espaçados | Replacement `�` |
|---|---:|---:|---:|---:|---:|
| `latour_woolgar_1986_lab_life_en` | 0 | 500 | 0 | 0 | 0 |
| `latour_1987_science_action_en` | 0 | 55 | 276 | 0 | 0 |
| `latour_1999_pandora_en` | 2.367 | 18 | 0 | 6 | 220 |

Notas:

- O grosso da normalização em Pandora foi remoção de soft hyphens U+00AD internos a palavras (`per­formed` → `performed`), problema sistemático da extração via leitor de PDF.
- Em Lab Life o ganho foi reconstruir 500 palavras quebradas no fim de linha por `pdftotext -layout`.
- Em Science in Action o ganho foi retirar 276 marcadores `((NN))` que o conversor injetou no corpo.
- O cabeçalho espaçado `P A N D O R A ' S H O P E` em Pandora ocorre nas variantes (com letras coladas, com palavras intermediárias, etc.) que escapam ao regex conservador; o impacto sobre o KWIC é nulo porque tokens de letra única não casam termos do catálogo.

## 3. Classificação por estado da página

A heurística de `scripts/01b_normalize_text.py` (e `01_extract_text.py` para futuras re-extrações) classifica cada página em uma das cinco classes `inicio_capitulo`, `corpo`, `notas_fim`, `paratexto`, `qualidade_baixa`. Adendos 2 e 3 das decisões metodológicas refinaram a heurística para distinguir front matter (não-sticky) de back matter (sticky), detectar início de capítulo no topo da página (5 primeiras linhas), e aceitar variantes tipográficas como `CHAPTER ONE` ou letras espaçadas `C H A P T E R` (estilo Pandora's Hope). Distribuição resultante:

| Obra | inicio_capitulo | corpo | notas_fim | paratexto | qualidade_baixa |
|---|---:|---:|---:|---:|---:|
| `latour_woolgar_1986_lab_life_en` | 7 | 200 | 33 | 46 | 10 |
| `latour_1987_science_action_en` | 4 | 277 | 4 | 27 | 2 |
| `latour_1999_pandora_en` | 3 | 297 | 0 | 31 | 6 |

Notas sobre os estratos sub-representados:

- `notas_fim` em Pandora's Hope: a obra não preserva linha isolada "Notes" detectável pela regex (a seção de notas é absorvida no back matter); como a heurística não identifica transição corpo → notas_fim, esse estrato fica vazio para essa obra.
- `qualidade_baixa` em Science in Action: o livro só tem 2 páginas marcadas como qualidade baixa, sinal positivo da extração; a amostra fica sub-representada porque o livro não oferece mais material para validar.

## 4. Tabela de frequências preliminar (consolidada)

Frequência absoluta e por 10 000 palavras, por grupo figurativo, por obra. Fonte: `outputs/<id>/csv/frequencias.csv` (gerada por `scripts/03_frequencies.py`).

| Grupo | 1986 lab_life | 1987 science_action | 1999 pandora | Obras |
|---|---|---|---|---:|
| `inscription` | 11,82 (125) | 4,43 (62) | 1,09 (14) | 3/3 |
| `construction` | 19,29 (204) | 3,79 (53) | 4,84 (62) | 3/3 |
| `network` | 4,26 (45) | 9,08 (127) | 2,73 (35) | 3/3 |
| `translation` | 0,28 (3) | 5,58 (78) | 5,47 (70) | 3/3 |
| `black_box` | 0,95 (10) | 9,58 (134) | 1,33 (17) | 3/3 |
| `enrollment` | 0,09 (1) | 3,15 (44) | 0,94 (12) | 3/3 |
| `proposition` | 0,47 (5) | 0,36 (5) | 3,20 (41) | 3/3 |
| `actor_network` | 0 | 1,22 (17) | 2,42 (31) | 2/3 |
| `immutable_mobile` | 0 | 0,29 (4) | 0,23 (3) | 2/3 |
| `centre_of_calculation` | 0 | 1,36 (19) | 0,31 (4) | 2/3 |
| `spokesperson` | 0,09 (1) | 3,29 (46) | 0 | 2/3 |
| `articulation` | 0 | 0,29 (4) | 4,14 (53) | 2/3 |
| `trial_of_strength` | 0 | 1,43 (20) | 0 | 1/3 |
| `factish` | 0 | 0 | 4,14 (53) | 1/3 |
| `circulating_reference` | 0 | 0 | 1,41 (18) | 1/3 |
| `agonistic` | 3,03 (32) | 0 | 0 | 1/3 |

Total de ocorrências válidas por obra (após exclusões): 426 (1986), 613 (1987), 413 (1999). Total geral: 1.452.

## 5. Outputs gerados na Etapa 1

Por obra (em `outputs/<id>/`):

- `csv/kwic.csv` — uma linha por ocorrência, com janela ±10 palavras, página, posição e flag de exclusão.
- `csv/frequencias.csv` — contagem por grupo, com frequência por 10k palavras.
- `csv/cocorrencia.csv` — matriz grupo × grupo com pesos por janela de 200 palavras.
- `csv/amostra_validacao.csv` — amostra estratificada para validação manual (com colunas vazias prontas para codificação).
- `figuras/frequencia_grupos.png` — ranking visual de grupos.
- `figuras/densidade_ao_longo_do_texto.png` — histograma da posição relativa das ocorrências.
- `figuras/rede_cocorrencia.png` — grafo de cocorrência figural.
- `relatorios/frequencias.md` — ranking + exemplos top-3.
- `relatorios/cocorrencia.md` — top 20 pares por força de cocorrência.
- `relatorios/validacao_amostral_etapa1.md` — guia de leitura da amostra.

Consolidados (em `outputs/`):

- `trajetoria_latour_1986_1999.csv` — matriz grupo × obra com perfil de trajetória.
- `trajetoria_latour_1986_1999.md` — relatório textual da trajetória 1986-1999.
- `amostra_validacao_etapa1.csv` — 26 linhas (limitação descrita em §3).

## 6. Status da amostra estratificada (passo 6 do plano)

A decisão de 13/05/2026 previu 45 páginas (15 por obra, 5 estratos de 3). Após a correção da heurística (Adendos 2 e 3), a amostra efetiva tem **41 páginas**, distribuídas:

- `latour_woolgar_1986_lab_life_en`: 15 páginas (3 em cada estrato; cobertura completa).
- `latour_1987_science_action_en`: 14 páginas (3 `inicio_capitulo`, 3 `corpo`, 3 `notas_fim`, 3 `paratexto`, 2 `qualidade_baixa`).
- `latour_1999_pandora_en`: 12 páginas (3 `inicio_capitulo`, 3 `corpo`, 0 `notas_fim`, 3 `paratexto`, 3 `qualidade_baixa`).

As 4 páginas faltantes correspondem a estratos onde o próprio livro não oferece material:

- 1 página em `qualidade_baixa` de Science in Action (o livro só tem 2 páginas classificadas como baixa qualidade; sinal positivo de extração limpa).
- 3 páginas em `notas_fim` de Pandora's Hope (a obra não preserva linha isolada "Notes" antes das notas globais; a seção é absorvida no back matter).

A amostra está pronta em `outputs/amostra_validacao_etapa1.csv` (consolidada) e em `outputs/<id>/csv/amostra_validacao.csv` (por obra), com colunas vazias para codificação manual durante a Etapa 2 (`estrato_correto`, `classe_correta`, `erro_extracao`, `decisao_metodologica`).

---

**Resumo executivo**: extração e normalização concluídas com qualidade boa nas três obras (947 páginas, 373.611 palavras, 1.452 ocorrências válidas no catálogo). KWIC, frequências, visualizações, cocorrência e trajetória entregues e consistentes com leitura qualitativa esperada (Lab Life concentra `inscription`/`construction`; Science in Action consolida `black_box`/`network`/`translation`; Pandora introduz `factish` e `circulating_reference`). Amostra estratificada com 41/45 páginas, faltando apenas onde o próprio livro não oferece material. Heurística de classificação de páginas refinada em dois adendos. Pronto para passar à Etapa 2 (validação amostral) com aprovação.
