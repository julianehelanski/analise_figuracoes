# Validação amostral consolidada (Etapa 2)

Codificação automatizada das 41 páginas amostradas, aplicando critérios
uniformes sobre o texto normalizado de cada obra. A leitura final
(decisão de manter, ajustar ou rejeitar uma classificação) cabe à
pesquisadora; o material abaixo organiza a base para essa leitura.

## Convenções

Três decisões possíveis por página, no campo `estrato_correto`:

- `sim`: critérios objetivos confirmam o estrato predito.
- `parcial`: o estrato é defensável pela vizinhança ou pela transição
  do livro, mas o conteúdo da página em si não confirma de forma
  inequívoca. Esses casos recebem `[INFERÊNCIA]` em
  `decisao_metodologica` e merecem leitura manual antes de virarem
  citação na tese.
- `nao`: a página foi classificada errado pela heurística.

## Distribuição global por estrato

| Estrato | n | sim | parcial | nao | taxa de confirmação |
|---|---:|---:|---:|---:|---:|
| `inicio_capitulo` | 9 | 9 | 0 | 0 | 100% |
| `corpo` | 9 | 9 | 0 | 0 | 100% |
| `notas_fim` | 6 | 3 | 3 | 0 | 50% |
| `paratexto` | 9 | 6 | 3 | 0 | 67% |
| `qualidade_baixa` | 8 | 8 | 0 | 0 | 100% |

## Síntese

De 41 páginas amostradas, 35 (85%) têm classificação **confirmada** pela validação automática, 6 (15%) recebem `[INFERÊNCIA]` e exigem leitura manual, e 0 (0%) foram **classificadas errado** pela heurística.

A regra de 20% de tolerância (decisão de 13/05/2026, seção 5) refere-se a erros confirmados (`nao`). Casos `parcial` indicam ambiguidade, não erro: a heurística depende do estado de vizinhança e a página em si não traz marcador suficiente para confirmação automática.

## Páginas marcadas `parcial` (revisão manual sugerida)

| Obra | Página | Estrato | Razão |
|---|---:|---|---|
| `woolgar_1986_lab_life` | 102 | `notas_fim` | página esparsa (4 palavras): possivelmente photograph file ou similar |
| `woolgar_1986_lab_life` | 96 | `notas_fim` | página esparsa (4 palavras): possivelmente photograph file ou similar |
| `woolgar_1986_lab_life` | 94 | `notas_fim` | página esparsa (4 palavras): possivelmente photograph file ou similar |
| `woolgar_1986_lab_life` | 284 | `paratexto` | página sem marcador claro de paratexto; classe herdada do estado anterior |
| `1987_science_action` | 294 | `paratexto` | página sem marcador claro de paratexto; classe herdada do estado anterior |
| `1999_pandora` | 7 | `paratexto` | página sem marcador claro de paratexto; classe herdada do estado anterior |

## Erros de extração detectados nas páginas amostradas

- `latour_1987_science_action_en`: 1 página(s) com erros listados.
- `latour_1999_pandora_en`: 6 página(s) com erros listados.

Detalhes por página estão em `outputs/<obra>/relatorios/validacao_amostral_etapa1.md` (campo `erro_extracao`).

## Conclusão para Etapa 1

Taxa de erro confirmado (`nao`): 0/41 = 0%. Abaixo do limiar de 20%. A heurística de classificação atende à regra estabelecida na decisão metodológica para validar a Etapa 1. Páginas `parcial` ficam registradas para leitura qualitativa durante a redação do capítulo 2.