# Relatório consolidado: análise de figurações em Latour, 1986-1999

**Autora:** Juliane Helanski
**Data de consolidação:** 15 de maio de 2026
**Versão:** 1.0 (fonte autoritativa, substitui os relatórios parciais como referência única)
**Repositório:** `julianehelanski/analise_figuracoes`

---

## Sumário executivo

A hipótese central da análise, **divisão de trabalho metafórico por gênero textual entre livros monográficos solo de Latour e seus artigos metateóricos para pares STS, foi confirmada e reforçada pelas três etapas do projeto**. Os livros monográficos (*Science in Action* 1987 e *Pandora's Hope* 1999) mobilizam o vocabulário militar-industrial em densidades de 16 a 26 ocorrências por 10.000 palavras como tropo descritivo da prática científica; os dois artigos metateóricos (*Clarifications* 1996 e *On Recalling ANT* 1999) recuam esse vocabulário a zero figural quando a leitura é restringida ao tropo da prática científica, e o vocabulário têxtil-topológico ocupa o terreno deixado. A Etapa 2-bis, reanálise do *Recalling* a partir de TXT integral fornecido após a Etapa 2.6, sustenta esse achado central em corpus que cobre 100% do artigo, contra os 25,3% (e não os ~80% que o relatório original da Etapa 2 declarou, em premissa errada) do corpus parcial inicial.

A pergunta orientadora opera sobre cinco obras de Latour publicadas entre 1986 e 1999. As três etapas estão concluídas. As pendências abertas são pontuais e estão declaradas na seção 8.

---

## 1. Objeto e perguntas

A análise rastreia o vocabulário figurativo de Bruno Latour em cinco obras publicadas em treze anos:

| Obra | Ano | Gênero | Palavras de corpo (convenção `split`) |
|---|---:|---|---:|
| *Laboratory Life* (com S. Woolgar) | 1986 | livro (2ª edição) | 105.749 |
| *Science in Action* | 1987 | livro | 139.861 |
| *Pandora's Hope* | 1999 | livro | 128.001 |
| *On Actor-Network Theory: A Few Clarifications* | 1996 | artigo (*Soziale Welt*) | 7.848 |
| *On Recalling ANT* | 1999 | artigo (Law e Hassard, eds.) | 4.825 [a] |

[a] *Recalling ANT*: 4.825 palavras é a contagem da Etapa 2-bis sobre o TXT integral (pp. 15-25 do volume). A Etapa 2 original operou com corpus parcial de 1.241 palavras (5 das 11 páginas, 25,3% de cobertura efetiva; vide § 3.6). Para campos figurativos cujas ocorrências caíam justamente no estrato excluído (`circulating_reference`, `translation`, `inscription`, `articulation`, `textil`), o efeito é qualitativo, não apenas quantitativo: campos ausentes do corpus antigo passam a comparecer no integral.

As perguntas que orientam o conjunto:

- Como o vocabulário figurativo se distribui ao longo da trajetória latouriana entre 1986 e 1999?
- A figuração militar-industrial é vocabulário descritivo geral da escrita latouriana ou figuração de registro situado? Caso seja situada, o registro é o da descrição da prática (livros monográficos) ou o da metalinguagem sobre a teoria (artigos metateóricos)?
- Em que medida o vocabulário têxtil-topológico, que reivindico como herança feminista mobilizada por Haraway, é também mobilizado pelo próprio Latour, e em que registro?

---

## 2. Catálogo lexical

Trabalho com dezenove campos figurativos. Dezessete vêm do `campos_lexicais/catalogo_termos.yaml` consolidado na Etapa 1; dois (`textil` e `topologia`) foram acrescentados na Etapa 2 como arquivos de adição (`campos_lexicais/latour_textil_en_etapa2_adicoes.txt` e `_topologia_en_etapa2_adicoes.txt`), sem alterar o YAML, conforme o briefing § 3.1 da Etapa 2.

| Campo | Variantes rastreadas | Proveniência |
|---|---|---|
| `inscription` | inscription, inscriptions, inscription device, inscription devices, literary inscription | Etapa 1 |
| `immutable_mobile` | immutable mobile, immutable mobiles | Etapa 1 |
| `black_box` | black box, black-box, black boxes, blackbox, blackboxing, black-boxing | Etapa 1 |
| `centre_of_calculation` | centre/center of calculation e plurais | Etapa 1 |
| `actor_network` | actor-network, actor network, actant, actants | Etapa 1 |
| `translation` | translation, translations, translate, translates, translated | Etapa 1 |
| `trial_of_strength` | trial of strength, trials of strength | Etapa 1 |
| `factish` | factish, factishes | Etapa 1 |
| `circulating_reference` | circulating reference, circulating references | Etapa 1 |
| `articulation` | articulation, articulations, articulate, articulated | Etapa 1 |
| `construction` | construction, constructed, constructing, social construction | Etapa 1 |
| `proposition` | proposition, propositions | Etapa 1 |
| `network` | network, networks, networking | Etapa 1 |
| `agonistic` | agonistic, agonistics, agonistic field | Etapa 1 |
| `enrollment` | enrollment, enrolment, enroll, enrol, enrolled | Etapa 1 |
| `spokesperson` | spokesperson, spokespersons, spokesman, spokesmen, spokeswoman | Etapa 1 |
| `militar` | 64 variantes em inglês cobrindo ally/enemy/recruit/mobilise/battle/war/conquer/victory/defeat/troops/attack/defend/fortress/weapon/soldier/siege e flexões; exclusões `best ally`, `natural ally`, `first attack`, `asthma/heart/panic attack`, `battle of ideas` | Etapa 1 (consolidado em 14/05/2026) |
| `textil` | thread, weave, knot, tangle, fiber/fibre, fibrous, filament, string, wire, rope, lace, plait, twist, net, fabric, texture, capillary e flexões (61 variantes) | Etapa 2 (acréscimo) |
| `topologia` | fluid, surface, node, connection, topology, flat, fold, locus, trajectory, flow, circulation, path, grid, mesh, boundary, inside, outside, proximity, scale, plane e flexões (43 variantes; `network` permanece no grupo homônimo do YAML para não duplicar) | Etapa 2 (acréscimo) |

O acréscimo de `textil` e `topologia` é decisão metodológica reflexiva que registro como parte do achado: a leitura qualitativa dos dois artigos metateóricos revelou um vocabulário denso de imagens têxteis (fibrous, thread-like, woven, weaving, tied, knotted) e topológicas (filaments, surfaces, fluids, flat, folded, circulation) que o catálogo da Etapa 1, organizado em torno do vocabulário conceitual canônico da TAR, não capturava. Acrescentei os dois campos como arquivos de adição separados para preservar o catálogo da Etapa 1 intocado e tornar o gesto auditável. Esse acréscimo é parte do que a análise mostra: o vocabulário figurativo central do *Clarifications* não estava no catálogo até que a leitura qualitativa o tornasse visível, em um movimento que faz do método parte do argumento da tese.

---

## 3. Procedimento

### 3.1. Extração e normalização

**Três livros (Etapa 1).** Extraí o texto a partir dos PDFs sincronizados em pasta privada do Google Drive (referenciada em `.env` na variável `CORPUS_PDF_PATH`), via `scripts/01_extract_text.py` (`pdftotext -layout`, com fallback para `pdfminer.six`). O texto cru fica em `corpus/txt/<id>.txt` como artefato auditável. Normalizo em seguida com `scripts/01b_normalize_text.py`, que aplica seis operações documentadas no Adendo 1 das decisões metodológicas (remoção de soft hyphens U+00AD, de-hifenização de fim de linha, remoção de marcadores `((NN))` injetados pelo conversor, descarte de cabeçalhos espaçados, normalização NFKC com aspas e travessões, substituição de replacement chars por espaço). O resultado normalizado fica em `corpus/txt_norm/<id>.txt`, base de toda a análise lexicométrica.

**Dois artigos metateóricos (Etapa 2).** Os `.txt` chegaram já normalizados, em sessão de chat anterior fora do pipeline canônico, conforme briefing § 3.3. O fluxo Drive → sincronização local → leitura via `.env` não se aplica aqui (a normalização aconteceu fora). Os arquivos foram depositados em `corpus/txt_norm/latour_1996_clarifications_en.txt` e `corpus/txt_norm/latour_1999_recalling_en.txt`, com cabeçalhos `#` registrando origem, paginação e nota de estrutura. O *Recalling* da Etapa 2 cobria as páginas pares de um zip de OCR (pp. 16, 18, 20, 22, 24 do volume), com as páginas ímpares descartadas por OCR truncado.

**TXT integral do *Recalling* (Etapa 2-bis).** Em sessão de 15 de maio de 2026, depositei em `corpus/txt_fornecido/latour_1999_recalling_nativo.txt` o `.txt` integral do artigo (pp. 15-25 do volume), obtido por canais de acesso institucional. Apliquei normalização simétrica à da Etapa 1 (5 soft hyphens U+00AD, 11 caracteres de controle ASCII de baixa ordem, 32 reconstituições de hifenização EOL; CRLF/LF tratado transparentemente pela leitura como texto). Detalhamento em `outputs/etapa2bis_recalling/normalizacao_aplicada.md`. O arquivo normalizado final ficou em `corpus/txt_norm/latour_1999_recalling_bis.txt`, lado a lado com o `.txt` antigo, que permanece intocado para auditoria. Hashes SHA-256 dos dois arquivos no Anexo C.

A tabela de qualidade da extração, consolidando as cinco obras mais a versão bis do *Recalling*:

| Obra | Páginas | Palavras | Qualidade global |
|---|---:|---:|---|
| `latour_woolgar_1986_lab_life_en` | 296 | 105.749 | boa |
| `latour_1987_science_action_en` | 314 | 139.861 | boa |
| `latour_1999_pandora_en` | 337 | 128.001 | boa |
| `latour_1996_clarifications_en` | 14 | 7.848 | boa, com pequenos artefatos de OCR |
| `latour_1999_recalling_en` (Etapa 2) | 5 | 1.241 | parcial, com colagem de OCR |
| `latour_1999_recalling_bis` (Etapa 2-bis) | 11 | 4.825 | boa, TXT nativo |

Fonte: `corpus/qualidade_extracao.csv`.

### 3.2. Catalogação, contagem KWIC, densidade

`scripts/02_kwic.py` percorre cada `.txt` normalizado e procura ocorrências de cada variante do catálogo (mais arquivos de adição quando `--adicoes` é passado), com regex tolerante a quebras de linha, hífen opcional via `[-\s]?` e equivalência entre aspas tipográficas e ASCII. Janela KWIC fixada em **±10 palavras** desde a Etapa 1 (decisão de 13/05/2026, seção 3 das decisões metodológicas). A saída é uma linha por ocorrência em `outputs/<obra>/csv/kwic.csv`, com `contexto_antes`, `trecho_central`, `contexto_depois`, `pagina`, `posicao_no_texto` e flag de exclusão.

`scripts/03_frequencies.py` agrega o `kwic.csv` em frequências absolutas e relativas (ocorrências por 10.000 palavras), com `palavras_total` lido de `corpus/qualidade_extracao.csv`. A normalização por 10.000 permite comparar obras de tamanhos distintos: as três obras monográficas têm entre 106 e 140 mil palavras, os artigos têm entre 1.241 e 7.848.

### 3.3. Desambiguação por categorias

Na Etapa 2.2, defini cinco categorias para classificar as ocorrências do campo `militar`:

- `descritivo_historico`: colocação com objeto histórico (`Science Wars`, `World War`, `Cold War`, `Franco-Prussian War`, `phony war`, `War and Peace`, `Ministry of War`, `Hundred Years' War`, `Thirty Years' War`, `Great War`).
- `descritivo_bibliografico`: ocorrência em referência bibliográfica ou em título de obra citada. Gatilho: ≥2 entre ano em parênteses, editora conhecida (Routledge, Blackwell, Harvard, Princeton, Gallimard, Bantam, Oxford, Cambridge UP, Sage, Seuil, Minuit, La Découverte, PUF) e nomes próprios sequenciais.
- `metalinguistico`: Latour cita o próprio vocabulário da TAR. Gatilho: ≥2 aspas curvas/retas na janela junto a ≥1 termo da TAR (association, translation, passage point, actor-network, enrollment, actant, actor, network e variantes, mediator, displacement, AT, ANT), ou indicador citacional explícito (`vocabulary`, `the word`, `the notion`, `the term`, `the expression of`, `let us abandon`, `coffin`, `so-called`, `misunderstanding`, `misrepresented`) com ≥2 termos da TAR.
- `conceitual_debate`: descrição de polêmica entre escolas teóricas. Gatilho: ≥2 palavras terminadas em `-ist`, `-ists`, `-ism`, `-isms` na janela.
- `figurativo`: default sem gatilho. Uso figural do vocabulário militar como tropo da prática científica. Esta é a categoria que **conta** para a contagem refinada figural; as outras quatro são subtraídas da bruta.

Implementação em `scripts/15_etapa2_desambiguar_militar.py`. A planilha de classificação dos artigos segue o formato de `refinamento/war_pandora_classificacao.csv` (Etapa 1, refinamento `war/wars` em *Pandora's Hope*).

### 3.4. Cocorrência

`scripts/05_cooccurrence.py` constrói matriz de cocorrência grupo × grupo a partir do `kwic.csv` da obra, usando janela em palavras aproximada por caracteres (média 5,5 caracteres/palavra). Para os livros monográficos da Etapa 1, janela única de 200 palavras. Para os artigos da Etapa 2, duas configurações coexistem via argumento `--sufixo`: janela 200 (controle direto para comparação com os livros) e janela proporcional 2% das palavras totais (157 para *Clarifications*; 25 para *Recalling* da Etapa 2; **97** para *Recalling* da Etapa 2-bis sobre o corpus integral). A janela proporcional foi adotada como recomendada para a tese porque padroniza a fração textual da janela entre obras de tamanhos distintos, ao custo de tornar a comparação direta com os livros indireta; a janela 200 fica disponível como controle metodológico.

### 3.5. Validação amostral semântica A/B/C

`scripts/18_etapa2_validacao_amostral.py` (Etapa 2.6) e `scripts/21_etapa2bis_validacao_migracao.py` (Etapa 2-bis) geram planilhas de validação amostral em três camadas para os quatro campos centrais do argumento têxtil-topológico (`textil`, `topologia`, `network`, `actor_network`). O campo `militar` está fora porque já foi 100% desambiguado em registro autom (4/4 ocorrências nos artigos da Etapa 2; 2/2 na Etapa 2-bis).

Protocolo das camadas, definido na Etapa 2.6 (decisão registrada em `docs/decisoes_metodologicas.md` § 11 da Etapa 2):

- **Camada A — top-densidade.** Cinco ocorrências por campo cuja janela KWIC tem o maior número de termos do mesmo campo lexical na vizinhança imediata. Captura passagens onde o campo aparece de modo concentrado.
- **Camada B — aleatória.** Cinco ocorrências aleatórias por campo, com `seed=42`. Representa o fundo do campo, sem viés de densidade.
- **Camada C — variantes raras.** Cinco ocorrências por campo cuja variante (`termo_encontrado`) é das menos frequentes. Heurística para captar polissemia e uso periférico.

Quando o campo tem menos de 15 ocorrências, a amostra é exaustiva. A pesquisadora preenche manualmente três colunas por linha: `uso_figural` (`sim` / `parcial` / `nao`), `subcategoria` (texto livre; sugestões: `tecnico`, `polissemia`, `descritivo`, `metalinguistico`, e a `definicao_operacional` cunhada durante o preenchimento), e `comentario` (registro etnográfico).

### 3.6. A descoberta tardia: cobertura real do *Recalling* na Etapa 2

A Etapa 2-bis revelou um achado metodológico que organizo aqui em três parágrafos.

Primeiro: o briefing da Etapa 2 assumiu, em sua premissa quantitativa preliminar, que o artigo *On Recalling ANT* integral tinha em torno de 1.500 palavras. Essa premissa derivava do entendimento, que se mostrou equivocado, de que as 1.241 palavras processáveis do corpus da Etapa 2 representavam cerca de 80% do artigo. O número 1.500 nunca foi verificado contra a edição publicada do artigo; surgiu como cota inferida do número 1.241 e da estimativa intuitiva de cobertura. A inferência estava errada na premissa, não na contagem.

Segundo: o artigo ocupa as páginas 15-25 do volume Law e Hassard 1999, *Actor Network Theory and After*, publicado pela Blackwell para *The Sociological Review*. Onze páginas. A densidade típica em *Sociological Review* é de aproximadamente 440 palavras por página de texto principal, o que dá uma estimativa razoável de 4.840 palavras totais. O TXT integral fornecido na Etapa 2-bis tem 4.825 palavras após normalização, alinhado com a estimativa. O corpus parcial da Etapa 2 cobriu, na realidade, **as cinco páginas pares do zip de OCR** (pp. 16, 18, 20, 22, 24 do volume), mais alguma fração truncada das ímpares; em palavras, 1.241 sobre 4.825 dá **25,3% de cobertura efetiva**. As 1.241 palavras estavam restritas, ainda, a partes das cinco páginas retidas (a contagem média foi de ~245 palavras por página retida contra a média esperada de ~440, sinal de truncamento adicional dentro dos blocos pares).

Terceiro: a descoberta é parte do registro etnográfico do projeto. Não a tratei como falha a esconder, e o relatório original da Etapa 2 (em `outputs/etapa2_artigos/relatorio_etapa2.md`) permanece intocado como artefato auditável de uma sessão que operou sobre premissa equivocada. O relatório da Etapa 2-bis (em `outputs/etapa2bis_artigos/relatorio_etapa2bis.md`) declara a correção explicitamente, e este relatório consolidado a registra como parte do que a análise mostrou: a cadeia mim → OCR → pipeline normalizou um pedaço do *Recalling* que era menor do que eu pensava, e a aferição correta só veio quando a Etapa 2-bis tornou o estrato excluído acessível.

---

## 4. Trajetória latouriana 1986-1999 nas três obras monográficas

A Etapa 1 analisou os três livros sob janela KWIC ±10 e os dezessete campos figurativos do catálogo (sem `textil` e `topologia`, acrescidos depois na Etapa 2). O resultado consolida-se na tabela seguinte, da matriz grupo × obra, em frequência por 10.000 palavras com contagem absoluta entre parênteses.

| Grupo | *Lab Life* 1986 | *Sci. in Action* 1987 | *Pandora's Hope* 1999 | Obras (n/3) |
|---|---:|---:|---:|---:|
| `inscription` | 11,82 (125) | 4,43 (62) | 1,09 (14) | 3/3 |
| `construction` | 19,29 (204) | 3,79 (53) | 4,84 (62) | 3/3 |
| `network` | 4,26 (45) | 9,08 (127) | 2,73 (35) | 3/3 |
| `translation` | 0,28 (3) | 5,58 (78) | 5,47 (70) | 3/3 |
| `black_box` | 0,95 (10) | 9,58 (134) | 1,33 (17) | 3/3 |
| `enrollment` | 0,09 (1) | 3,15 (44) | 0,94 (12) | 3/3 |
| `proposition` | 0,47 (5) | 0,36 (5) | 3,20 (41) | 3/3 |
| `militar` | 3,69 (39) | **26,74 (374)** | **16,56 (212)** | 3/3 |
| `actor_network` | 0 | 1,22 (17) | 2,42 (31) | 2/3 |
| `immutable_mobile` | 0 | 0,29 (4) | 0,23 (3) | 2/3 |
| `centre_of_calculation` | 0 | 1,36 (19) | 0,31 (4) | 2/3 |
| `spokesperson` | 0,09 (1) | 3,29 (46) | 0 | 2/3 |
| `articulation` | 0 | 0,29 (4) | 4,14 (53) | 2/3 |
| `trial_of_strength` | 0 | 1,43 (20) | 0 | 1/3 |
| `factish` | 0 | 0 | 4,14 (53) | 1/3 |
| `circulating_reference` | 0 | 0 | 1,41 (18) | 1/3 |
| `agonistic` | 3,03 (32) | 0 | 0 | 1/3 |

Fonte: `outputs/trajetoria_latour_1986_1999.csv` (gerado por `scripts/07_trajectory.py`); tabela em LaTeX em `outputs/latex/trajetoria_latour_1986_1999.tex`.

O pico do campo `militar` em *Science in Action* (26,74/10k) é a maior densidade do livro inteiro entre os dezessete campos catalogados, ultrapassando `black_box` (9,58), `network` (9,08), `translation` (5,58) e `inscription` (4,43). Em *Pandora's Hope*, a densidade militar continua alta (16,56/10k). Em *Laboratory Life*, fica em patamar muito baixo (3,69/10k), próximo do patamar que vou encontrar nos artigos metateóricos. O contraste entre 1986 e os livros monográficos solo de 1987 e 1999 é o achado etnográfico complementar sobre coautoria: a inflexão militar-industrial consolida-se com Latour solo a partir de 1987.

O deslocamento entre `agonistic` (3,03/10k em 1986; zero em 1987 e 1999) e `trial_of_strength` (zero em 1986; 1,43/10k em 1987; zero em 1999) opera como deslocamento substituticional dentro do mesmo campo conceitual: o vocabulário agonístico de 1986 é reformulado em 1987 como "prova de força" e desaparece como termo cunhado em 1999, mas o vocabulário militar-industrial que o sustenta permanece em densidade alta.

A figura seguinte mostra a comparação direta dos dezessete campos nas três obras, com o campo militar destacado:

![Comparação de frequências entre as três obras, dezessete campos figurativos, densidade por 10.000 palavras, campo militar destacado. Fonte: `outputs/passo4/figuras/comparacao_frequencias_tres_obras.png`, gerada por `scripts/11_passo4_graficos.py` em 14/05/2026.](figuras/comparacao_frequencias_tres_obras.png)

O painel de rankings absolutos por obra:

![Painel de rankings absolutos dos campos figurativos por obra, contagem absoluta. Fonte: `outputs/passo4/figuras/frequencia_grupos_tres_obras_painel.png`, gerada por `scripts/11_passo4_graficos.py`.](figuras/frequencia_grupos_tres_obras_painel.png)

A janela deslizante mostra a densidade do campo `militar` ao longo dos dois livros monográficos solo:

![Densidade do campo militar ao longo de *Science in Action* (1987) e *Pandora's Hope* (1999), em janela deslizante. Fonte: `outputs/passo4/figuras/densidade_militar_sia_pandora.png`, gerada por `scripts/11_passo4_graficos.py`.](figuras/densidade_militar_sia_pandora.png)

### 4.1. Refinamento do campo militar nos livros (desambiguação `war/wars`)

Apliquei na Etapa 1 (passo 1 do refinamento, 14/05/2026) desambiguação manual do termo `war/wars` nas três obras, distinguindo uso descritivo-histórico (objetos nomeados como `Science Wars`, `World War`, `Cold War`, `Franco-Prussian War`, *War and Peace* de Tolstói, narrativas históricas da Segunda Guerra centradas em Joliot e Szilard, *Ministry of War* etc.) do uso figurativo do vocabulário militar como tropo da prática científica. A planilha está em `refinamento/war_pandora_classificacao.csv`; a tabela consolidada em `refinamento/militar_refinado_tres_obras.csv` e `refinamento/tabela_militar_refinada.tex`.

A contagem refinada figural para os três livros:

| Obra | Palavras | Bruta n | Bruta /10k | Refinada n | Refinada /10k |
|---|---:|---:|---:|---:|---:|
| *Laboratory Life* (1986) | 105.749 | 39 | 3,69 | 37 | 3,50 |
| *Science in Action* (1987) | 139.861 | 374 | 26,74 | 364 | 26,03 |
| *Pandora's Hope* (1999) | 128.001 | 212 | 16,56 | **156** | **12,19** |

Fonte: `refinamento/militar_refinado_tres_obras.csv`.

O refinamento subtrai pouco em *Science in Action* (10 ocorrências, queda de 2,7%) e em *Laboratory Life* (2 ocorrências, queda de 5,1%). Em *Pandora's Hope*, a subtração é mais densa: 56 ocorrências (queda de 26,4%), concentradas em duas séries: as menções a `Science Wars` (que dão o tom da introdução do livro, "News from the Trenches of the Science Wars"), e as narrativas históricas da Segunda Guerra Mundial nos capítulos sobre Joliot e Szilard. Mesmo após o refinamento, *Pandora's Hope* mantém densidade militar figural de 12,19/10k, em patamar alto comparado ao das outras obras do corpus.

Frequência refinada dos grupos em *Science in Action* e *Pandora's Hope* (com `militar` substituído pela versão refinada):

![Frequência dos grupos figurativos em *Science in Action* (1987), versão refinada do campo militar. Fonte: `outputs/passo4/figuras/frequencia_grupos_sia_refinada.png`.](figuras/frequencia_grupos_sia_refinada.png)

![Frequência dos grupos figurativos em *Pandora's Hope* (1999), versão refinada do campo militar. Fonte: `outputs/passo4/figuras/frequencia_grupos_pandora_refinada.png`.](figuras/frequencia_grupos_pandora_refinada.png)

### 4.2. Cocorrência nos três livros

As redes de cocorrência (janela 200 palavras) por obra:

![Rede de cocorrência figural em *Laboratory Life* (1986), janela 200 palavras, nós dimensionados por frequência, arestas pela força de cocorrência, layout *force-directed* com `seed=42`. Fonte: `outputs/latour_woolgar_1986_lab_life_en/figuras/rede_cocorrencia.png`.](figuras/rede_cocorrencia_lab_life.png)

![Rede de cocorrência figural em *Science in Action* (1987), janela 200 palavras, layout *force-directed* `seed=42`. Fonte: `outputs/latour_1987_science_action_en/figuras/rede_cocorrencia.png`.](figuras/rede_cocorrencia_sia.png)

![Rede de cocorrência figural em *Pandora's Hope* (1999), janela 200 palavras, layout *force-directed* `seed=42`. Fonte: `outputs/latour_1999_pandora_en/figuras/rede_cocorrencia.png`.](figuras/rede_cocorrencia_pandora.png)

### 4.3. Postscript da segunda edição de *Laboratory Life* (1986)

A segunda edição de *Laboratory Life* (Princeton, 1986) contém um pós-escrito (pp. 274-287, 5.976 palavras) em que Latour e Woolgar justificam a remoção da palavra "Social" do subtítulo. O pós-escrito é, ele próprio, registro de deslocamento figurativo. A tabela seguinte mostra a distribuição dos quatro campos com ocorrências no Postscript:

| Campo figurativo | No Postscript | No livro | % no PS | Freq./10k (PS) |
|---|---:|---:|---:|---:|
| `construction` | 8 | 204 | 3,9% | 13,39 |
| `black_box` | 1 | 10 | 10,0% | 1,67 |
| `inscription` | 1 | 125 | 0,8% | 1,67 |
| `enrollment` | 1 | 1 | 100,0% | 1,67 |

Fonte: `outputs/latex/postscript_1986_figuracoes.tex`, gerada em 14/05/2026 a partir de `outputs/latour_woolgar_1986_lab_life_en/csv/kwic.csv`.

O Postscript não recupera densidade militar (zero ocorrências), confirmando que o vocabulário agonístico-militar de 1986 não é tematizado retrospectivamente pelos autores na revisão da segunda edição.

### 4.4. Três passagens-âncora dos livros monográficos

As três passagens que aparecem como marcos do registro figural militar nos livros estão em `outputs/passo4/sequencia_exercito_ciencia.md` (curadoria temática manual; arquivo no `.gitignore` por reprodução textual de trechos extensos). Reproduzo três marcas em prosa contida:

1. Em *Laboratory Life* (1986), Latour e Woolgar abrem um trecho com `"Let us consider an analogy with war..."`. A figuração militar entra explicitamente como **analogia**.
2. Em *Science in Action* (1987), Latour escreve `"is not a metaphor, it is literally the mutual problem of winning..."`. A figuração militar passa de analogia a **literalidade**: a prática científica é literalmente um problema de "winning".
3. Em *Pandora's Hope* (1999), na introdução, Latour escreve `"Every one of the weapons used in the science wars..."`. A figuração militar é agora vocabulário de **autodescrição** do que o livro faz: o autor já não precisa justificá-la como analogia ou literalidade; mobiliza-a como vocabulário disponível.

A trajetória das três passagens é a do gesto figurativo: analogia (1986), identificação literal (1987), vocabulário disponível (1999). É a trajetória que o capítulo 2 da minha tese mobiliza como base empírica para a leitura do registro figural-militar como marca lexical situada da escrita latouriana.

---

## 5. Os artigos metateóricos: deslocamento de registro

### 5.1. Por que estender a análise

A leitura qualitativa dos dois artigos metateóricos centrais que Latour escreve no mesmo período (*Clarifications* 1996, *Soziale Welt*; *On Recalling ANT* 1999, em Law e Hassard) sugeriu uma divisão de trabalho metafórico entre dois gêneros textuais. Nos livros, o vocabulário militar-industrial domina; nos artigos, recua sensivelmente, e o vocabulário têxtil-topológico ocupa o terreno. A Etapa 2 submete essa hipótese qualitativa à mesma contagem sistemática aplicada aos livros, preempetando a objeção previsível da banca ("e os artigos? a teoria ator-rede se formula em artigos tanto quanto em livros"), e dando ao argumento sobre a especificidade da figuração militar-industrial o contraste empírico que ele precisa.

### 5.2. Acréscimo dos campos têxtil e topologia

O catálogo da Etapa 1 não tinha grupos para os vocabulários têxtil e topológico. Acrescentei-os como arquivos de adição na Etapa 2 (`campos_lexicais/latour_textil_en_etapa2_adicoes.txt` e `_topologia_en_etapa2_adicoes.txt`), sem alterar o YAML do catálogo, conforme registrado na seção 5 das decisões metodológicas da Etapa 2. O acréscimo é decisão metodológica que registro como parte do achado: a leitura qualitativa dos artigos é o que tornou esses campos visíveis para a contagem; a contagem não os teria revelado.

### 5.3. Apresentação Etapa 2 e Etapa 2-bis lado a lado para o *Recalling*

A Etapa 2 original processou o *Recalling* sobre corpus parcial de 1.241 palavras (25,3% do artigo, em premissa errada que declarava ~80%; vide § 3.6). A Etapa 2-bis reprocessou o mesmo artigo sobre TXT integral de 4.825 palavras (100% do artigo), mantendo os outputs da Etapa 2 intocados em paralelo. Apresento daqui em diante os dados das duas versões lado a lado, com nota explicitando que o leitor pode comparar diretamente o efeito do estrato antes excluído sobre cada campo. Para *Clarifications*, a coluna é única, porque a Etapa 2-bis não reextraiu esse artigo (não havia razão para fazê-lo: a Etapa 2 já cobriu o artigo integral, sem ressalva).

### 5.4. Tabela comparativa geral, dezenove campos × cinco obras

| Campo | *Lab Life* 1986 | *Sci. Action* 1987 | *Pandora* 1999 | *Clarifications* 1996 | *Recalling* E2 1999 | *Recalling* E2-bis 1999 |
|---|---:|---:|---:|---:|---:|---:|
| Palavras | 105.749 | 139.861 | 128.001 | 7.848 | 1.241 | 4.825 |
| `inscription` | 11,82 (125) | 4,43 (62) | 1,09 (14) | -- | -- | 2,07 (1) |
| `immutable_mobile` | -- | 0,29 (4) | 0,23 (3) | -- | -- | -- |
| `black_box` | 0,95 (10) | 9,58 (134) | 1,33 (17) | -- | -- | -- |
| `centre_of_calculation` | -- | 1,36 (19) | 0,31 (4) | 1,27 (1) | -- | -- |
| `actor_network` | -- | 1,22 (17) | 2,42 (31) | 24,21 (19) | 16,12 (2) | 18,65 (9) |
| `translation` | 0,28 (3) | 5,58 (78) | 5,47 (70) | 5,10 (4) | -- | 4,15 (2) |
| `trial_of_strength` | -- | 1,43 (20) | -- | -- | -- | -- |
| `factish` | -- | -- | 4,14 (53) | -- | -- | -- |
| `circulating_reference` | -- | -- | 1,41 (18) | -- | -- | 4,15 (2) |
| `articulation` | -- | 0,29 (4) | 4,14 (53) | -- | -- | 2,07 (1) |
| `construction` | 19,29 (204) | 3,79 (53) | 4,84 (62) | 2,55 (2) | 8,06 (1) | 4,15 (2) |
| `proposition` | 0,47 (5) | 0,36 (5) | 3,20 (41) | -- | -- | -- |
| `network` | 4,26 (45) | 9,08 (127) | 2,73 (35) | 118,50 (93) | 56,41 (7) | 58,03 (28) |
| `agonistic` | 3,03 (32) | -- | -- | -- | -- | -- |
| `enrollment` | 0,09 (1) | 3,15 (44) | 0,94 (12) | -- | -- | -- |
| `spokesperson` | 0,09 (1) | 3,29 (46) | -- | -- | -- | -- |
| `militar` | **3,69 (39)** | **26,74 (374)** | **16,56 (212)** | **3,82 (3)** | **8,06 (1)** | **4,15 (2)** |
| `textil` | 1,23 (13) | 7,94 (111) | 8,20 (105) | 49,69 (39) | -- | 2,07 (1) |
| `topologia` | 13,81 (146) | 34,68 (485) | 27,58 (353) | 150,36 (118) | 104,75 (13) | 99,48 (48) |

Fontes: `outputs/etapa2_artigos/tabela_comparativa_5_obras_freq.csv` (livros + *Clarifications* + *Recalling* E2), `outputs/etapa2bis_artigos/tabela_comparativa_5_obras_bis_freq.csv` (coluna *Recalling* E2-bis).

A leitura desta tabela é o coração do argumento. Nos livros monográficos solo (*Science in Action* e *Pandora's Hope*), o campo `militar` aparece em densidades de 16 a 26 por 10k. Em *Laboratory Life* (coautoria com Woolgar) e nos dois artigos metateóricos, fica em densidades de 3 a 8 por 10k. Os campos `textil` e `topologia` operam em sentido inverso: dentro dos artigos metateóricos, atingem densidades muito altas (49,69 e 150,36 em *Clarifications*; zero e 99,48 em *Recalling* bis). O contraste **bruta** já mostra o deslocamento de registro; a refinada figural, abaixo, confirma e reforça.

### 5.5. Tabela militar refinada, cinco obras

| Obra | Palavras | Bruta n | Bruta /10k | Refinada n | Refinada /10k |
|---|---:|---:|---:|---:|---:|
| *Laboratory Life* (1986) | 105.749 | 39 | 3,69 | 37 | 3,50 |
| *Science in Action* (1987) | 139.861 | 374 | 26,74 | 364 | 26,03 |
| *Pandora's Hope* (1999) | 128.001 | 212 | 16,56 | 156 | 12,19 |
| *Clarifications* (1996) | 7.848 | 3 | 3,82 | **0** | **0,00** |
| *Recalling ANT* E2 (1999) | 1.241 | 1 | 8,06 | **0** | **0,00** |
| *Recalling ANT* E2-bis (1999) | 4.825 | 2 | 4,15 | **0** | **0,00** |

Fontes: `outputs/etapa2_artigos/tabela_militar_refinada_5_obras.tex` (Etapa 2, com *Recalling* E2), `outputs/etapa2bis_artigos/tabela_militar_refinada_5_obras_bis.tex` (Etapa 2-bis, com *Recalling* bis).

A contagem refinada figural cai a zero nos dois artigos, em ambas as versões do *Recalling*. O argumento da divisão de trabalho metafórico está sustentado: o vocabulário militar-industrial está empiricamente ausente como tropo da prática científica nos dois artigos metateóricos. A Etapa 2-bis amplia a base empírica desse achado: as duas ocorrências brutas do *Recalling* integral (em vez da uma da Etapa 2) confirmam que mesmo expondo o artigo ao volume três vezes maior do estrato antes excluído, o registro permanece não-figural.

### 5.6. Tabela têxtil-topológica, cinco obras

| Obra | Palavras | `textil` /10k (n) | `topologia` /10k (n) |
|---|---:|---:|---:|
| *Laboratory Life* (1986) | 105.749 | 1,23 (13) | 13,81 (146) |
| *Science in Action* (1987) | 139.861 | 7,94 (111) | 34,68 (485) |
| *Pandora's Hope* (1999) | 128.001 | 8,20 (105) | 27,58 (353) |
| *Clarifications* (1996) | 7.848 | **49,69 (39)** | **150,36 (118)** |
| *Recalling ANT* E2 (1999) | 1.241 | -- (0) | 104,75 (13) |
| *Recalling ANT* E2-bis (1999) | 4.825 | 2,07 (1) | **99,48 (48)** |

Fontes: `outputs/etapa2_artigos/tabela_textil_topologico_5_obras.tex` (livros + *Clarifications* + *Recalling* E2), `outputs/etapa2bis_artigos/tabela_textil_topologico_5_obras_bis.tex` (coluna *Recalling* E2-bis).

A inversão entre livros e artigos no campo `topologia` aparece com nitidez: nos livros, densidades de 13 a 34 por 10k; em *Clarifications*, 150,36; em *Recalling* bis, 99,48 (ordem de grandeza preservada em relação aos 104,75 do *Recalling* E2). No campo `textil`, a densidade salta de 1 a 8 por 10k nos livros para 49,69 em *Clarifications*. No *Recalling*, o campo `textil` é praticamente ausente em ambas as versões (zero na Etapa 2, uma única ocorrência na Etapa 2-bis), o que sugere que dentro do gênero metateórico há divisão de segundo nível: *Clarifications* mobiliza vocabulário têxtil-topológico de modo denso; *Recalling* concentra-se na topologia, com a fração têxtil residual.

### 5.7. Validação amostral semântica nos dois artigos

A Etapa 2.6 aplicou o protocolo A/B/C aos quatro campos centrais do argumento têxtil-topológico (`textil`, `topologia`, `network`, `actor_network`) em 82 ocorrências classificadas manualmente. Resultados consolidados:

| Campo | n total | sim | parcial | nao | taxa de figuralidade |
|---|---:|---:|---:|---:|---:|
| `textil` | 15 | 14 | 1 | 0 | 0,967 |
| `topologia` | 28 | 26 | 2 | 0 | 0,964 |
| `network` | 22 | 9 | 5 | 8 | 0,523 |
| `actor_network` | 17 | 13 | 1 | 3 | 0,794 |

Por obra:

| Obra | n | sim | parcial | nao | taxa de figuralidade |
|---|---:|---:|---:|---:|---:|
| *Clarifications* 1996 | 60 | 48 | 9 | 3 | 0,875 |
| *Recalling ANT* 1999 (E2) | 22 | 14 | 0 | 8 | 0,636 |

Fonte: `outputs/etapa2_artigos/validacao_amostral_resultados.md` (gerado por `scripts/19_etapa2_finalizar_validacao.py`).

Os campos `textil` e `topologia` saem com taxas no topo (0,967 e 0,964), confirmando que o vocabulário têxtil-topológico opera nos artigos predominantemente em registro figural. O campo `network` tem taxa de 0,523, efeito direto do registro autocrítico-metalinguístico do *Recalling*, que tematiza o termo em vez de mobilizá-lo. O `actor_network` recebe o mesmo efeito em escala menor (0,794).

O mapa de polissemia, distribuição das 20 classificações `nao`/`parcial`:

| Subcategoria | n | predominância |
|---|---:|---|
| `metalinguistico` | 9 | Recalling = 8, Clarifications = 1 |
| `tecnico` | 5 | Clarifications = 5 |
| `descritivo` | 4 | Clarifications = 4 |
| `definicao_operacional` | 1 | Clarifications = 1 |
| `polissemia` | 1 | Clarifications = 1 |

Dos 11 casos `nao` em todo o corpus validado, **9 são da subcategoria `metalinguistico`**, e **8 desses 9 estão no *Recalling***. As ocorrências concentram-se em passagens em que Latour cita o próprio vocabulário da TAR para suspendê-lo (`let us abandon the words actor and network`, `the very expression of network invites this reaction`, `the third nail in the coffin`). O *Recalling* opera em registro autocrítico-metalinguístico distinto do registro expositivo-figural de *Clarifications*. Esse é resultado novo da Etapa 2.6 e organiza, dentro do gênero metateórico, uma divisão de segundo nível.

A Etapa 2-bis refez a amostragem sobre o corpus integral do *Recalling*. Resultado: 40 ocorrências amostradas (vs. 22 exaustivas na Etapa 2.6); **31 classificações migradas automaticamente** da planilha preenchida (por casamento de chave composta `campo + termo + trecho central`), **9 linhas novas em branco** aguardam preenchimento manual em sessão futura (vide § 8). A taxa de figuralidade do *Recalling* na 2-bis fica como referência parcial: as 9 novas distribuem-se principalmente em camadas A e B, com expectativa de taxas altas similares às dos demais campos. O achado central (concentração metalinguística no *Recalling*) é robusto às 9 linhas.

A tabela têxtil-topológica refinada pela validação semântica, com a coluna *Science in Action* marcada como pendente (a validação retroativa nos livros é uma das pendências abertas, vide § 8):

| Obra | Campo | Bruta n | Taxa fig. | Refinada n | Freq. refinada /10k |
|---|---|---:|---:|---:|---:|
| *Clarifications* (1996) | `textil` | 39 | 0,967 | 37,7 | 48,04 |
| *Clarifications* (1996) | `topologia` | 118 | 0,933 | 110,1 | 140,33 |
| *Clarifications* (1996) | `network` | 93 | 0,700 | 65,1 | 82,95 |
| *Clarifications* (1996) | `actor_network` | 19 | 0,900 | 17,1 | 21,79 |
| *Recalling* (E2) | `topologia` | 13 | 1,000 | 13,0 | 104,75 |
| *Recalling* (E2) | `network` | 7 | 0,143 | 1,0 | 8,06 |
| *Recalling* (E2) | `actor_network` | 2 | 0,000 | 0,0 | 0,00 |
| *Science in Action* (1987) | (todos) | -- | *pendente* | -- | -- |

Fonte: `outputs/etapa2_artigos/tabela_textil_topologico_refinada.tex`.

### 5.8. Classificação automática do campo militar nos artigos

A desambiguação automática da Etapa 2.2 cobriu as 4 ocorrências brutas do campo militar nos artigos, com gatilho casando em 100% dos casos:

| Obra | Termo | Categoria | Gatilho automático |
|---|---|---|---|
| *Clarifications* 1996 | `allies` (em `"network of allies and extend his power"`) | `metalinguistico` | aspas=4 + 2 termos TAR (`network`, `network`) |
| *Clarifications* 1996 | `enemies` (em `"pre-relativist enemies"`) | `conceitual_debate` | `Reflexivists`, `pre-relativist` (2 palavras em `-ist`/`-ism`) |
| *Clarifications* 1996 | `alliance` (em `"Prigogine et Stengers, La nouvelle alliance, métamorphose..., Gallimard/Bantam, (1979)"`) | `descritivo_bibliografico` | ano em parênteses + editora + autores sequenciais |
| *Recalling* E2 / E2-bis | `wars` (em `"the recent Science Wars"`) | `descritivo_historico` | casa `Science Wars` |
| *Recalling* E2-bis (apenas) | `alliance` (em `"ridiculous poverty of the ANT vocabulary—association, translation, alliance, obligatory passage point"`) | `metalinguistico` | indicador `vocabulary` + 4 termos TAR |

Fontes: `outputs/etapa2_artigos/militar_classificacao_automatica.csv` (Etapa 2, 4 ocorrências) e `outputs/etapa2bis_recalling/militar_classificacao_automatica.csv` (Etapa 2-bis, 2 ocorrências do *Recalling*).

A nova ocorrência `alliance` no *Recalling* bis é o achado pontual mais saliente da Etapa 2-bis. A passagem `ridiculous poverty of the ANT vocabulary—association, translation, alliance, obligatory passage point` é exatamente a que motivou, na Etapa 2.2, a criação da categoria `metalinguistico`, e cuja ausência do corpus parcial era ressalva metodológica explícita registrada no relatório original da Etapa 2 (subseção 2.1, § Ressalvas; § 2 do briefing 2-bis). Latour cita os termos canônicos da TAR (`association`, `translation`, `alliance`, `obligatory passage point`) precisamente para classificá-los como vocabulário pobre a ser substituído. A nova ocorrência amplia a base empírica do recuo do vocabulário militar no *Recalling*: nas duas únicas ocorrências brutas, nenhuma mobiliza o vocabulário militar como tropo da prática científica. A refinada figural permanece zero, agora em sustentação mais robusta.

### 5.9. Cocorrência principal nos dois artigos

A janela proporcional (2% das palavras totais) é a configuração recomendada para a tese; a janela 200 fica como controle. Para o *Recalling*, mostro as duas versões (Etapa 2, j=25, e Etapa 2-bis, j=97).

Top 10 pares por força em *Clarifications*, janela 157 (proporcional 2% de 7.848):

| Par | n (j=157) | n (j=200, controle) |
|---|---:|---:|
| network, topologia | 616 | 783 |
| textil, topologia | 171 | 222 |
| actor_network, network | 138 | 162 |
| network, textil | 101 | 130 |
| actor_network, topologia | 84 | 102 |
| militar, network | 8 | 10 |
| topologia, translation | 7 | 8 |
| actor_network, textil | 6 | 7 |
| centre_of_calculation, network | 4 | 5 |
| centre_of_calculation, textil | 3 | 5 |

Fonte: `outputs/latour_1996_clarifications_en/relatorios/cocorrencia_j157.md` e `cocorrencia_j200.md`.

Top pares por força no *Recalling*, com Etapa 2 (j=25) e Etapa 2-bis (j=97) lado a lado:

| Par | E2 j=25 | E2-bis j=97 |
|---|---:|---:|
| network, topologia | 2 | **38** |
| actor_network, network | 2 | 23 |
| actor_network, topologia | 0 | 10 |
| **circulating_reference, topologia** | 0 | **9** |
| textil, topologia | 0 | 6 |
| militar, topologia | 1 | 3 |
| network, translation | 0 | 3 |
| topologia, translation | 0 | 2 |
| inscription, network | 0 | 2 |
| articulation, topologia | 0 | 2 |
| construction, topologia | 0 | 2 |

Fontes: `outputs/latour_1999_recalling_en/relatorios/cocorrencia_j025.md` (Etapa 2), `outputs/latour_1999_recalling_bis/relatorios/cocorrencia_jprop.md` (Etapa 2-bis).

O ranking dos pares principais é consistente entre as duas versões do *Recalling* (`network`–`topologia` lidera, seguido por `actor_network`–`network`), e consistente também com o ranking de *Clarifications*. O par **`circulating_reference`–`topologia` (9 ocorrências na Etapa 2-bis, zero na Etapa 2)** comparece como achado novo: o campo `circulating_reference` tinha zero ocorrências no corpus parcial da Etapa 2 porque suas ocorrências caíam nas páginas excluídas, em particular nas pp. 22-23 do volume, onde Latour desenvolve o argumento "after ANT" como teoria do espaço de fluidos circulantes. A força do par no corpus integral o coloca entre os cinco principais. Registro o par como pista interpretativa relevante para futura elaboração na tese, sem desenvolver aqui interpretação que excederia o que a contagem mostra: o par compõe um vocabulário fluido-circulatório que coexiste com o vocabulário topológico no artigo; a leitura qualitativa das passagens correspondentes ficará por minha conta na redação do capítulo 2.

As redes de cocorrência por obra, com a duplicação Etapa 2 / Etapa 2-bis para o *Recalling*:

![Rede de cocorrência figural em *Clarifications* (1996), janela 200 palavras, layout *force-directed* `seed=42`. Fonte: `outputs/latour_1996_clarifications_en/figuras/rede_cocorrencia_j200.png`.](figuras/rede_cocorrencia_clarifications_j200.png)

![Rede de cocorrência figural em *Clarifications* (1996), janela proporcional 157 palavras. Fonte: `outputs/latour_1996_clarifications_en/figuras/rede_cocorrencia_j157.png`.](figuras/rede_cocorrencia_clarifications_j157.png)

![Rede de cocorrência figural em *Recalling ANT* (1999), Etapa 2, corpus parcial de 1.241 palavras, janela 200 (cobre cerca de 15% do texto, portanto produz pares espúrios por proximidade). Fonte: `outputs/latour_1999_recalling_en/figuras/rede_cocorrencia_j200.png`.](figuras/rede_cocorrencia_recalling_etapa2_j200.png)

![Rede de cocorrência figural em *Recalling ANT* (1999), Etapa 2, janela proporcional 25 palavras (2% do texto antigo). Fonte: `outputs/latour_1999_recalling_en/figuras/rede_cocorrencia_j025.png`.](figuras/rede_cocorrencia_recalling_etapa2_j025.png)

![Rede de cocorrência figural em *Recalling ANT* (1999), Etapa 2-bis, corpus integral de 4.825 palavras, janela 200. Fonte: `outputs/latour_1999_recalling_bis/figuras/rede_cocorrencia_j200.png`.](figuras/rede_cocorrencia_recalling_etapa2bis_j200.png)

![Rede de cocorrência figural em *Recalling ANT* (1999), Etapa 2-bis, janela proporcional 97 palavras (2% de 4.825). O par `circulating_reference`–`topologia` aparece com força entre os cinco principais, ausente da rede da Etapa 2. Fonte: `outputs/latour_1999_recalling_bis/figuras/rede_cocorrencia_jprop.png`.](figuras/rede_cocorrencia_recalling_etapa2bis_jprop.png)

### 5.10. Seis passagens-âncora dos artigos metateóricos

Reproduzo seis passagens-âncora dos artigos, em prosa contida, organizadas pela ordem do texto.

**De *Clarifications* (1996), nas pp. 76-77 do PDF de circulação:**

1. `"AT is a change of methaphors to describe essences: instead of surfaces one gets filaments..."` — Latour anuncia explicitamente que a TAR é mudança de metáforas, e nomeia a nova metáfora como filamentos contra superfícies.
2. `"More precisely it is a change of topology..."` — A mudança metafórica é especificada como mudança topológica.
3. `"modern societies cannot be described without recognizing them as having a fibrous, thread-like, wiry, stringy, ropy, capillary character..."` — A sequência canônica do vocabulário têxtil-topológico mobilizado para descrever as sociedades modernas. Seis adjetivos em série (`fibrous, thread-like, wiry, stringy, ropy, capillary`) que constituem a passagem programática do campo `textil` nos artigos.

**De *On Recalling ANT* (1999):**

4. `"may be the social possesses the bizarre property of not being made of agency and structure at all, but rather of being a circulating entity"` — A reformulação do social como entidade circulante, base da articulação `circulating_reference`–`topologia` da Etapa 2-bis.
5. `"the ridiculous poverty of the ANT vocabulary—association, translation, alliance, obligatory passage point..."` — A passagem que Latour usa para classificar os termos da TAR (incluindo `alliance` do campo militar) como vocabulário pobre a ser substituído. Passagem-chave do registro metalinguístico, ausente do corpus parcial da Etapa 2 e restituída pela Etapa 2-bis.
6. `"our own vocabulary has contaminated our ability to let the actors build their own space..."` — O gesto autocrítico explícito sobre a contaminação do vocabulário da TAR, presente em ambas as versões do *Recalling*.

---

## 6. Diff Etapa 2 → Etapa 2-bis no *Recalling*

### 6.1. Cobertura comparada

| Métrica | Etapa 2 | Etapa 2-bis | Δ |
|---|---:|---:|---:|
| Palavras de corpo (`split`) | 1.241 | 4.825 | +3.584 |
| Páginas do volume cobertas | 5 (16, 18, 20, 22, 24) | 11 (15-25) | +6 |
| Cobertura efetiva (sobre 4.825) | 25,3% | 100% | +74,7 pp |

### 6.2. Diff por campo figurativo

| Campo | E2 n | E2 /10k | bis n | bis /10k | Δ n | Δ /10k |
|---|---:|---:|---:|---:|---:|---:|
| `inscription` | 0 | 0,00 | 1 | 2,07 | +1 | +2,07 |
| `immutable_mobile` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `black_box` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `centre_of_calculation` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `actor_network` | 2 | 16,12 | 9 | 18,65 | +7 | +2,54 |
| `translation` | 0 | 0,00 | 2 | 4,15 | +2 | +4,15 |
| `trial_of_strength` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `factish` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `circulating_reference` | 0 | 0,00 | 2 | 4,15 | +2 | +4,15 |
| `articulation` | 0 | 0,00 | 1 | 2,07 | +1 | +2,07 |
| `construction` | 1 | 8,06 | 2 | 4,15 | +1 | −3,91 |
| `proposition` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `network` | 7 | 56,41 | 28 | 58,03 | +21 | +1,62 |
| `agonistic` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `enrollment` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `spokesperson` | 0 | 0,00 | 0 | 0,00 | 0 | 0,00 |
| `militar` | 1 | 8,06 | 2 | 4,15 | +1 | −3,91 |
| `textil` | 0 | 0,00 | 1 | 2,07 | +1 | +2,07 |
| `topologia` | 13 | 104,75 | 48 | 99,48 | +35 | −5,27 |
| **Total** | 24 | -- | 96 | -- | -- | -- |

Os campos com maior delta absoluto são `topologia` (+35), `network` (+21) e `actor_network` (+7). Os campos antes ausentes que agora aparecem no corpus integral: `translation` (+2), `circulating_reference` (+2), `inscription` (+1), `articulation` (+1), `textil` (+1).

Comentário sobre as densidades aparentemente decrescentes (`topologia` de 104,75 para 99,48; `construction` e `militar` de 8,06 para 4,15): são artefato da renormalização. A cobertura passou a incluir as pp. 15 e 25 do volume e a parte truncada das pp. 17, 19, 21, 23, onde a densidade dos campos centrais é menor que nos blocos canônicos das pp. 18, 20, 22, 24 da Etapa 2 original. Não há redução real; há alargamento da base, com manutenção da ordem de grandeza.

### 6.3. Diff de desambiguação

| Termo | Etapa 2 | Etapa 2-bis | Categoria |
|---|---|---|---|
| `wars` (em `"Science Wars"`) | presente | presente | `descritivo_historico` |
| `alliance` (em `"vocabulary—association, translation, alliance, obligatory passage point"`) | ausente (caía em estrato excluído) | **presente** | `metalinguistico` |

| Versão | Bruta n | Refinada figural n | Refinada figural /10k |
|---|---:|---:|---:|
| Etapa 2 | 1 | **0** | **0,00** |
| Etapa 2-bis | 2 | **0** | **0,00** |

A contagem refinada figural permanece zero. A nova ocorrência `alliance` é classificada automaticamente como `metalinguistico` (gatilho: indicador `vocabulary` + 4 termos TAR), e o argumento sobre o recuo do vocabulário militar no *Recalling* fica reforçado: das duas únicas ocorrências brutas, ambas são não-figurais.

### 6.4. Diff de cocorrência

Vide tabela em § 5.9. Destaque para o par `circulating_reference`–`topologia` (9 ocorrências na Etapa 2-bis, ausente da Etapa 2 porque `circulating_reference` tinha zero ocorrências no corpus parcial). Registro a aparição como achado documentado, sem desenvolver interpretação que excederia o que a contagem mostra.

### 6.5. Diff de validação semântica

| Campo | Etapa 2.6 (antigo) | Etapa 2-bis | Migradas | Novas (em branco) |
|---|---|---|---:|---:|
| `textil` | exaustiva (n=0) | exaustiva (n=1) | 0 | 1 |
| `topologia` | exaustiva (n=13) | A/B/C (n=15) | 13 | 2 |
| `network` | exaustiva (n=7) | A/B/C (n=15) | 7 | 8 |
| `actor_network` | exaustiva (n=2) | exaustiva (n=9) | 2 | 7 |
| **Total** | **22** | **40** | **31** | **9** |

Das 40 ocorrências da planilha 2-bis, 31 vieram com classificação migrada da Etapa 2.6 (mesma ocorrência, mesma classificação, casada por chave `campo + termo + trecho central`). 9 são novas (oriundas das páginas antes excluídas, em particular pp. 15, 17, 19, 21, 23, 25) e ficam em branco aguardando preenchimento manual da pesquisadora em sessão futura. O preenchimento dessas 9 linhas é a pendência principal da Etapa 2-bis (vide § 8).

### 6.6. Conclusão sobre o argumento

O achado central (inversão entre vocabulário militar e vocabulário têxtil-topológico nos artigos metateóricos) é **confirmado e reforçado** pela Etapa 2-bis. A nova ocorrência metalinguística de `alliance` amplia a base empírica do recuo do vocabulário militar no *Recalling*; as densidades têxtil-topológicas mantêm-se em ordem de grandeza comparável às da Etapa 2 (topologia em 99,48/10k contra 104,75/10k), indicando que o achado de fundo não era artefato do corpus parcial. O par `circulating_reference`–`topologia`, ausente na Etapa 2 porque caía no estrato excluído, comparece agora com força e fica registrado como pista interpretativa relevante para futura elaboração na tese.

---

## 7. Síntese final

A trajetória do campo `militar` na escrita latouriana entre 1986 e 1999, conforme as três etapas mostram, segue movimento de pico e sedimentação interno aos livros monográficos solo. Em 1987, com *Science in Action*, a densidade militar bruta atinge 26,74/10k, com refinada figural de 26,03 após subtrair as 10 ocorrências de `war/wars` descritivas. Em 1999, com *Pandora's Hope*, a densidade militar bruta cai para 16,56, com refinada de 12,19 após subtrair 56 ocorrências descritivo-históricas (Science Wars, Joliot, Szilard). Em 1986, *Laboratory Life* (coautoria com Woolgar) está em patamar baixo (3,69/10k bruta, 3,50 refinada), próximo do patamar dos artigos metateóricos. O contraste entre 1986 e 1987-1999 é o achado etnográfico complementar sobre a coautoria com Woolgar, pista para investigação futura sobre efeito da coautoria no registro figurativo da escrita latouriana. Nos dois artigos metateóricos (*Clarifications* 1996 e *Recalling ANT* 1999, esta segunda obra em duas versões de corpus), a contagem refinada figural cai a zero: as ocorrências militares dos artigos são todas não-figurais (`descritivo_historico` para `wars` em Science Wars; `metalinguistico` para `allies` em `"network of allies"` e para `alliance` em `"poverty of the ANT vocabulary"`; `conceitual_debate` para `enemies` em `"pre-relativist enemies"`; `descritivo_bibliografico` para `alliance` em `"La nouvelle alliance"`).

A trajetória inversa é a do vocabulário têxtil-topológico. Nos livros, presente em densidades de 1 a 8 (textil) e 13 a 34 (topologia) por 10.000 palavras. Em *Clarifications*, salta para 49,69 e 150,36. Em *Recalling*, a topologia atinge 99,48/10k no corpus integral (104,75 no corpus parcial, ordem de grandeza preservada), e o textil é residual (uma ocorrência, `ties`). A validação amostral semântica da Etapa 2.6 confirma que essas densidades são predominantemente figurais: taxa de figuralidade de 0,967 para `textil` e 0,964 para `topologia` sobre as 43 ocorrências dos dois campos classificadas em camadas A/B/C. Em *Clarifications*, a taxa por obra é 0,875; em *Recalling* (corpus parcial), 0,636, com o campo `network` em 0,143 (sustentado pela concentração metalinguística do registro autocrítico). A validação retroativa A/B/C nos livros monográficos fica como pendência (vide § 8); a aplicação retroativa permitiria fechar a comparação cruzada de figuralidade entre artigos e livros sob a mesma instrumentação.

A questão do **registro** é o que organiza o conjunto. O vocabulário militar é vocabulário da descrição da prática tecnocientífica: nos livros, Latour mobiliza `ally`, `enemy`, `mobilise`, `enroll`, `battle`, `victory` para descrever o que cientistas e engenheiros fazem. O vocabulário têxtil-topológico é vocabulário do registro autorreflexivo: nos artigos, Latour mobiliza `fibrous`, `thread-like`, `wiry`, `stringy`, `ropy`, `capillary`, `filaments`, `surfaces`, `fluid`, `flat`, `folded`, `circulation` para descrever **o que a teoria ator-rede é**. A divisão de trabalho metafórico por gênero textual é, portanto, divisão entre dois objetos descritos: o objeto da descrição da prática (livros) e o objeto da metateoria (artigos). Dentro do gênero metateórico, há uma divisão de segundo nível identificada pela Etapa 2.6: *Clarifications* opera em registro expositivo-figural (taxa de figuralidade 0,875), enquanto *Recalling* opera em registro autocrítico-metalinguístico (taxa 0,636, com network a 0,143). Latour, no *Recalling*, tematiza o vocabulário da TAR para suspendê-lo, no gesto autocrítico que dá ao artigo seu título e sua estrutura interna em quatro "nails in the coffin".

A pista do par `circulating_reference`–`topologia` no *Recalling* integral (9 cocorrências na janela proporcional 97, ausente do corpus parcial) abre um terceiro nível interpretativo, que registro como dado e deixo para a redação da tese desenvolver: dentro do *Recalling*, há um regime fluido-circulatório que se articula com a topologia, distinto tanto do regime expositivo-figural de *Clarifications* (em que a topologia se articula com o têxtil) quanto do regime descritivo-militar dos livros (em que a topologia se articula com `network` e o vocabulário militar). O par marca o vocabulário do "after ANT" como teoria do espaço de fluidos circulantes nas pp. 22-23 do volume, e a leitura qualitativa das passagens correspondentes vai compor a argumentação do capítulo 2 da tese em sessão posterior. Aqui, registro a pista sem desenvolver interpretação que excederia o que a contagem mostra.

A descoberta tardia de que a Etapa 2 cobriu 25,3% do *Recalling*, e não os ~80% que o relatório original declarava em premissa errada sobre o tamanho do artigo, é parte da história do projeto. A Etapa 2-bis tornou essa descoberta possível e fez a contagem agora representativa. Mantenho o relatório da Etapa 2 intocado como artefato auditável de uma sessão que operou sobre premissa equivocada; mantenho o relatório da Etapa 2-bis com a correção explícita; e este relatório consolidado registra ambas as versões lado a lado, sem suavizar o que aconteceu. O método é parte do argumento: a cadeia mim → OCR → pipeline normalizou um pedaço do *Recalling* que era menor do que eu pensava, e a aferição correta veio apenas quando o estrato excluído ficou acessível.

---

## 8. Pendências e limitações declaradas

1. **Nove linhas em branco da validação amostral semântica do *Recalling* (Etapa 2-bis)** aguardam preenchimento manual da pesquisadora, em `outputs/etapa2bis_recalling/validacao_amostral_semantica.csv`. As colunas em branco são `uso_figural`, `subcategoria` e `comentario`. Distribuição das 9 linhas: 7 em `actor_network` exaustivo (campo passou de 2 ocorrências exaustivas na Etapa 2.6 para 9 ocorrências exaustivas na 2-bis), 8 em `network` A/B/C (campo passou de 7 exaustivas para 15 amostradas em 3 camadas), 2 em `topologia` A/B/C, 1 em `textil` exaustivo (ocorrência única `ties`, que era zero na Etapa 2). Após o preenchimento, a taxa de figuralidade refinada para o *Recalling* na 2-bis pode ser computada de modo definitivo.

2. **Validação amostral semântica das três obras monográficas (aplicação retroativa A/B/C aos livros)** permanece pendente. As densidades dos campos `textil` e `topologia` nos livros (1,23/13,81 em Lab Life; 7,94/34,68 em Science in Action; 8,20/27,58 em Pandora's Hope) não foram aferidas em registro semântico, apenas em registro lexical. Sem essa aferição, a coluna *Science in Action* da tabela `tab:textil-topologico-refinado` fica como `pendente`, e a comparação cruzada de figuralidade entre artigos e livros sob a mesma instrumentação não pode ser fechada.

3. **Leitura manual dos seis candidatos `metalinguistico` retroativos nos livros**, listados em `outputs/etapa2_artigos/metalinguistico_retroativo_livros.csv` (4 candidatos `network` em *Science in Action*, 1 `actor_network` em *Science in Action*, 1 `actor_network` em *Pandora's Hope*; zero em *Laboratory Life*). A planilha foi gerada por gatilho automático na Etapa 2.6; a classificação manual fica para sessão futura. Sem essa classificação, a tabela militar refinada não detalha as categorias `metalinguistico`, `descritivo_bibliografico` e `conceitual_debate` para os livros (na tabela detalhada da Etapa 2.5 essas colunas aparecem como `--` para os livros, indicando que a desambiguação só foi feita para `war/wars` na Etapa 1).

4. **Dois commits locais da Etapa 2-bis (`476707e` Passo 0 e `ced27df` Passos 1-8)** aguardam revisão antes de push ao remoto. O briefing da Etapa 2-bis pediu commit local sem push automático; mantenho a instrução até autorização explícita.

5. **PDF nativo do *Recalling* para reanálise integral** foi pendência originalmente declarada na Etapa 2.6 e está fechada pela Etapa 2-bis, com o TXT integral fornecido pela pesquisadora. O ciclo aqui se encerra.

6. **Ajustes no código entre etapas**: a Etapa 2-bis estendeu os scripts `02_kwic.py`, `03_frequencies.py`, `04_visualizations.py` e `05_cooccurrence.py` para aceitar o novo escopo `etapa2bis` (coluna `escopo_etapa2bis` adicionada ao `metadata.csv`). Documentado em `docs/decisoes_metodologicas.md` § Etapa 2-bis § 2.

7. **Princípio de auditabilidade**: nenhuma sessão sobrescreveu output anterior em silêncio. Os outputs da Etapa 2 original em `outputs/etapa2_artigos/` e `outputs/<obra>/` (para `latour_1999_recalling_en`) permanecem intactos lado a lado dos outputs da Etapa 2-bis em `outputs/etapa2bis_artigos/`, `outputs/etapa2bis_recalling/` e `outputs/latour_1999_recalling_bis/`.

---

## Anexos

### Anexo A — Arquivos CSV gerados

**Etapa 1 (livros monográficos):**

| Caminho | Função |
|---|---|
| `corpus/metadata.csv` | Catálogo bibliográfico das obras com colunas `escopo_etapa1`, `escopo_etapa2`, `escopo_etapa2bis`. |
| `corpus/qualidade_extracao.csv` | Páginas, palavras totais e taxas de qualidade por obra. |
| `corpus/paginas/<id>.csv` | Classificação de cada página por classe (`inicio_capitulo`, `corpo`, `notas_fim`, `paratexto`, `qualidade_baixa`). |
| `outputs/<obra>/csv/kwic.csv` | Uma linha por ocorrência (janela ±10, página, posição, exclusão). |
| `outputs/<obra>/csv/frequencias.csv` | Contagem por grupo, frequência por 10k palavras, variantes top. |
| `outputs/<obra>/csv/cocorrencia.csv` | Matriz simétrica grupo × grupo, janela 200 palavras. |
| `outputs/<obra>/csv/amostra_validacao.csv` | Amostra estratificada da Etapa 0/1, validação manual de classificação de página. |
| `outputs/trajetoria_latour_1986_1999.csv` | Matriz grupo × obra (3 obras), freq por 10k. |
| `outputs/amostra_validacao_etapa1.csv` | Consolidado da validação amostral da Etapa 1. |
| `refinamento/war_pandora_classificacao.csv` | Classificação manual `war/wars` na Etapa 1 (descritivo/figurativo). |
| `refinamento/militar_refinado_tres_obras.csv` | Tabela refinada do campo militar nos 3 livros. |

**Etapa 2 (artigos metateóricos):**

| Caminho | Função |
|---|---|
| `outputs/latour_1996_clarifications_en/csv/kwic.csv` | KWIC do *Clarifications*. |
| `outputs/latour_1996_clarifications_en/csv/frequencias.csv` | Frequências do *Clarifications*. |
| `outputs/latour_1996_clarifications_en/csv/cocorrencia_j200.csv` | Cocorrência do *Clarifications*, janela 200. |
| `outputs/latour_1996_clarifications_en/csv/cocorrencia_j157.csv` | Cocorrência do *Clarifications*, janela proporcional 157. |
| `outputs/latour_1996_clarifications_en/csv/validacao_amostral_semantica.csv` | Planilha A/B/C do *Clarifications* (60 linhas). |
| `outputs/latour_1999_recalling_en/csv/kwic.csv` | KWIC do *Recalling* (Etapa 2, corpus parcial). |
| `outputs/latour_1999_recalling_en/csv/frequencias.csv` | Frequências do *Recalling* E2. |
| `outputs/latour_1999_recalling_en/csv/cocorrencia_j025.csv` | Cocorrência do *Recalling* E2, j=25. |
| `outputs/latour_1999_recalling_en/csv/cocorrencia_j200.csv` | Cocorrência do *Recalling* E2, j=200. |
| `outputs/latour_1999_recalling_en/csv/validacao_amostral_semantica.csv` | Planilha A/B/C do *Recalling* E2 (22 linhas, exaustiva). |
| `outputs/etapa2_artigos/militar_classificacao_automatica.csv` | Classificação automática do campo militar (4 ocorrências dos artigos). |
| `outputs/etapa2_artigos/metalinguistico_retroativo_livros.csv` | Candidatos `metalinguistico` retroativos nos livros (6 ocorrências; classificação manual em branco). |
| `outputs/etapa2_artigos/tabela_comparativa_5_obras_n.csv` | Comparativa 19 campos × 5 obras, contagem absoluta. |
| `outputs/etapa2_artigos/tabela_comparativa_5_obras_freq.csv` | Comparativa 19 campos × 5 obras, densidade. |
| `outputs/etapa2_artigos/tabela_militar_refinado_5_obras.csv` | Militar refinado detalhado por categoria. |
| `outputs/etapa2_artigos/tabela_textil_topologico_5_obras.csv` | Têxtil e topologia nas 5 obras. |
| `outputs/etapa2_artigos/validacao_amostral_semantica.csv` | Consolidado A/B/C (82 linhas, colunas em branco). |
| `outputs/etapa2_artigos/validacao_amostral_semantica_PREENCHIDA.csv` | Mesmas 82 linhas preenchidas pela pesquisadora. |
| `outputs/etapa2_artigos/validacao_amostral_semantica_PREENCHIDA_CORRIGIDA.csv` | Versão com `id_kwic` único por offset e `pagina` recalculada. |

**Etapa 2-bis (*Recalling* TXT integral):**

| Caminho | Função |
|---|---|
| `outputs/latour_1999_recalling_bis/csv/kwic.csv` | KWIC do *Recalling* bis. |
| `outputs/latour_1999_recalling_bis/csv/frequencias.csv` | Frequências do *Recalling* bis. |
| `outputs/latour_1999_recalling_bis/csv/cocorrencia_j200.csv` | Cocorrência do *Recalling* bis, j=200. |
| `outputs/latour_1999_recalling_bis/csv/cocorrencia_jprop.csv` | Cocorrência do *Recalling* bis, j=97 (proporcional). |
| `outputs/etapa2bis_recalling/militar_classificacao_automatica.csv` | Classificação automática militar (2 ocorrências do *Recalling* bis). |
| `outputs/etapa2bis_recalling/validacao_amostral_semantica.csv` | Planilha A/B/C migrada + novas linhas em branco (40 linhas). |
| `outputs/etapa2bis_artigos/tabela_comparativa_5_obras_bis_n.csv` | Comparativa com *Recalling* bis no lugar do antigo. |
| `outputs/etapa2bis_artigos/tabela_comparativa_5_obras_bis_freq.csv` | Idem, densidade. |

### Anexo B — Scripts utilizados

| Script | Função |
|---|---|
| `scripts/01_extract_text.py` | Extrai PDFs via `pdftotext -layout`, classifica páginas, gera `corpus/qualidade_extracao.csv`. |
| `scripts/01b_normalize_text.py` | Normaliza extração: soft hyphens, hifenização EOL, marcadores `((NN))`, cabeçalhos espaçados, NFKC. |
| `scripts/02_kwic.py` | KWIC sobre `corpus/txt_norm/`. Aceita `--escopo etapa1|etapa2|etapa2bis|todos` e `--adicoes <arquivos>`. |
| `scripts/03_frequencies.py` | Tabela de frequências por grupo, com freq por 10k. Idem `--escopo`. |
| `scripts/04_visualizations.py` | Figuras de frequência e densidade por obra. Idem `--escopo`. |
| `scripts/05_cooccurrence.py` | Matriz de cocorrência e rede figural. Aceita `--janela` e `--sufixo`. Idem `--escopo`. |
| `scripts/06_sampling.py` | Amostragem estratificada (Etapa 0/1, classificação de página). |
| `scripts/07_trajectory.py` | Matriz grupo × obra para o relatório de trajetória. |
| `scripts/08_validate_sample.py` | Validação amostral da classificação de página. |
| `scripts/10_passo4_kwic_ampliado.py` | KWIC ampliado a ±50 palavras para curadoria de citações. |
| `scripts/11_passo4_graficos.py` | Figuras do passo 4 (comparação 3 obras, painel de rankings, densidade militar, refinada). |
| `scripts/13_audit_articles_etapa2.py` | Sanity check dos `.txt` dos artigos da Etapa 2. |
| `scripts/14_etapa2_tabela_comparativa.py` | Tabela comparativa 5 obras (Etapa 2.1). |
| `scripts/15_etapa2_desambiguar_militar.py` | Desambiguação automática do campo militar nos artigos. |
| `scripts/16_etapa2_cocorrencia_comparacao.py` | Relatório comparativo de cocorrência (Etapa 2.4). |
| `scripts/17_etapa2_tabelas_finais.py` | Três tabelas finais consolidadas (Etapa 2.5). |
| `scripts/18_etapa2_validacao_amostral.py` | Geração das planilhas A/B/C (Etapa 2.6). |
| `scripts/19_etapa2_finalizar_validacao.py` | Correção de bugs, resultados analíticos, tabela refinada (Etapa 2.6 final). |
| `scripts/20_etapa2bis_tabela_5_obras.py` | Tabela comparativa 5 obras com *Recalling* bis. |
| `scripts/21_etapa2bis_validacao_migracao.py` | Migração de classificações A/B/C da Etapa 2.6 para 2-bis. |

### Anexo C — Hashes SHA-256 dos TXT normalizados

```
latour_woolgar_1986_lab_life_en.txt    11a01b2fe168d7104903b759f198d7c10be5e7ae0afd38344509fce80b300387
latour_1987_science_action_en.txt      436b309fad0a02829699e2072f900c7200d8454201771bbbf860f2f37b781f4a
latour_1999_pandora_en.txt             5951f89663ec1ea760b4c88615a9021c38f8e1ac10425a09c2f913c89da30ba6
latour_1996_clarifications_en.txt      cbea60abba433fc253958c7768f688b83221d2e9dfa64e18b101bff4aee3bfd1
latour_1999_recalling_en.txt           eac86c0fdf52b80d832af843135318acea5a73d4730ed3d2830287fcf23b0367
latour_1999_recalling_bis.txt          c090ca0a7508d9913bf1ca2d186a4293cd08c122152669216959580f6ed66912
```

Os dois últimos hashes correspondem às duas versões do *Recalling* (Etapa 2 antigo e Etapa 2-bis novo). Ambos permanecem versionados em `corpus/txt_norm/` e podem ser auditados independentemente.

---

**Fim do relatório consolidado.**

Os relatórios parciais permanecem como artefato auditável em seus diretórios originais (`outputs/etapa2_artigos/relatorio_etapa2.md`, `outputs/etapa2bis_artigos/relatorio_etapa2bis.md`, `outputs/trajetoria_latour_1986_1999.md`, `outputs/relatorio_extracao_etapa1.md`). Este documento substitui-os como fonte autoritativa de referência para a redação do capítulo 2 da tese e para leitura externa do conjunto da análise.
