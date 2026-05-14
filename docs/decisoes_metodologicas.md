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
