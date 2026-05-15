# Relatório consolidado da Etapa 2: análise lexicométrica dos artigos teóricos de Latour

Data da execução: 15 de maio de 2026. Cinco subetapas executadas em sequência (2.0, 2.1, 2.2, 2.4, 2.5), com gates de revisão pela pesquisadora entre cada uma. A Etapa 2.3 não foi necessária (cobertura automática 4/4 das ocorrências militares dos artigos). A Etapa 2.6 (validação amostral semântica A/B/C) fica como pendência ao final deste relatório.

Este documento consolida a contagem lexicométrica nos dezenove campos figurativos (dezessete do catálogo da Etapa 1 e duas adições da Etapa 2: `textil` e `topologia`) para as cinco obras de Latour em análise: três livros monográficos (*Laboratory Life* 1986, *Science in Action* 1987, *Pandora's Hope* 1999) e dois artigos metateóricos (*Clarifications* 1996, *Recalling ANT* 1999). A pergunta empírica que orienta o trabalho é a divisão de trabalho metafórico por gênero textual proposta pelo briefing da Etapa 2: o vocabulário militar-industrial domina nos livros monográficos solo; o vocabulário têxtil-topológico ocupa o terreno nos artigos metateóricos.

## Etapa 2.1: contagem bruta. Densidade do campo militar (ocorrências por 10.000 palavras)

| Obra | Palavras | n militar | freq./10k |
|---|---:|---:|---:|
| Lab Life 1986 | 105.749 | 39 | 3.69 |
| Sci. in Action 1987 | 139.861 | 374 | 26.74 |
| Pandora 1999 | 128.001 | 212 | 16.56 |
| Clarifications 1996 | 7.848 | 3 | 3.82 |
| Recalling 1999 | 1.241 | 1 | 8.06 |

A leitura quantitativa sustenta o contraste central do briefing: nos livros monográficos em que Latour é autor solo, a densidade do campo militar oscila entre 16,56 e 26,74 ocorrências por 10.000 palavras, ao passo que nos dois artigos metateóricos a densidade fica entre 3,82 e 8,06. Em *Laboratory Life* 1986, escrita em coautoria com Steve Woolgar, a densidade militar (3,69) está em patamar próximo ao dos artigos, fato que merece registro etnográfico: a inflexão militar-industrial parece consolidar-se com Latour solo a partir de 1987.

A contagem bruta do *Recalling* (n=1) e do *Clarifications* (n=3) cai para próximo de zero após a desambiguação prevista para a Etapa 2.2:

- *Recalling* 1999: a única ocorrência é `wars` em `"the recent Science Wars"` (referência ao debate público dos anos 1990 entre cientistas e estudiosos das ciências, categoria `descritivo-historica`).
- *Clarifications* 1996: `allies` em `"network of allies and extend his power"` é uso que Latour cita para criticar (categoria `metalinguistico`); `enemies` em `"pre-relativist enemies"` é uso conceitual-debate; `alliance` em `"La nouvelle alliance"` (Prigogine e Stengers) é título de livro citado (categoria `descritivo-bibliografico`).

Nenhuma das ocorrências militares dos dois artigos é uso figural do vocabulário militar-industrial como tropo para a prática científica, contrário ao que predomina em *Science in Action* (de onde provêm `allies`(92), `mobilisation`(28), `mobilised`(24), `alliances`(22) entre as variantes top).

## Densidade dos campos têxtil e topologia

| Obra | Palavras | n têxtil | freq./10k | n topologia | freq./10k |
|---|---:|---:|---:|---:|---:|
| Lab Life 1986 | 105.749 | 13 | 1.23 | 146 | 13.81 |
| Sci. in Action 1987 | 139.861 | 111 | 7.94 | 485 | 34.68 |
| Pandora 1999 | 128.001 | 105 | 8.20 | 353 | 27.58 |
| Clarifications 1996 | 7.848 | 39 | 49.69 | 118 | 150.36 |
| Recalling 1999 | 1.241 | 0 | 0.00 | 13 | 104.75 |

O campo `topologia` é o vocabulário que ocupa o terreno deixado pelo vocabulário militar nos artigos: a densidade no *Clarifications* (150,36/10k) e no *Recalling* (104,75/10k) supera a do mesmo campo nos livros monográficos (entre 13,81 e 34,68/10k). O campo `textil` segue padrão análogo no *Clarifications* (49,69/10k), enquanto no *Recalling* a densidade é nula, o que sugere uma especialização interna entre os dois artigos: *Clarifications* mobiliza vocabulário têxtil-topológico de modo denso, *Recalling* concentra-se na topologia.

Variantes top do `textil` em *Clarifications*: `net`(10), `nets`(3), `tied`(3), `tie`(2). A passagem que ancora qualitativamente esse achado está na página 76 do PDF interno, com a sequência `"fibrous, thread-like, wiry, stringy, ropy, capillary character"` (confirmada por sanity check em `scripts/13_audit_articles_etapa2.py`). A inspeção das variantes do campo na Etapa 2.2 (KWIC) é necessária para depurar polissemias prováveis como `tie` (laço/empate), `net` (rede/líquido), `string` (corda/sequência de caracteres).

## Ressalvas metodológicas

1. O *Recalling* opera sobre 1.241 palavras de corpo (convenção `split`), cerca de 80% do artigo original. As páginas 15 e 25 do volume estão excluídas por falha sistemática de OCR. Detalhamento em `docs/decisoes_metodologicas.md`, seção Etapa 2 § 3.

2. O briefing § 2 previa a presença, no *Recalling*, da citação metalinguística `"vocabulary association, translation, alliance, obligatory passage point"`. A inspeção do `.txt` confirma que essa passagem não está no corpus disponível, o que sugere que ela se encontra em uma das páginas excluídas (15 ou 25 do volume). A contagem efetiva do campo militar no *Recalling* (n=1, com `wars` em `Science Wars`) é portanto distinta da prevista (n=1, com `alliance` metalinguístico). O argumento comparativo de divisão de trabalho metafórico não é afetado: a única ocorrência permanece não-figural.

3. As contagens dos campos `textil` e `topologia` carregam polissemia esperada. A validação amostral semântica da Etapa 2.6, com mesma estratificação A/B/C aplicada à Etapa 1, vai estabelecer a taxa de uso figural por campo.

## Outputs gerados

- `outputs/etapa2_artigos/tabela_comparativa_5_obras_n.csv` (contagem absoluta).
- `outputs/etapa2_artigos/tabela_comparativa_5_obras_freq.csv` (densidade por 10k).
- `outputs/etapa2_artigos/tabela_comparativa_5_obras.tex` (LaTeX, pronto para inclusão).
- `outputs/<obra>/csv/frequencias.csv` (atualizados nas 5 obras com `textil` e `topologia`).

## Etapa 2.2: desambiguação automática do campo militar nos artigos

Data da execução: 15 de maio de 2026, sequencial à Etapa 2.1 e ao Gate 2.1 confirmado pela pesquisadora.

Apliquei `scripts/15_etapa2_desambiguar_militar.py` sobre as quatro ocorrências do campo militar nos dois artigos, com cinco categorias possíveis e gatilhos automáticos na seguinte ordem de prioridade:

1. `descritivo_historico`: colocação com objeto histórico (`Science Wars`, `World War`, `Cold War`, `Franco-Prussian War`, `War and Peace`, etc.). Reutiliza a regra da Etapa 1.
2. `descritivo_bibliografico`: ≥2 entre ano em parênteses, editora conhecida e nomes próprios sequenciais na janela.
3. `metalinguistico`: aspas em torno (≥2) e ≥1 termo da TAR, ou indicador citacional e ≥2 termos da TAR.
4. `conceitual_debate`: ≥2 palavras terminadas em `-ist`, `-ists`, `-ism`, `-isms` na janela (escolas teóricas).
5. `figurativo`: default, sem gatilho. Uso figural do vocabulário militar como tropo da prática científica.

Resultado, com gatilho automático aceito como sugestão inicial em todas as quatro ocorrências:

| Obra | Pág. | Termo | Categoria | Gatilho |
|---|---:|---|---|---|
| *Recalling* 1999 | 1 | `wars` | descritivo_historico | casa `Science Wars` |
| *Clarifications* 1996 | 1 | `allies` | metalinguistico | aspas=4, termos TAR=2 (`network`, `network`) |
| *Clarifications* 1996 | 1 | `enemies` | conceitual_debate | ismos = `Reflexivists`, `pre-relativist` |
| *Clarifications* 1996 | 1 | `alliance` | descritivo_bibliografico | ano entre parênteses + editora (`Gallimard/Bantam`) + autores sequenciais (`Prigogine et Stengers`) |

A contagem refinada figural (uso militar-industrial como tropo da prática científica) cai a zero nos dois artigos:

| Obra | Palavras | Bruta n | Bruta /10k | Refinada n | Refinada /10k |
|---|---:|---:|---:|---:|---:|
| *Laboratory Life* 1986 | 105.749 | 39 | 3,69 | 37 | 3,50 |
| *Science in Action* 1987 | 139.861 | 374 | 26,74 | 364 | 26,03 |
| *Pandora's Hope* 1999 | 128.001 | 212 | 16,56 | 156 | 12,19 |
| *Clarifications* 1996 | 7.848 | 3 | 3,82 | **0** | **0,00** |
| *Recalling ANT* 1999 | 1.241 | 1 | 8,06 | **0** | **0,00** |

A contagem refinada figural é zero nos dois artigos: o vocabulário militar-industrial está presente apenas em uso descritivo-histórico, descritivo-bibliográfico, metalinguístico ou de polêmica conceitual entre escolas teóricas. A hipótese da divisão de trabalho metafórico por gênero textual ganha sustentação empírica completa: o léxico militar-industrial recua de 16-26/10k nos livros monográficos para 0/10k nos artigos metateóricos, quando a leitura figural é restringida ao tropo da prática científica.

A contagem refinada dos livros vem do `refinamento/militar_refinado_tres_obras.csv` da Etapa 1, sem reanálise. A contagem refinada dos artigos vem da desambiguação automática desta etapa, com a categoria final sugerida igual à categoria automática, pendente de revisão manual da pesquisadora (Etapa 2.3).

### Outputs da Etapa 2.2

- `outputs/etapa2_artigos/militar_classificacao_automatica.csv`: 4 ocorrências dos artigos, com `categoria_auto`, `gatilho_detectado`, `categoria_final` (igual à automática) e `justificativa`. A pesquisadora ajusta `categoria_final` se discordar.
- `outputs/etapa2_artigos/tabela_militar_refinada_5_obras.tex`: tabela LaTeX consolidada, pronta para `\input{}` no master da tese.

## Etapa 2.4: cocorrência figural

Data da execução: 15 de maio de 2026, sequencial ao Gate 2.2 confirmado pela pesquisadora.

Apliquei `scripts/05_cooccurrence.py` aos dois artigos em duas configurações de janela, conforme briefing § 3.4:

- **Janela 200 palavras** (controle direto, mesma janela aplicada aos livros da Etapa 1).
- **Janela proporcional 2%** das palavras totais por obra: 25 palavras para *Recalling* (sobre 1.241), 157 palavras para *Clarifications* (sobre 7.848). Os valores resultam da convenção `split` registrada em `corpus/qualidade_extracao.csv`; o briefing § 3.4 antecipava 27 e 159 a partir da convenção `\b\w+\b`, ligeiramente diferente.

Top 5 pares por força, em cada configuração:

**Clarifications 1996:**

| Par | j=200 | j=157 (prop.) |
|---|---:|---:|
| network, topologia | 783 | 616 |
| textil, topologia | 222 | 171 |
| actor_network, network | 162 | 138 |
| network, textil | 130 | 101 |
| actor_network, topologia | 102 | 84 |

**Recalling 1999:**

| Par | j=200 | j=25 (prop.) |
|---|---:|---:|
| network, topologia | 20 | 2 |
| actor_network, network | 6 | 2 |
| militar, topologia | 5 | 1 |

O ranking dos pares principais é consistente entre as duas janelas em ambas as obras. O campo militar ocupa posição periférica nos dois artigos: em *Clarifications* o par `militar`–`network` (8 na janela proporcional) é cerca de 77 vezes menor que `network`–`topologia` (616). A malha argumentativa central dos artigos é estruturada por `network`–`topologia` e suas extensões `actor_network` e `textil`.

### Outputs da Etapa 2.4

- `outputs/<obra>/csv/cocorrencia_j200.csv` (matriz controle).
- `outputs/<obra>/csv/cocorrencia_j025.csv` (Recalling, proporcional).
- `outputs/<obra>/csv/cocorrencia_j157.csv` (Clarifications, proporcional).
- `outputs/<obra>/relatorios/cocorrencia_j*.md` (top 20 pares por configuração).
- `outputs/<obra>/figuras/rede_cocorrencia_j*.{png,svg}` (rede com nós dimensionados por frequência do grupo e arestas dimensionadas pela força de cocorrência, layout *force-directed* com `seed=42`).
- `outputs/etapa2_artigos/cocorrencia_comparacao.md`: relatório consolidado lado a lado das duas configurações para cada artigo.

### Recomendação para a tese (pendente Gate 2.4)

Sugiro adotar a **janela proporcional** como configuração principal na tabela e na figura do capítulo 2, com a janela 200 mencionada em nota de rodapé como controle metodológico. A justificativa: a janela proporcional padroniza a fração textual da janela entre obras de tamanhos distintos, e o ranking dos pares centrais é preservado. A janela 200 permanece como ponto de comparação com os livros monográficos.

A decisão final cabe à pesquisadora. Alternativas viáveis: apresentar as duas configurações lado a lado, ou manter apenas a 200 e mover a proporcional para o apêndice metodológico.

## Etapa 2.5: outputs comparativos consolidados

Data da execução: 15 de maio de 2026, sequencial ao Gate 2.4 confirmado pela pesquisadora.

Esta etapa fecha o pacote analítico da Etapa 2 com três tabelas finais para incorporação no capítulo 2 da tese e a leitura sintética dos contrastes. As tabelas e o relatório respondem ao briefing § 4.2.

### Os três cortes tabulares

1. **Comparativa geral (19 campos × 5 obras)**: `outputs/etapa2_artigos/tabela_comparativa_5_obras.{csv,tex}`. Gerada na Etapa 2.1 e mantida sem alteração. Versão LaTeX em formato `booktabs`, com densidade por 10.000 palavras e contagem absoluta entre parênteses.
2. **Campo militar refinado (5 obras)**: duas versões. A enxuta `tabela_militar_refinada_5_obras.tex` apresenta bruta e refinada figural, adequada à seção do capítulo 2. A detalhada `tabela_militar_refinado_5_obras_detalhada.tex` decompõe a subtração por categoria (descritivo-histórica, descritivo-bibliográfica, metalinguística, polêmica conceitual), apropriada ao apêndice metodológico. CSV equivalente em `tabela_militar_refinado_5_obras.csv`.
3. **Têxtil e topologia (5 obras)**: `tabela_textil_topologico_5_obras.{csv,tex}`. Mostra a inversão de densidade entre livros monográficos e artigos metateóricos no vocabulário têxtil-topológico.

### KWIC militar dos artigos (com categoria de desambiguação)

- **Clarifications 1996**, termo `allies`, categoria `metalinguistico` (gatilho: aspas=4, tar=2):
  > male- who wishes to grab power makes a network of **allies** and extend his power -doing some “networking” or “liaising” as
- **Clarifications 1996**, termo `enemies`, categoria `conceitual_debate` (gatilho: ismos=['Reflexivists', 'pre-relativist']):
  > anything to the world. Reflexivists as well as their pre-relativist **enemies** dream of substracting knowledge from the things in themselves. AT
- **Clarifications 1996**, termo `alliance`, categoria `descritivo_bibliografico` (gatilho: ano_parenteses+editora+autores_sequenciais):
  > Routledge, London, (1985). Ilya Prigogine et Isabelle Stengers, La nouvelle **alliance** métamorphose de la science, Gallimard/Bantam, Paris/New-York, (1979). Michel SERRES, HERMES.
- **Recalling ANT 1999**, termo `Wars`, categoria `descritivo_historico` (gatilho: casa 'Science Wars'):
  > which it derived, mentioned social constructivism and the recent Science **Wars** Clearly the treatment of the collectiveof scientificreality as a circulation

### Cinco exemplos KWIC têxtil-topológico em *Clarifications*

- **textil**, termo `tie`:
  > The second one is to grant them sociality and to **tie** them with the social fabric. The third one is to
- **textil**, termo `fabric`:
  > grant them sociality and to tie them with the social **fabric** The third one is to consider them as a semiotic
- **textil**, termo `filaments`:
  > of methaphors to describe essences: instead of surfaces one gets **filaments** (or rhyzomes in Deleuze’s parlance 197-). More precisely it is
- **textil**, termo `fibrous`:
  > societies cannot be described without recognizing them as having a **fibrous** thread-like, wiry, stringy, ropy, capillary character that is never captured
- **textil**, termo `thread`:
  > cannot be described without recognizing them as having a fibrous, **thread** wiry, stringy, ropy, capillary character that is never captured by

### Leitura sintética

Os três cortes tabulares consolidam três resultados articulados.

Primeiro: a densidade do campo militar bruto cai de 16,56-26,74 ocorrências por 10.000 palavras nos livros monográficos de Latour solo (*Science in Action* 1987 e *Pandora's Hope* 1999) para 3,82 e 8,06 nos dois artigos metateóricos. Após a desambiguação aplicada na Etapa 2.2, a contagem refinada figural cai a zero nos dois artigos. O vocabulário militar-industrial está presente nos artigos apenas em uso descritivo-histórico (`Science Wars`), descritivo-bibliográfico (`La nouvelle alliance` no rodapé), metalinguístico (Latour citando uso ingênuo da TAR que ele rebate) e de polêmica conceitual entre escolas teóricas (`pre-relativist enemies`).
Segundo: o vocabulário têxtil-topológico ocupa o terreno deixado pelo militar nos artigos. A densidade de `topologia` em *Clarifications* 1996 atinge 150,36 ocorrências por 10.000 palavras, mais de quatro vezes a densidade do mesmo campo em *Science in Action* 1987 (34,68/10k), e 5,5 vezes a de *Pandora's Hope* 1999 (27,58/10k). No *Recalling* 1999, a densidade topológica é de 104,75/10k. O campo `textil`, ausente no *Recalling*, atinge 49,69/10k em *Clarifications*, com a sequência paradigmática `fibrous, thread-like, wiry, stringy, ropy, capillary character` (página 76 do PDF interno) como passagem-citação central.
Terceiro: a cocorrência confirma que a malha argumentativa dos artigos é estruturada por `network`–`topologia`. Em *Clarifications* j=157, esse par tem 616 ocorrências conjuntas, contra 8 do par `militar`–`network` (relação cerca de 77 vezes menor). No *Recalling*, mesmo com o texto curto, `network`–`topologia` lidera a topologia da rede figurativa.
Esses três resultados sustentam a hipótese de divisão de trabalho metafórico por gênero textual proposta pelo briefing. O vocabulário militar-industrial é a marca lexical dominante dos livros monográficos solo (Latour 1987, 1999); recua quando Latour escreve metateoricamente para pares STS, e o vocabulário têxtil-topológico ocupa esse lugar. A coautoria com Woolgar em *Laboratory Life* 1986 apresenta densidade militar bruta (3,69/10k) em patamar próximo ao dos artigos, fato que merece registro etnográfico para o capítulo 2: a inflexão militar-industrial parece consolidar-se com Latour solo a partir de 1987.

### Limitações declaradas

1. A cobertura do *Recalling* é parcial (1.241 palavras de corpo, cerca de 80% do artigo), com as páginas 15 e 25 do volume excluídas por falha de OCR.
2. As contagens dos campos `textil` e `topologia` carregam polissemia. A validação amostral semântica da Etapa 2.6 (A/B/C) vai estabelecer a taxa de uso figural por campo e por obra.
3. A subtração por categoria de desambiguação dos livros está restrita à coluna `war`/`wars` (Etapa 1). As demais categorias (descritivo-bibliográfica, metalinguística, polêmica conceitual) não foram aferidas para os livros nesta etapa; foram aplicadas apenas aos artigos.
4. A janela de cocorrência apresentada como principal é a proporcional (2% do texto). A janela 200 está disponível como controle metodológico. A decisão final cabe à pesquisadora; ambas as versões estão geradas e versionadas.

### Outputs finais da Etapa 2 (resumo)

- `outputs/etapa2_artigos/tabela_comparativa_5_obras.{csv,tex}` (Etapa 2.1).
- `outputs/etapa2_artigos/tabela_comparativa_5_obras_n.csv` e `_freq.csv` (Etapa 2.1, granular).
- `outputs/etapa2_artigos/militar_classificacao_automatica.csv` (Etapa 2.2).
- `outputs/etapa2_artigos/tabela_militar_refinada_5_obras.tex` (Etapa 2.2, enxuta).
- `outputs/etapa2_artigos/tabela_militar_refinado_5_obras.csv` (Etapa 2.5, CSV detalhado).
- `outputs/etapa2_artigos/tabela_militar_refinado_5_obras_detalhada.tex` (Etapa 2.5, detalhada).
- `outputs/etapa2_artigos/tabela_textil_topologico_5_obras.{csv,tex}` (Etapa 2.5).
- `outputs/etapa2_artigos/cocorrencia_comparacao.md` (Etapa 2.4).
- `outputs/<artigo>/{csv,figuras,relatorios}/` (rotina por obra).
- `outputs/etapa2_artigos/relatorio_etapa2.md` (este arquivo, consolidado das cinco subetapas).

## Próximos passos (Gate 2.5 pendente)

A pesquisadora aprova as três tabelas e o relatório consolidado para incorporação ao capítulo 2 da tese. Pendências subsequentes:

- **Etapa 2.6**: validação amostral semântica A/B/C análoga à da Etapa 1, aplicada aos trechos figurativos dos artigos. A amostra dos artigos é menor em volume absoluto (n total = 24 no *Recalling*, n total = 279 no *Clarifications*), mas o protocolo é idêntico ao da Etapa 1.
- **Pendência aberta para Etapa 2-bis**: caso a pesquisadora obtenha PDF nativo do *Recalling*, reanálise pode estender a cobertura para o artigo integral e oferecer contagem mais robusta. A contagem atual cobre 80% do artigo, com a passagem-chave dos pp. 19-20 sobre a contaminação do vocabulário integralmente incluída.
