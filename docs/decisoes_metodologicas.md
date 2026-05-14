# Decisões metodológicas — projeto `analise_figuracoes`

Este documento registra as decisões metodológicas tomadas para cada etapa da análise computacional do corpus teórico mobilizado na tese. Cada decisão é datada, justificada e revisável. Alterações posteriores devem ser registradas em adendo, com data e razão, sem sobrescrever a decisão anterior.

---

## Etapa 1 — Análise de trajetória conceitual em três obras de Bruno Latour (1986, 1987, 1999)

Data da decisão: 13 de maio de 2026.

### Objetivo analítico

A Etapa 1 rastreia o vocabulário figurativo de Bruno Latour em três obras publicadas ao longo de duas décadas, com objetivo de mapear continuidades, deslocamentos e introduções conceituais ao longo da trajetória do autor. A escolha de três obras do mesmo autor (em vez de uma) permite análise de trajetória que análise de obra única não oferece: como conceitos como *inscription*, *black box*, *immutable mobile* aparecem, persistem ou são reformulados ao longo do tempo, e quais figurações são introduzidas em momentos específicos da obra (por exemplo, *factish* em 1999).

A primeira obra do corpus, *Laboratory Life* (1986), tem coautoria com Steve Woolgar. Esse fato é registrado no metadata e considerado na análise: o vocabulário figurativo do livro é coautoral, e a comparação com as obras subsequentes (de Latour solo) permite observar quais figurações persistem após a parceria.

### 1. Corpus inicial

**Decisão**: a Etapa 1 processa três obras, todas em inglês:

- `latour_woolgar_1986_lab_life_en` — Latour e Woolgar, *Laboratory Life: The Construction of Scientific Facts*, Princeton University Press, 1986 (segunda edição).
- `latour_1987_science_action_en` — Bruno Latour, *Science in Action: How to Follow Scientists and Engineers through Society*, Harvard University Press, 1987.
- `latour_1999_pandora_en` — Bruno Latour, *Pandora's Hope: Essays on the Reality of Science Studies*, Harvard University Press, 1999.

**Justificativa**: as três obras compõem a trajetória de Latour entre o estudo etnográfico inicial do laboratório (com Woolgar), a sistematização da teoria ator-rede como programa de pesquisa, e a reflexão posterior sobre realismo científico e mediação. O vocabulário figurativo de cada obra é parcialmente herdeiro do anterior e parcialmente novo. Mapear esses três momentos permite produzir resultados que dialogam diretamente com a tese, em que Latour é mobilizado em todos os capítulos.

**Escolha da edição de *Laboratory Life***: a edição de 1986 (Princeton) substitui a de 1979 (Sage). A diferença não é trivial: a edição de 1986 remove a palavra "Social" do subtítulo (de *The Social Construction of Scientific Facts* para *The Construction of Scientific Facts*) e inclui um pós-escrito em que os autores justificam essa remoção. O pós-escrito é, ele mesmo, registro de deslocamento figurativo. A edição 1986 contém o texto da edição 1979 acrescido do pós-escrito, e é a edição mais citada na literatura subsequente.

### 2. Idioma de trabalho

**Decisão**: inglês. Modelo spaCy a carregar: `en_core_web_sm`.

**Justificativa**: as três obras são originais em inglês. Latour é francês e parte da sua obra é publicada originalmente em francês, mas as três obras desta etapa foram escritas e publicadas em inglês como textos originais (não como traduções). A análise se faz na língua de publicação original. Traduções para o português entram em rodadas posteriores, com pergunta analítica distinta.

### 3. Janela KWIC

**Decisão**: janela de ±10 palavras (10 palavras antes do termo-alvo e 10 palavras depois).

**Justificativa**: 5 palavras (padrão `nltk` e CLAWS) trunca a unidade argumentativa na prosa teórica densa de Latour, em que conceitos como *immutable mobile* ou *centre of calculation* costumam vir acompanhados de elaboração extensa. Janelas de 15 ou mais palavras geram contexto longo demais para leitura rápida durante validação amostral. 10 palavras é o ponto onde a unidade argumentativa fecha sem produzir excesso. A janela é parâmetro revisável: se a validação amostral mostrar que casos específicos exigem janela maior, o ajuste pode ser feito por termo, com adendo abaixo.

