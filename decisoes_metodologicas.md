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

(reservar espaço para revisões posteriores das decisões acima, com data e justificativa)
---

## Refinamento da Etapa 3 — Desambiguação de `war`/`wars` no campo militar

Data da decisão: 14 de maio de 2026.

### Motivação

A leitura crítica do relatório `outputs/trajetoria_latour_1986_1999.md` identificou um efeito de inflação na densidade do campo `militar` em \emph{Pandora's Hope} (1999). Das 212 ocorrências contabilizadas no campo, 85 são da variante `war`/`wars`. Parte dessas ocorrências aparece em colocações que nomeiam objetos historicamente datados, como `science wars`, `World War II`, `Cold War`, `Franco-Prussian war`, `phony war`, `Ministry of War`, e em referências bibliográficas (Tolstoi, \emph{War and Peace}). Esses usos são descritivos de um objeto nomeado, não mobilizações figurativas do vocabulário militar pela escrita de Latour. Contar esses usos junto com os figurativos confunde dois fenômenos distintos e enfraquece o argumento empírico que a tese constrói sobre a tensão figural Latour-Haraway.

### Decisão

A análise do campo `militar` passa a registrar, para cada obra, duas contagens: a **contagem bruta** (todas as ocorrências detectadas pelo catálogo, sem filtro) e a **contagem refinada** (com subtração das ocorrências de `war`/`wars` classificadas como descritivo-históricas).

A classificação é binária: `descritivo` para usos em colocação histórica ou editorial nomeada; `figurativo` para mobilizações do vocabulário militar como tropo descritivo da prática científica ou da polêmica metafísica. A regra opera em duas camadas:

1. **Camada automática**: a ocorrência é classificada como `descritivo` se houver, nas 5 palavras adjacentes ao termo (de cada lado), um dos seguintes gatilhos lexicais (case-insensitive): `science`, `culture`, `cold`, `world war`, `second world`, `first world`, `great war`, `post-war`, `pre-war`, `vietnam`, `korean`, `civil war`, `gulf war`, `nuclear war`.

2. **Camada manual**: ocorrências não capturadas pela camada automática são revisadas em janela ampliada (capítulo inteiro quando necessário) e classificadas com justificativa breve. A camada manual cobre casos em que a colocação está fora da janela KWIC (e.g. `science wars` mencionado uma vez no início do capítulo e referido por elipse depois), referências históricas sem termo-âncora explícito (capítulos sobre Joliot e Szilard que narram WWII), instituições nomeadas (`Ministry of War`), referências bibliográficas e alusões textuais clássicas (Hobbes `war of all against all`, Tolstoi).

### Aplicação simétrica

A desambiguação se aplica às três obras do corpus, não apenas a \emph{Pandora's Hope}. A aplicação simétrica garante comparabilidade: filtrar apenas a obra em que o efeito é visível introduziria viés.

### Resultado

| Obra | Bruto ($n$) | Bruto/10k | Descritivo subtraído | Refinado ($n$) | Refinado/10k |
|---|---:|---:|---:|---:|---:|
| \emph{Laboratory Life} (1986) | 39 | 3,69 | 2 | 37 | 3,50 |
| \emph{Science in Action} (1987) | 374 | 26,74 | 10 | 364 | 26,03 |
| \emph{Pandora's Hope} (1999) | 212 | 16,56 | 56 | 156 | 12,19 |

A queda em \emph{Pandora's Hope} é de 26,4% do campo militar; em \emph{Science in Action}, 2,7%; em \emph{Laboratory Life}, 5,1%. O pico de 1987 permanece como ponto de cristalização do vocabulário militar-industrial em uso figurativo. A leitura da seção 4.3.a do relatório de trajetória precisa de ajuste: o vocabulário militar figurativo recua pela metade entre 1987 e 1999 em densidade por dez mil palavras, em vez de se manter estável; parte da aparência de continuidade vinha de Latour estar narrando historicamente a militarização da ciência no século XX (Joliot, Szilard, science wars).

### Artefatos

- `outputs/refinamento/war_pandora_classificacao.csv`: os 85 hits de `war`/`wars` em \emph{Pandora's Hope} classificados um a um, com justificativa.
- `outputs/refinamento/militar_refinado_tres_obras.csv`: tabela consolidada bruto/refinado para as três obras.
- `outputs/refinamento/tabela_militar_refinada.tex`: tabela em LaTeX pronta para `\input{}` na tese.

### Pendência para script

A camada automática de desambiguação está implementada em script ad hoc (`/home/claude/desambiguar_war_pandora.py` no ambiente da sessão de 14/05/2026, não versionado). Para entrar no pipeline reprodutível da Etapa 3 plena, será necessário portar a lógica para `scripts/`, com nome sugerido `09_desambiguar_war.py`, e incluí-lo no `run_etapa1.sh` (ou criar `run_etapa3.sh` se a Etapa 3 plena exigir orquestração própria). A camada manual fica documentada em planilha auditável, fora do script.
