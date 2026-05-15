# Validação amostral semântica (Etapa 2.6): instruções de preenchimento

Data da geração: 15 de maio de 2026.

As planilhas em `outputs/<artigo>/csv/validacao_amostral_semantica.csv` e o consolidado em `outputs/etapa2_artigos/validacao_amostral_semantica.csv` contêm 82 ocorrências para classificação manual nos quatro campos centrais do argumento têxtil-topológico: `textil`, `topologia`, `network`, `actor_network`. O campo `militar` está fora desta amostra (já 100% desambiguado na Etapa 2.2).

## Distribuição da amostra

| Obra | Campo | Camada | n |
|---|---|---|---:|
| latour_1996_clarifications_en | actor_network | A_top_densidade | 5 |
| latour_1996_clarifications_en | actor_network | B_aleatoria | 5 |
| latour_1996_clarifications_en | actor_network | C_variantes_raras | 5 |
| latour_1996_clarifications_en | network | A_top_densidade | 5 |
| latour_1996_clarifications_en | network | B_aleatoria | 5 |
| latour_1996_clarifications_en | network | C_variantes_raras | 5 |
| latour_1996_clarifications_en | textil | A_top_densidade | 5 |
| latour_1996_clarifications_en | textil | B_aleatoria | 5 |
| latour_1996_clarifications_en | textil | C_variantes_raras | 5 |
| latour_1996_clarifications_en | topologia | A_top_densidade | 5 |
| latour_1996_clarifications_en | topologia | B_aleatoria | 5 |
| latour_1996_clarifications_en | topologia | C_variantes_raras | 5 |
| latour_1999_recalling_en | actor_network | exaustiva | 2 |
| latour_1999_recalling_en | network | exaustiva | 7 |
| latour_1999_recalling_en | textil | exaustiva | 0 |
| latour_1999_recalling_en | topologia | exaustiva | 13 |

## Protocolo de três camadas (A/B/C)

Para cada campo com 15 ou mais ocorrências, sorteio três amostras independentes de cinco ocorrências cada:

- **Camada A — top-densidade**: ocorrências cuja janela KWIC tem o maior número de termos do mesmo campo lexical. Heurística: passagens onde o campo aparece de modo concentrado.
- **Camada B — aleatória**: cinco ocorrências aleatórias (seed=42).
- **Camada C — variantes raras**: ocorrências cuja variante (termo exato) é das menos frequentes no campo. Heurística: mais suspeitas de polissemia ou uso periférico.

Quando o campo tem menos de 15 ocorrências (caso comum no *Recalling*), a amostra é exaustiva (todas as ocorrências entram, camada `exaustiva`).

## Colunas para preenchimento manual

- `uso_figural` (`sim`, `parcial`, `nao`): a ocorrência é uso figural do campo no sentido da tese? Tropo têxtil-topológico para descrever ANT, rede ou prática científica?
- `subcategoria` (texto livre): se `nao`, classificar o motivo. Sugestões: `tecnico` (uso técnico do termo, e.g. `tie` como verbo, `net` como rede de computadores), `polissemia` (termo em sentido comum), `descritivo` (descrição de objeto não-figural), `metalinguistico` (Latour cita o próprio vocabulário).
- `comentario` (texto livre): observação metodológica que valha registro etnográfico (ex.: discordância com a classificação automática anterior, candidatos a citação na tese, casos-limite).

## Procedimento sugerido

1. Abrir o CSV consolidado em planilha (ou um por obra).
2. Ler cada linha (`contexto_antes` + **`trecho_central`** + `contexto_depois`).
3. Marcar `uso_figural`; em casos `nao` ou `parcial`, anotar `subcategoria`.
4. Usar `comentario` para registrar discordâncias e candidatos a citação.
5. Salvar e me avisar quando terminar. Gero então:
   - Taxa de uso figural por campo e por camada (precisão estimada).
   - Lista das `subcategoria` mais frequentes (mapa de polissemia).
   - Densidade refinada figural para `textil` e `topologia` (com base na taxa de figuralidade aplicada à contagem bruta).

## Após o preenchimento

A pesquisadora me devolve a planilha preenchida. Gero:

- `outputs/etapa2_artigos/validacao_amostral_resultados.md` com as taxas.
- `outputs/etapa2_artigos/tabela_textil_topologico_refinada.tex` com a densidade refinada (bruta × taxa de figuralidade).
- Atualização do relatório consolidado da Etapa 2.