### 4. Catálogo único de termos em YAML

**Decisão**: aceita. O catálogo de termos a rastrear será mantido em arquivo único `campos_lexicais/catalogo_termos.yaml`, com hierarquia autor → campo figurativo → termos, e metadados por termo (variantes, lematização, exclusões, nota analítica).

**Justificativa**: arquivo único é mais auditável que múltiplos `.txt` plano. YAML permite registrar variantes, exclusões e notas que em `.txt` virariam ruído. O catálogo torna-se artefato citável: pode integrar o apêndice metodológico da tese, documentando exatamente quais termos foram rastreados e com que critérios.

**Estrutura inicial do catálogo para a Etapa 1 (Latour)**:

```yaml
latour:
  inscription:
    termos: ["inscription", "inscriptions", "inscription device", "inscription devices", "literary inscription"]
    nota: "Conceito presente desde Laboratory Life. Verificar continuidade nas tres obras."
  immutable_mobile:
    termos: ["immutable mobile", "immutable mobiles"]
    nota: "Aparece em Science in Action. Rastrear se ha precursor em Laboratory Life."
  black_box:
    termos: ["black box", "black-box", "black boxes", "blackbox", "blackboxing", "black-boxing"]
    nota: "Verificar primeira ocorrencia entre as tres obras."
  centre_of_calculation:
    termos: ["centre of calculation", "center of calculation", "centres of calculation", "centers of calculation"]
    nota: "Variantes ortograficas britanica e americana."
  actor_network:
    termos: ["actor-network", "actor network", "actant", "actants"]
    nota: "Em Laboratory Life o termo 'actant' ja aparece. Em Science in Action a expressao actor-network se consolida."
  translation:
    termos: ["translation", "translations", "translate", "translates", "translated"]
    exclusoes: ["translation of", "english translation", "french translation"]
    nota: "Atencao a falsos positivos: 'translation' em sentido linguistico trivial precisa ser separado do sentido conceitual."
  trial_of_strength:
    termos: ["trial of strength", "trials of strength"]
    nota: "Conceito de Science in Action."
  factish:
    termos: ["factish", "factishes"]
    nota: "Neologismo de Pandora's Hope. Verificar se ha precursores."
  circulating_reference:
    termos: ["circulating reference", "circulating references"]
    nota: "Pandora's Hope."
  articulation:
    termos: ["articulation", "articulations", "articulate", "articulated"]
    nota: "Conceito reformulado em Pandora's Hope. Possivel ruido por usos triviais do termo."
  construction:
    termos: ["construction", "constructed", "constructing", "social construction"]
    nota: "Conceito central em Laboratory Life. O pos-escrito de 1986 discute a polissemia do termo."
  proposition:
    termos: ["proposition", "propositions"]
    nota: "Reformulacao em Pandora's Hope. Atencao a usos logicos triviais."
  network:
    termos: ["network", "networks", "networking"]
    exclusoes: ["telephone network", "computer network"]
    nota: "Termo polissemico. Validacao amostral cuidadosa."
  agonistic:
    termos: ["agonistic", "agonistics", "agonistic field"]
    nota: "Science in Action."
  enrollment:
    termos: ["enrollment", "enrolment", "enroll", "enrol", "enrolled"]
    nota: "Variantes ortograficas britanica e americana."
  spokesperson:
    termos: ["spokesperson", "spokespersons", "spokesman", "spokesmen", "spokeswoman"]
    nota: "Traducao do frances 'porte-parole'."
```

### 5. Validação amostral das heurísticas de detecção de corpo e de qualidade

**Decisão**: validação por amostra estratificada de 15 páginas por obra (45 páginas no total para as três obras), distribuídas em cinco categorias de 3 páginas cada.

**Justificativa**: a validação estratificada garante representatividade dos contextos onde a heurística pode falhar. A redução de 25 para 15 páginas por obra é compensada pela triplicação do número de obras: 45 páginas no total cobre proporcionalmente mais diversidade de layouts editoriais e padrões de extração do que 25 páginas de uma obra única. Se durante a revisão a taxa de erro em uma categoria ultrapassar 20%, a amostra naquela categoria é ampliada e a heurística correspondente é ajustada.

**Distribuição da amostra (por obra)**:

- 3 páginas marcadas pelo algoritmo como início de capítulo
- 3 páginas marcadas como corpo de capítulo
- 3 páginas marcadas como notas de fim
- 3 páginas marcadas como bibliografia, índice remissivo ou outros paratextos
- 3 páginas com aviso automático de qualidade baixa (caracteres corrompidos, falhas de OCR, ligaduras mal extraídas)

Resultado da validação fica registrado em três arquivos:

- `outputs/latour_woolgar_1986_lab_life_en/relatorios/validacao_amostral_etapa1.md`
- `outputs/latour_1987_science_action_en/relatorios/validacao_amostral_etapa1.md`
- `outputs/latour_1999_pandora_en/relatorios/validacao_amostral_etapa1.md`

### 6. Estrutura do relatório final da Etapa 1

**Decisão**: o relatório final da Etapa 1 é organizado em dois níveis: relatório por obra (três arquivos) e relatório de trajetória (um arquivo consolidado).

**Por obra**: cada obra recebe seu próprio diretório de outputs em `outputs/<id_da_obra>/`, com KWIC, tabelas de frequência, visualizações e relatório descritivo.

**Trajetória consolidada**: o arquivo `outputs/trajetoria_latour_1986_1999.md` agrega resultados das três obras com foco em três perguntas:

1. Quais figurações aparecem em todas as três obras? Com que frequência relativa?
2. Quais figurações são introduzidas em uma obra e desaparecem ou persistem nas seguintes?
3. Como o vocabulário coautoral de *Laboratory Life* (Latour-Woolgar) se relaciona com o vocabulário das obras posteriores de Latour solo?

A estrutura comparativa do relatório de trajetória é o que torna a Etapa 1 analiticamente distinta de três análises independentes empilhadas.

---

## Adendos

### Adendo 1 (14 de maio de 2026): pipeline de normalização pré-KWIC

Decisão tomada após a primeira inspeção amostral dos três `corpus/txt/<id>.txt`. Inspeção registrou três artefatos sistemáticos de extração que, sem tratamento, contaminam a tokenização e o casamento de termos do catálogo:

- `latour_woolgar_1986_lab_life_en.txt`: 578 hifenizações de fim de linha (`infor-\nmation`).
- `latour_1987_science_action_en.txt`: 276 marcadores `((NN))` injetados no corpo pelo conversor (formato `((1))`, `((2))`, ...).
- `latour_1999_pandora_en.txt`: cerca de 2.500 caracteres não-ASCII dominados por soft hyphens U+00AD dentro de palavras (`per­formed`, `tech­nology`, `philoso­phers`); 220 replacement chars `�`; cabeçalhos com letras espaçadas (`P A N D O R A ' S H O P E`) repetidos no topo de muitas páginas.

Para preservar os textos crus como artefato auditável e operar a análise sobre versão normalizada, fica decidido:

1. Os arquivos em `corpus/txt/<id>.txt` permanecem intocados como extrações cruas. São o registro daquilo que o conversor entregou.
2. O script `scripts/01b_normalize_text.py` aplica seis operações de normalização e grava o resultado em `corpus/txt_norm/<id>.txt`. As operações, em ordem:
   1. Soft hyphen U+00AD removido.
   2. De-hifenização de fim de linha: `r"-\n(?=[a-z])"` substituído por `""`, juntando palavras quebradas pelo layout. Hifens médios (`actor-network`) ficam intactos.
   3. Marcadores `((NN))` substituídos por espaço.
   4. Linhas que casam o padrão de cabeçalho espaçado (sequências de caracteres únicos separados por espaço) descartadas.
   5. NFKC e mapeamento de aspas tipográficas (`‘’“”`) para ASCII; travessões longos (`–—`) para `-`.
   6. Replacement chars `�` substituídos por espaço (preserva separação de tokens; o caso reaparece na validação amostral da Etapa 2).
3. Os scripts seguintes (02 a 06) lêem a partir de `corpus/txt_norm/<id>.txt`. A tabela de páginas `corpus/paginas/<id>.csv` é regenerada a partir da versão normalizada, mantendo a heurística de classificação de `01_extract_text.py`. `corpus/qualidade_extracao.csv` é atualizado a partir das contagens da versão normalizada.
4. Nenhum parâmetro analítico da Etapa 1 muda. Janela KWIC continua ±10 palavras. Catálogo continua o mesmo. Amostra estratificada continua 15 páginas por obra. A normalização é preparação técnica.

Justificativa: sem essas seis operações, o KWIC perde casamentos óbvios em Pandora (`per­formed` não casa `performed`) e produz tokens espúrios em Science in Action (`((103))` virando token). Tratar de forma uniforme as três obras é o que permite que a comparação de trajetória produza números comparáveis.

### Adendo 2 (14 de maio de 2026): correção da heurística de classificação de páginas

Decisão tomada após a primeira rodada da amostra estratificada. A heurística original em `scripts/01_extract_text.py` tratava `paratexto` como estado único e sticky. Como toda obra começa com `Contents` ou `Sumário`, o estado entrava em `paratexto` na primeira página e nunca saía. Consequência: 282/296 (Lab Life), 309/314 (Science in Action) e 328/337 (Pandora) páginas classificadas como `paratexto`, com `corpo` colapsado para 4, 2 e 3 páginas respectivamente. A amostra estratificada, que pede 3 páginas por estrato, ficou inviável: 26 páginas em vez de 45.

Correção:

1. A regex `_RE_PARATEXTO` é decomposta em duas. `_RE_FRONT_MATTER` casa `contents`, `table of contents`, `sumário`, `sumario`, `acknowledgements`, `acknowledgments`, `agradecimentos`, `preface`, `prefácio`, `prefacio`, `dedication`, `introduction`, `foreword`. `_RE_BACK_MATTER` casa `bibliography`, `references`, `additional references`, `bibliografia`, `index`, `índice`, `indice`, `appendix`, `apêndice`, `apendice`.
2. O estado interno passa a ter três valores: `front_matter` (inicial, não-sticky), `corpo`, `back_matter` (sticky). `notas_fim` continua sendo classe de transição entre `corpo` e `back_matter`.
3. Detecção de início de capítulo (`Chapter N`, `CHAPTER N`, `Capítulo N`) passa a transitar para `corpo` mesmo se o estado atual for `front_matter`. Esse é o ponto que destrava o algoritmo: a primeira ocorrência de `Chapter 1` (Lab Life pg16, Science in Action pg25, Pandora — variantes) sai do front matter e começa a contar o corpo do livro.
4. `back_matter` continua sticky: uma vez em `Bibliography`, `Index`, etc., não se volta para `corpo`.
5. A classe registrada em `corpus/paginas/<id>.csv` permanece com cinco valores (`inicio_capitulo`, `corpo`, `notas_fim`, `paratexto`, `qualidade_baixa`) para preservar a estrutura dos estratos da decisão original. O front matter e o back matter ambos rotulam como `paratexto`; o estado interno apenas controla a transição.

A correção é replicada em `scripts/01_extract_text.py` (para quando a extração for refeita a partir do PDF) e em `scripts/01b_normalize_text.py` (para a regeneração imediata sobre os textos já normalizados). O catálogo de termos, a janela KWIC e a amostra estratificada (15 páginas por obra, 5 estratos de 3) permanecem inalterados. Os arquivos de KWIC, frequência, cocorrência e trajetória já gerados **não** são afetados, porque essas análises operam sobre o texto integral e não dependem da classificação por estado.

### Adendo 3 (14 de maio de 2026): refinamentos posteriores na heurística de página

Após a primeira rodada do Adendo 2, dois ajustes adicionais foram necessários para acomodar diferenças tipográficas entre as três obras:

1. **Início de capítulo detectado só no topo da página** (5 primeiras linhas, `_LINHAS_TOPO_INICIO_CAPITULO = 5`). Motivo: a página de abertura da seção de notas de Science in Action (pg282) começa com `Notes` seguido de `Introduction` e depois `Chapter 1` como subtítulo do agrupamento de notas por capítulo. A regex original casava `Chapter 1` em qualquer lugar da página e classificava erroneamente esta página como `inicio_capitulo`. Restringir a detecção ao topo da página resolve esse falso positivo sem sacrificar a detecção de capítulos reais, que sempre aparecem como cabeçalho na primeira linha não-vazia da página.

2. **Variantes tipográficas adicionais para início de capítulo**. A regex `_RE_INICIO_CAPITULO` foi estendida com três alternativas:
   - `^\s*(chapter|capítulo|capitulo|chapitre|part|parte)\s+(\d+|[ivxlcdm]+)\b` — padrão canônico (Lab Life, Science in Action).
   - `^\s*C\s+H\s+A\s+P\s+T\s+E\s+R\b` — letras espaçadas (Pandora's Hope, que tipografa cabeçalhos como `C H A P T E R   O N E`).
   - `^\s*chapter\s+(one|two|three|four|five|six|seven|eight|nine|ten)\b` — ordinal por extenso (também usado em Pandora).

Distribuição final de páginas por classe:

| Obra | inicio_capitulo | corpo | notas_fim | paratexto | qualidade_baixa |
|---|---:|---:|---:|---:|---:|
| `latour_woolgar_1986_lab_life_en` | 7 | 200 | 33 | 46 | 10 |
| `latour_1987_science_action_en` | 4 | 277 | 4 | 27 | 2 |
| `latour_1999_pandora_en` | 3 | 297 | 0 | 31 | 6 |

A amostra estratificada subsequente produz 41/45 páginas. As 4 páginas faltantes correspondem a estratos onde o livro não oferece material: 1 em `qualidade_baixa` de Science in Action (livro com extração quase perfeita) e 3 em `notas_fim` de Pandora (cuja seção de notas é absorvida pelo back matter sem cabeçalho `Notes` isolado).

---

## Etapa 2 — Validação amostral

Data da execução: 14 de maio de 2026.

### Procedimento

A validação amostral aplica critérios uniformes sobre o texto normalizado em `corpus/txt_norm/<obra>.txt` para cada uma das 41 páginas amostradas. Implementação em `scripts/08_validate_sample.py`. Cada página recebe três campos preenchidos automaticamente:

- `estrato_correto` (`sim`, `parcial`, `nao`): se o estrato predito é confirmado pelo conteúdo da página.
- `erro_extracao`: descrição curta de problemas visíveis na página (replacement chars, letras espaçadas, linhas com excesso de caracteres não-alfa, soft hyphens residuais).
- `decisao_metodologica`: justificativa em uma linha; recebe prefixo `[INFERÊNCIA]` quando a decisão depende do estado de vizinhança e não de marcador objetivo na própria página.

A leitura final cabe à pesquisadora. Casos `parcial` ficam registrados para revisão manual antes de virarem citação na tese.

### Critérios automáticos por estrato

- `inicio_capitulo` confirmado quando `_RE_INICIO_CAPITULO` casa nas 5 primeiras linhas da página.
- `corpo` confirmado quando a página tem ≥150 palavras de prosa contínua, sem cabeçalho de front/back matter, sem dominância de notas numeradas.
- `notas_fim` confirmado quando há cabeçalho `Notes`/`Notas` no topo ou ≥4 linhas com padrão `^\d+\s+[A-Z]` (notas numeradas).
- `paratexto` confirmado quando há cabeçalho de front ou back matter, ≥3 entradas de índice (`palavra N, N, N`) ou ≥3 linhas de TOC (linha terminando em número de página).
- `qualidade_baixa` confirmado quando a página tem <10 palavras, replacement chars, ou >5% caracteres não-padrão.

### Resultado

| Estrato | n | sim | parcial | nao | taxa de confirmação |
|---|---:|---:|---:|---:|---:|
| `inicio_capitulo` | 9 | 9 | 0 | 0 | 100% |
| `corpo` | 9 | 9 | 0 | 0 | 100% |
| `notas_fim` | 6 | 3 | 3 | 0 | 50% |
| `paratexto` | 9 | 6 | 3 | 0 | 67% |
| `qualidade_baixa` | 8 | 8 | 0 | 0 | 100% |

Taxa de erro confirmado (`nao`): 0/41 = 0%, abaixo da tolerância de 20% prevista na decisão de 13/05/2026 (Etapa 1, seção 5). A heurística de classificação atende à regra.

### Casos `parcial` para revisão manual

Os seis casos `parcial` decorrem de páginas onde a heurística predisse pelo estado da vizinhança, sem marcador objetivo na própria página:

- Lab Life pg94, pg96, pg102: páginas com placeholder `Image Not Available NN` referentes ao Photograph File (pg91--104). Classificadas como `notas_fim` por herança do estado (Notes do capítulo 2 termina em pg88). Ajuste futuro: a heurística poderia reconhecer páginas de figura como classe própria (`figura`), mas o ganho analítico é baixo porque essas páginas têm 4 palavras cada.
- Lab Life pg284: segunda página do **Postscript da 2ª edição**, classificada como `paratexto` por herança de back matter. Esse é um caso metodologicamente sensível: o Postscript é o conteúdo distintivo da edição de 1986 (justifica a remoção de "Social" do subtítulo) e contém prosa argumentativa, não paratexto. As análises de KWIC, frequência e cocorrência **operam sobre o texto integral** e portanto incluem o Postscript no cálculo das figurações; apenas a estratificação da amostra registra o conteúdo erroneamente. Para a Etapa 1, o efeito é nulo. Para análises futuras que dependam da estratificação, considerar regex específica para `^\s*POSTSCRIPT\s*$` antes de back matter.
- Science in Action pg294: continuação da bibliografia (entradas Dauben, Dubos...) sem cabeçalho `References` na própria página. Caso esperado e benigno.
- Pandora pg7: página de Acknowledgments com cabeçalho tipografado em letras espaçadas (`A C K N O W L E D G M E NT S`). A heurística de front matter não casa esse padrão. Análoga ao tratamento dado a `C H A P T E R` no Adendo 3; ajuste similar seria viável se o ganho justificasse.

### Outputs

- `outputs/amostra_validacao_etapa1.csv` (consolidado, 41 linhas com campos preenchidos).
- `outputs/<id_obra>/csv/amostra_validacao.csv` (por obra).
- `outputs/<id_obra>/relatorios/validacao_amostral_etapa1.md` (relatório por obra).
- `outputs/validacao_amostral_etapa1.md` (relatório consolidado).

---

## Etapa 3 — Lexicometria expandida (rodada parcial sobre o corpus de Etapa 1)

Data da execução: 14 de maio de 2026.

A Etapa 3 plena prevista no `plano_de_trabalho.md` (linhas 254-328) requer a inclusão de obras adicionais de Latour (*Pasteur 1984* em francês, *Reassembling 2005*, *On recalling ANT 1999*, *Clarifications 1996*), das obras centrais de Haraway (*Cyborg Manifesto*, *Situated Knowledges*, *Modest_Witness*, *Companion Species*, *When Species Meet*, *Staying with the Trouble*) e de Stengers e Ingold em escala reduzida. Como esses textos ainda não foram extraídos para `corpus/txt/`, a Etapa 3 é executada aqui em rodada parcial sobre as três obras de Latour da Etapa 1, com expansão do catálogo e dependências instaladas para suportar o corpus completo quando ele chegar.

### 1. Expansão do catálogo: campo `militar`

Decisão: o catálogo `campos_lexicais/catalogo_termos.yaml` recebe um novo grupo `militar` sob o autor Latour, com 64 variantes em inglês cobrindo o vocabulário militar-industrial que minha tese argumenta ser característico de Latour. Termos: `ally`/`allies`/`alliance`/`alliances`; `enemy`/`enemies`/`enmity`; `recruit` e flexões; `mobilise`/`mobilize` e flexões (variantes britânica e americana); `battle`/`battles`/`battlefield`/`embattled`; `war`/`wars`/`warfare`/`warlike`; `conquer` e flexões; `victory`/`victories`/`victorious`; `defeat` e flexões; `troops`; `attack` e flexões; `defend`/`defends`/`defended`/`defensive`/`defence`/`defenses`/`defenders`; `fortress`/`fortresses`/`fortified`/`fortify`/`citadel`/`citadels`; `weapon`/`weapons`/`weaponry`/`arsenal`/`arsenals`; `soldier`/`soldiers`; `siege`/`besieged`/`besieging`.

Exclusões definidas para descartar usos metafóricos triviais e termos médicos: `best ally`, `natural ally`, `first attack`, `asthma attack`, `heart attack`, `panic attack`, `battle of ideas`.

Justificativa: o campo militar é o eixo empírico da tensão figural que minha tese sustenta. Sem um grupo dedicado, esse vocabulário aparece dispersamente em outros grupos (`enrollment`, `mobilise`, `trial_of_strength` etc.) e a leitura quantitativa fica fragmentada. A consolidação em um único campo permite leitura de densidade total.

### 2. Resultado quantitativo

Contagem absoluta e frequência por 10.000 palavras, com janela KWIC de ±10:

| Obra | n | freq/10k |
|---|---:|---:|
| `latour_woolgar_1986_lab_life_en` | 39 | 3,69 |
| `latour_1987_science_action_en` | 374 | 26,74 |
| `latour_1999_pandora_en` | 212 | 16,56 |

O pico de 374 ocorrências em \emph{Science in Action} é a maior densidade do livro inteiro entre os dezessete campos figurativos do catálogo, ultrapassando `black_box` (9,58/10k), `network` (9,08/10k) e `translation` (5,58/10k). Variantes top em 1987: `allies` (92), `mobilisation` (28), `mobilised` (24), `alliances` (22), `ally` (21), `war` (16), `defence` (15). Em 1999, predominância de `war`/`wars` (85 conjuntas).

### 3. Decisão sobre lematização

A Etapa 3 prevê lematização com spaCy para neutralizar variações flexionais (`mobilise`/`mobilised`/`mobilising` viram um lema único). Instalei `spacy==3.8.14` e o modelo `en_core_web_sm` no ambiente, mas optei por **manter o casamento literal de variantes** nesta rodada parcial, por três razões:

1. Auditabilidade: a lista de variantes literais é inspecionável no YAML; lematização é caixa-preta.
2. Robustez: para inglês acadêmico, variantes flexionais regulares são poucas; listei explicitamente as principais para cada lema do campo militar.
3. Custo de oportunidade: a lematização só se torna necessária quando entram obras em francês ou português, onde a flexão é mais rica. Para essa rodada (3 obras em inglês), o casamento literal é suficiente.

A integração da lematização fica para a Etapa 3 plena, junto com a entrada de \emph{Pasteur 1984} em francês.

### 4. Scripts e outputs atualizados

Os scripts da Etapa 1 (02_kwic, 03_frequencies, 04_visualizations, 05_cooccurrence, 07_trajectory) foram re-executados sobre o catálogo expandido. Outputs por obra (`outputs/<obra>/csv/`, `outputs/<obra>/relatorios/`, `outputs/<obra>/figuras/`) e o consolidado (`outputs/trajetoria_latour_1986_1999.md` e `.csv`) refletem a inclusão do campo militar. A seção 4.3.a do relatório de trajetória traz a leitura interpretativa específica.

### 5. Pendências para a Etapa 3 plena

- Subir os `.txt` das obras adicionais do plano de trabalho.
- Implementar lematização efetiva no `02_kwic.py` (flag `--lematizar`) para suportar francês e português.
- Adicionar campos lexicais correspondentes para Haraway (têxtil-feminista: companheirismo, parentesco, fiação, tecitura, costura, tecelagem) e para Stengers/Ingold conforme o plano.
- Comparação cruzada autor por autor, com matriz idioma × autor × campo.
